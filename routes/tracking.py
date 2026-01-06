"""
Tracking routes for handling email link clicks
"""
from flask import Blueprint, render_template, request
from database import db
from models.click_log import ClickLog
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track/<tracking_token>')
def track_click(tracking_token):
    """
    Track when an employee clicks on a phishing simulation link
    """
    # Find the click log entry
    click_log = ClickLog.query.filter_by(tracking_token=tracking_token).first()
    
    if not click_log:
        # Invalid token - show generic message
        return render_template('awareness/clicked.html', 
                             message="Invalid tracking link.",
                             is_valid=False)
    
    # Check if this is the first click (clicked_at is None initially)
    is_first_click = click_log.clicked_at is None
    
    if is_first_click:
        # First click - record it
        click_log.clicked_at = datetime.utcnow()
        click_log.ip_address = request.remote_addr
        click_log.user_agent = request.headers.get('User-Agent', '')
        db.session.commit()
        
        logger.info(f"Click tracked: Campaign {click_log.campaign_id}, Employee {click_log.employee_id}")
    
    # Get campaign and employee info
    campaign = click_log.campaign
    employee = click_log.employee
    
    # Show awareness page
    return render_template('awareness/clicked.html',
                         message="This was a phishing simulation for security training.",
                         campaign_name=campaign.name if campaign else "Unknown Campaign",
                         employee_name=employee.name if employee else "Unknown",
                         is_valid=True)

