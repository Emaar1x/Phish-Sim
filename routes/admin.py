"""
Admin routes for managing employees, campaigns, and viewing results
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from database import db
from models.employee import Employee
from models.campaign import Campaign
from models.click_log import ClickLog
from models.email_template import EmailTemplate
from datetime import datetime
import csv
from io import StringIO

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    """
    Main admin dashboard
    """
    # Get statistics
    total_employees = Employee.query.count()
    total_campaigns = Campaign.query.count()
    total_clicks = ClickLog.query.count()
    
    # Get recent campaigns
    recent_campaigns = Campaign.query.order_by(Campaign.created_at.desc()).limit(5).all()
    
    # Get employees with risk scores
    employees = Employee.query.all()
    employee_risk_data = [
        {
            'name': emp.name,
            'email': emp.email,
            'department': emp.department,
            'risk_score': emp.get_risk_score()
        }
        for emp in employees
    ]
    
    # Department-wise statistics
    departments = {}
    for emp in employees:
        dept = emp.department
        if dept not in departments:
            departments[dept] = {
                'total': 0,
                'total_clicks': 0,
                'employees': []
            }
        departments[dept]['total'] += 1
        departments[dept]['total_clicks'] += len(emp.click_logs)
        departments[dept]['employees'].append(emp.get_risk_score())
    
    # Calculate department risk scores
    dept_stats = []
    for dept, data in departments.items():
        avg_risk = sum(data['employees']) / len(data['employees']) if data['employees'] else 0
        dept_stats.append({
            'department': dept,
            'total_employees': data['total'],
            'total_clicks': data['total_clicks'],
            'avg_risk_score': round(avg_risk, 2)
        })
    
    return render_template('dashboard/admin.html',
                         total_employees=total_employees,
                         total_campaigns=total_campaigns,
                         total_clicks=total_clicks,
                         recent_campaigns=recent_campaigns,
                         employee_risk_data=employee_risk_data,
                         dept_stats=dept_stats)

@admin_bp.route('/employees', methods=['GET', 'POST'])
def employees():
    """
    Manage employees - GET shows list, POST adds new employee
    """
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name')
        email = data.get('email')
        department = data.get('department')
        
        if not all([name, email, department]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if email already exists
        existing = Employee.query.filter_by(email=email).first()
        if existing:
            return jsonify({'error': 'Employee with this email already exists'}), 400
        
        employee = Employee(name=name, email=email, department=department)
        db.session.add(employee)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'message': 'Employee added successfully', 'employee': employee.to_dict()}), 201
        else:
            flash('Employee added successfully', 'success')
            return redirect(url_for('admin.employees'))
    
    # GET request - show all employees
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    return render_template('dashboard/employees.html', employees=employees)

@admin_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """
    Delete an employee
    """
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'}), 200

@admin_bp.route('/campaigns')
def campaigns():
    """
    List all campaigns
    """
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    templates = EmailTemplate.query.all()
    return render_template('dashboard/campaigns.html', campaigns=campaigns, templates=templates)

@admin_bp.route('/campaigns/<int:campaign_id>')
def campaign_detail(campaign_id):
    """
    View campaign details and results
    """
    campaign = Campaign.query.get_or_404(campaign_id)
    # Only show click logs that were actually clicked (clicked_at is not None)
    click_logs = ClickLog.query.filter_by(campaign_id=campaign_id).filter(
        ClickLog.clicked_at.isnot(None)
    ).order_by(ClickLog.clicked_at.desc()).all()
    
    # Get all click_logs for statistics (including unclicked ones)
    all_click_logs = ClickLog.query.filter_by(campaign_id=campaign_id).all()
    
    return render_template('dashboard/campaign_detail.html', 
                         campaign=campaign, 
                         click_logs=click_logs,
                         all_click_logs_count=len(all_click_logs),
                         clicked_logs_count=len(click_logs))

@admin_bp.route('/test-smtp')
def test_smtp():
    """
    Test SMTP connection and email delivery
    """
    from utils.email_sender import send_phishing_email
    import config
    
    test_email = request.args.get('email', 'test@example.com')
    
    try:
        # Test connection first
        import smtplib
        import socket
        
        # Check if port is open
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((config.SMTP_HOST, config.SMTP_PORT))
        sock.close()
        
        if result != 0:
            return jsonify({
                'status': 'error',
                'message': f'Cannot connect to SMTP server at {config.SMTP_HOST}:{config.SMTP_PORT}',
                'suggestion': 'Make sure MailHog is running'
            }), 500
        
        # Try sending a test email
        success = send_phishing_email(
            to_email=test_email,
            to_name='Test User',
            subject='SMTP Test Email',
            html_body='<p>This is a test email to verify SMTP is working.</p>'
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Test email sent successfully to {test_email}. Check MailHog at http://localhost:8025'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send test email. Check application logs for details.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error testing SMTP: {str(e)}'
        }), 500

@admin_bp.route('/results/export')
def export_results():
    """
    Export campaign results as CSV
    """
    campaigns = Campaign.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Campaign Name', 'Template', 'Status', 'Emails Sent', 'Clicks', 'Click-Through Rate (%)', 'Created At'])
    
    # Write data
    for campaign in campaigns:
        writer.writerow([
            campaign.name,
            campaign.template.name if campaign.template else 'N/A',
            campaign.status,
            campaign.get_emails_sent_count(),
            campaign.get_clicks_count(),
            campaign.get_click_through_rate(),
            campaign.created_at.strftime('%Y-%m-%d %H:%M:%S') if campaign.created_at else ''
        ])
    
    output.seek(0)
    
    from flask import Response
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=campaign_results.csv'}
    )

