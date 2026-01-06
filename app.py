"""
Main Flask application for Phishing Simulation Platform
"""
from flask import Flask, redirect, url_for
from database import init_db
from routes.admin import admin_bp
from routes.campaign import campaign_bp
from routes.tracking import tracking_bp
import config
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(campaign_bp)
app.register_blueprint(tracking_bp)

@app.route('/')
def index():
    """
    Redirect to admin dashboard
    """
    return redirect(url_for('admin.dashboard'))

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    print("=" * 60)
    print("Phishing Simulation Platform")
    print("=" * 60)
    print(f"Admin Dashboard: http://localhost:5000/admin")
    print(f"SMTP Host: {config.SMTP_HOST}:{config.SMTP_PORT}")
    print("=" * 60)
    print("\nNote: Make sure your SMTP server (e.g., MailHog) is running!")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)

