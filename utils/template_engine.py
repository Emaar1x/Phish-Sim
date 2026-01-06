"""
Template engine for rendering email templates with variables
"""
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import random
from datetime import datetime, timedelta

def render_email_template(template_name, variables):
    """
    Render an email template with provided variables
    
    Args:
        template_name: Name of the template (e.g., 'password_reset')
        variables: Dictionary of variables to substitute
    
    Returns:
        str: Rendered HTML email body
    """
    # Get templates directory
    templates_dir = Path(__file__).parent.parent / 'templates' / 'emails'
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    
    # Add default variables if not provided
    default_vars = {
        'random_number': random.randint(1000, 9999),
        'amount': f"{random.randint(100, 999)}.{random.randint(10, 99)}",
        'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
        'deadline_date': (datetime.now() + timedelta(days=3)).strftime('%B %d, %Y')
    }
    
    # Merge variables
    template_vars = {**default_vars, **variables}
    
    # Load and render template
    template_file = f"{template_name}.html"
    template = env.get_template(template_file)
    
    return template.render(**template_vars)

