"""
Email sending utility for phishing simulation emails
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import config
import logging

logger = logging.getLogger(__name__)

def send_phishing_email(to_email, to_name, subject, html_body, sender_name=None, sender_email=None):
    """
    Send a phishing simulation email via SMTP
    
    Args:
        to_email: Recipient email address
        to_name: Recipient name
        subject: Email subject
        html_body: HTML email body
        sender_name: Sender display name (defaults to config)
        sender_email: Sender email (defaults to config)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Use config defaults if not provided
        sender_name = sender_name or config.SMTP_FROM_NAME
        sender_email = sender_email or config.SMTP_FROM_EMAIL
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = formataddr((to_name, to_email))
        
        # Add HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Connect to SMTP server and send
        try:
            server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10)
            server.set_debuglevel(0)  # Set to 1 for debug output
            
            if config.SMTP_USE_TLS:
                server.starttls()
            
            if config.SMTP_USER and config.SMTP_PASSWORD:
                server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            
            # Send email and get response
            send_errors = server.send_message(msg)
            server.quit()
            
            # Check if there were any errors
            if send_errors:
                logger.error(f"Email sending errors for {to_email}: {send_errors}")
                return False
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except (smtplib.SMTPConnectError, smtplib.SMTPAuthenticationError, 
                smtplib.SMTPServerDisconnected, ConnectionRefusedError, OSError) as e:
            logger.error(f"Connection error sending email to {to_email}: {str(e)}")
            return False
            
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error sending email to {to_email}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {str(e)}")
        return False

