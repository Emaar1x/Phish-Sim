# Phishing Email Simulation Platform

A comprehensive cybersecurity awareness and phishing simulation platform designed to help organizations test employee susceptibility to phishing attacks with full consent and ethical training purposes.

## ⚠️ Important Notice

**This tool is intended for authorized security training only.** Always obtain proper consent before running simulations. This platform does not collect credentials and is designed purely for educational and awareness purposes.

## Features

- **Email Template System**: Pre-built phishing email templates (password reset, invoice, HR notices)
- **Click Tracking**: Unique tracking links with automatic click logging
- **Employee Management**: Add and manage employees with department tracking
- **Campaign Management**: Create and launch phishing simulation campaigns
- **Analytics Dashboard**: View click-through rates, risk scores, and department statistics
- **CSV Export**: Export campaign results for analysis
- **Risk Scoring**: Individual and department-level risk assessment

## Requirements

- Python 3.8 or higher
- SMTP server (for email delivery)
  - **Recommended**: [MailHog](https://github.com/mailhog/MailHog) for local testing
  - Or any SMTP server (Gmail, SendGrid, etc.)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Emaar1x/Phish-Sim.git
   cd Phish-Sim
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SMTP server** (for local testing with MailHog)
   
   **Option A - Download MailHog:**
   - Download from: https://github.com/mailhog/MailHog/releases
   - Run `MailHog.exe` (Windows) or `./MailHog` (Linux/Mac)
   - Web UI available at: http://localhost:8025
   
   **Option B - Docker:**
   ```bash
   docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
   ```

4. **Configure settings** (optional)
   
   Edit `config.py` or set environment variables:
   ```bash
   export SMTP_HOST=localhost
   export SMTP_PORT=1025
   export SMTP_FROM_EMAIL=security@company.com
   export SMTP_FROM_NAME="IT Security Team"
   export BASE_URL=http://localhost:5000
   ```

## Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Accessing the Dashboard

Open your browser and navigate to:
```
http://localhost:5000/admin
```

### Basic Workflow

1. **Add Employees**
   - Navigate to "Employees" → Click "Add Employee"
   - Enter name, email, and department
   - Click "Add Employee"

2. **Create a Campaign**
   - Navigate to "Campaigns" → Click "Create Campaign"
   - Fill in campaign details:
     - Campaign name
     - Email template (password_reset, invoice, or hr_notice)
     - Sender name and email
     - Company name
   - Click "Create Campaign"

3. **Launch Campaign**
   - Click on the campaign name to view details
   - Click "Launch Campaign"
   - Select employees to send emails to
   - Click "Launch Campaign"

4. **View Results**
   - Check MailHog (http://localhost:8025) to view sent emails
   - Click links in emails to test tracking
   - View click logs and statistics in the dashboard

## Project Structure

```
Phish-Sim/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database initialization
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── models/               # Database models
│   ├── employee.py
│   ├── campaign.py
│   ├── click_log.py
│   └── email_template.py
│
├── routes/               # Flask routes/blueprints
│   ├── admin.py         # Admin dashboard routes
│   ├── campaign.py     # Campaign management routes
│   └── tracking.py      # Click tracking routes
│
├── templates/           # HTML templates
│   ├── emails/         # Email templates
│   ├── dashboard/      # Admin dashboard templates
│   └── awareness/      # Awareness page templates
│
└── utils/              # Utility functions
    ├── email_sender.py  # SMTP email sending
    └── template_engine.py  # Template rendering
```

## Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
# Database
DATABASE_URI=sqlite:///phish_simulator.db  # or PostgreSQL URI

# SMTP Settings
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=                    # Optional
SMTP_PASSWORD=                # Optional
SMTP_USE_TLS=False
SMTP_FROM_EMAIL=security@company.com
SMTP_FROM_NAME=IT Security Team

# Application
SECRET_KEY=your-secret-key-here
DEBUG=True
BASE_URL=http://localhost:5000
COMPANY_NAME=Your Company
```

### Database

- **Default**: SQLite (no setup required, database created automatically)
- **Production**: Set `DATABASE_URI` environment variable to use PostgreSQL

## Email Templates

The platform includes three pre-built email templates:

1. **password_reset**: Urgent password reset notification
2. **invoice**: Fake invoice payment request
3. **hr_notice**: HR policy update notification

All templates include:
- Hidden training disclaimers in HTML comments
- Variable substitution (employee name, company name, tracking links)
- Responsive HTML design

## Security & Ethics

### Best Practices

- Always obtain proper authorization before running simulations
- Inform employees about the training program
- Provide educational feedback after simulations
- Handle employee data according to privacy regulations
- Use realistic but clearly marked (in HTML comments) templates

### What This Platform Does NOT Do

- ❌ Collect credentials
- ❌ Harvest personal information
- ❌ Send emails without authorization
- ❌ Store sensitive data beyond training metrics

## Troubleshooting

### Emails Not Sending

- Verify SMTP server is running (check MailHog at http://localhost:8025)
- Check `SMTP_HOST` and `SMTP_PORT` in `config.py`
- Review application logs for SMTP errors

### Database Issues

- Delete `instance/phish_simulator.db` to reset the database
- Restart the application (database will be recreated automatically)

### Tracking Links Not Working

- Verify `BASE_URL` in `config.py` matches your server URL
- Ensure the tracking route is accessible

## License

This project is provided for educational and training purposes. Use responsibly and ethically.

## Contributing

Contributions are welcome! Please ensure that:
- Code follows the existing style
- All changes are tested
- Security and ethical considerations are maintained

## Disclaimer

This tool is designed for **authorized security training only**. The authors are not responsible for misuse of this software. Always:
- Obtain proper authorization
- Follow your organization's security policies
- Comply with applicable laws and regulations
- Use responsibly and ethically

---

**Remember**: The goal is education and awareness, not to trick employees. Always provide proper training and feedback after simulations.
