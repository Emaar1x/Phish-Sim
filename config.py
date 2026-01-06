"""
Configuration file for Phishing Simulation Platform
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Database configuration
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///phish_simulator.db')

# SMTP Configuration (for email sending)
SMTP_HOST = os.getenv('SMTP_HOST', 'localhost')
SMTP_PORT = int(os.getenv('SMTP_PORT', 1025))  # MailHog default port
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'False').lower() == 'true'
SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', 'security@company.com')
SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'IT Security Team')

# Application configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Base URL for tracking links
BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

# Company default name
DEFAULT_COMPANY_NAME = os.getenv('COMPANY_NAME', 'Your Company')

