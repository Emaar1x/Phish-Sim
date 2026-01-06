"""
Email template model for storing email templates
"""
from database import db
from datetime import datetime

class EmailTemplate(db.Model):
    """
    EmailTemplate model representing email templates for phishing simulations
    """
    __tablename__ = 'email_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EmailTemplate {self.name}>'
    
    def to_dict(self):
        """
        Convert email template to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'subject': self.subject,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

