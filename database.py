"""
Database initialization and session management
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Initialize database with Flask app
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        # Import all models to ensure they're registered
        from models.employee import Employee
        from models.campaign import Campaign
        from models.click_log import ClickLog
        from models.email_template import EmailTemplate
        
        # Create all tables
        db.create_all()
        
        # Initialize default email templates if they don't exist
        _init_default_templates()
    
    return db

def _init_default_templates():
    """
    Initialize default email templates in the database
    """
    from models.email_template import EmailTemplate
    
    templates = [
        {
            'name': 'password_reset',
            'subject': 'Urgent: Password Reset Required',
            'description': 'Password reset phishing simulation'
        },
        {
            'name': 'invoice',
            'subject': 'Invoice Payment Required - Action Needed',
            'description': 'Fake invoice phishing simulation'
        },
        {
            'name': 'hr_notice',
            'subject': 'HR Policy Update - Please Review',
            'description': 'HR policy update phishing simulation'
        }
    ]
    
    for template_data in templates:
        existing = EmailTemplate.query.filter_by(name=template_data['name']).first()
        if not existing:
            template = EmailTemplate(
                name=template_data['name'],
                subject=template_data['subject'],
                description=template_data['description']
            )
            db.session.add(template)
    
    db.session.commit()

