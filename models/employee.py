"""
Employee model for storing employee information
"""
from database import db
from datetime import datetime

class Employee(db.Model):
    """
    Employee model representing employees in the organization
    """
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    click_logs = db.relationship('ClickLog', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Employee {self.name} ({self.email})>'
    
    def to_dict(self):
        """
        Convert employee to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_risk_score(self):
        """
        Calculate risk score based on click history
        Higher score = more susceptible to phishing
        Only counts actual clicks (where clicked_at is not None)
        """
        # Only count actual clicks, not just click_logs
        actual_clicks = [log for log in self.click_logs if log.clicked_at is not None]
        total_campaigns = len(set(log.campaign_id for log in actual_clicks))
        total_clicks = len(actual_clicks)
        
        if total_campaigns == 0:
            return 0
        
        # Risk score: percentage of campaigns clicked
        # Also factor in total clicks (multiple clicks = higher risk)
        click_rate = (total_clicks / total_campaigns) * 100
        return min(100, int(click_rate))

