"""
Campaign model for storing phishing simulation campaigns
"""
from database import db
from datetime import datetime
import uuid

class Campaign(db.Model):
    """
    Campaign model representing a phishing simulation campaign
    """
    __tablename__ = 'campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('email_templates.id'), nullable=False)
    sender_name = db.Column(db.String(200), nullable=False)
    sender_email = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False, default='Your Company')
    status = db.Column(db.String(50), default='draft')  # draft, sent, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    template = db.relationship('EmailTemplate', backref='campaigns')
    click_logs = db.relationship('ClickLog', backref='campaign', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Campaign {self.name} ({self.status})>'
    
    def to_dict(self):
        """
        Convert campaign to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'template_id': self.template_id,
            'template_name': self.template.name if self.template else None,
            'sender_name': self.sender_name,
            'sender_email': self.sender_email,
            'company_name': self.company_name,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'emails_sent': self.get_emails_sent_count(),
            'clicks': self.get_clicks_count(),
            'click_through_rate': self.get_click_through_rate()
        }
    
    def get_emails_sent_count(self):
        """
        Get count of emails sent for this campaign
        Note: This would typically be stored separately, but for simplicity
        we'll use click logs to infer (not perfect, but works for demo)
        """
        # In a real system, you'd track this separately
        # For now, we'll use unique employees who received emails
        unique_employees = len(set(log.employee_id for log in self.click_logs))
        return unique_employees
    
    def get_clicks_count(self):
        """
        Get total number of unique employees who clicked (not total click_logs)
        This prevents counting multiple clicks from the same employee or duplicate entries
        """
        clicked_logs = [log for log in self.click_logs if log.clicked_at is not None]
        # Count unique employees who clicked, not total click_logs
        unique_employees_clicked = len(set(log.employee_id for log in clicked_logs))
        return unique_employees_clicked
    
    def get_click_through_rate(self):
        """
        Calculate click-through rate percentage
        """
        emails_sent = self.get_emails_sent_count()
        if emails_sent == 0:
            return 0.0
        clicks = self.get_clicks_count()
        return round((clicks / emails_sent) * 100, 2)

