"""
Campaign routes for creating and launching phishing simulation campaigns
"""
from flask import Blueprint, request, jsonify, redirect, url_for, flash
from database import db
from models.campaign import Campaign
from models.employee import Employee
from models.email_template import EmailTemplate
from models.click_log import ClickLog
from datetime import datetime
import uuid
from utils.email_sender import send_phishing_email
from utils.template_engine import render_email_template
import config
import logging

logger = logging.getLogger(__name__)

campaign_bp = Blueprint('campaign', __name__, url_prefix='/campaign')

@campaign_bp.route('/create', methods=['POST'])
def create_campaign():
    """
    Create a new phishing simulation campaign
    """
    data = request.get_json() if request.is_json else request.form
    
    name = data.get('name')
    template_id = data.get('template_id')
    sender_name = data.get('sender_name')
    sender_email = data.get('sender_email')
    company_name = data.get('company_name', config.DEFAULT_COMPANY_NAME)
    employee_ids = data.get('employee_ids', [])
    
    if not all([name, template_id, sender_name, sender_email]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate template exists
    template = EmailTemplate.query.get(template_id)
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    # Create campaign
    campaign = Campaign(
        name=name,
        template_id=template_id,
        sender_name=sender_name,
        sender_email=sender_email,
        company_name=company_name,
        status='draft'
    )
    db.session.add(campaign)
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': 'Campaign created successfully', 'campaign': campaign.to_dict()}), 201
    else:
        flash('Campaign created successfully', 'success')
        return redirect(url_for('admin.campaigns'))

@campaign_bp.route('/<int:campaign_id>/launch', methods=['POST'])
def launch_campaign(campaign_id):
    """
    Launch a campaign - send emails to selected employees
    """
    campaign = Campaign.query.get_or_404(campaign_id)
    
    data = request.get_json() if request.is_json else request.form
    employee_ids = data.get('employee_ids', [])
    
    if not employee_ids:
        return jsonify({'error': 'No employees selected'}), 400
    
    # Get employees
    employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()
    
    if not employees:
        return jsonify({'error': 'No valid employees found'}), 404
    
    # Get template
    template = campaign.template
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    # Check if campaign was already sent
    if campaign.status == 'sent':
        return jsonify({'error': 'Campaign has already been launched'}), 400
    
    # Send emails
    sent_count = 0
    failed_count = 0
    click_logs_to_commit = []
    
    for employee in employees:
        click_log = None
        try:
            # Generate unique tracking token
            tracking_token = str(uuid.uuid4())
            
            # Generate tracking link first
            tracking_link = f"{config.BASE_URL}/track/{tracking_token}"
            
            # Render email template
            email_variables = {
                'employee_name': employee.name,
                'company_name': campaign.company_name,
                'tracking_link': tracking_link
            }
            
            html_body = render_email_template(template.name, email_variables)
            
            # Send email FIRST - only create click log if email succeeds
            success = send_phishing_email(
                to_email=employee.email,
                to_name=employee.name,
                subject=campaign.template.subject,
                html_body=html_body,
                sender_name=campaign.sender_name,
                sender_email=campaign.sender_email
            )
            
            if success:
                # Only create click log if email was successfully sent
                click_log = ClickLog(
                    campaign_id=campaign.id,
                    employee_id=employee.id,
                    tracking_token=tracking_token
                )
                db.session.add(click_log)
                click_logs_to_commit.append(click_log)
                sent_count += 1
                logger.info(f"Email sent and click log created for {employee.email}")
            else:
                failed_count += 1
                logger.warning(f"Email failed to send to {employee.email}, no click log created")
                
        except Exception as e:
            logger.error(f"Error sending email to {employee.email}: {str(e)}")
            failed_count += 1
    
    # Commit all successful click logs and update campaign status
    try:
        campaign.status = 'sent'
        campaign.sent_at = datetime.utcnow()
        db.session.commit()
        logger.info(f"Campaign {campaign.id} launched: {sent_count} sent, {failed_count} failed")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error committing campaign launch: {str(e)}")
        return jsonify({'error': 'Failed to save campaign status'}), 500
    
    response_data = {
        'message': f'Campaign launched. {sent_count} emails sent, {failed_count} failed.',
        'sent_count': sent_count,
        'failed_count': failed_count
    }
    
    if request.is_json:
        return jsonify(response_data), 200
    else:
        flash(response_data['message'], 'success' if failed_count == 0 else 'warning')
        return redirect(url_for('admin.campaign_detail', campaign_id=campaign_id))

