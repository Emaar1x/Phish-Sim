"""
Click log model for tracking email link clicks
"""
from database import db
from datetime import datetime
import uuid

class ClickLog(db.Model):
    """
    ClickLog model tracking when employees click on phishing simulation links
    """
    __tablename__ = 'click_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    tracking_token = db.Column(db.String(100), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    clicked_at = db.Column(db.DateTime, nullable=True)  # Set to None initially, updated when clicked
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    
    def __repr__(self):
        return f'<ClickLog Campaign:{self.campaign_id} Employee:{self.employee_id}>'
    
    def to_dict(self):
        """
        Convert click log to dictionary
        """
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.name if self.employee else None,
            'employee_email': self.employee.email if self.employee else None,
            'tracking_token': self.tracking_token,
            'clicked_at': self.clicked_at.isoformat() if self.clicked_at else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent
        }

