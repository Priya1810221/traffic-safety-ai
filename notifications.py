# notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailNotifier:
    """Handles email notifications for traffic violations"""
    
    def __init__(self):
        # Email configuration (using environment variables)
        self.sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your_app_password')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        
    def send_email(self, to_email, subject, body):
        """Send email notification to manager"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = to_email
            
            # Create HTML version of the email
            html_body = self._create_html_body(body)
            
            # Attach plain text and HTML versions
            message.attach(MIMEText(body, 'plain'))
            message.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email credentials.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _create_html_body(self, text_body):
        """Create HTML formatted email body"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #333;
                    }}
                    .alert-box {{
                        background-color: #fff3cd;
                        border: 1px solid #ffc107;
                        padding: 15px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }}
                    .violation-details {{
                        background-color: #f8f9fa;
                        padding: 15px;
                        border-left: 4px solid #dc3545;
                        margin: 10px 0;
                    }}
                    .high-severity {{
                        color: #dc3545;
                        font-weight: bold;
                    }}
                    .medium-severity {{
                        color: #ffc107;
                        font-weight: bold;
                    }}
                    .low-severity {{
                        color: #28a745;
                        font-weight: bold;
                    }}
                    footer {{
                        font-size: 12px;
                        color: #666;
                        margin-top: 20px;
                        padding-top: 10px;
                        border-top: 1px solid #ddd;
                    }}
                </style>
            </head>
            <body>
                <div class="alert-box">
                    <h2>⚠️ Traffic Safety Alert</h2>
                    <p>A traffic rule violation has been detected and reported.</p>
                </div>
                <div class="violation-details">
                    <pre>{text_body}</pre>
                </div>
                <footer>
                    <p>This is an automated notification from the Traffic Safety AI System.</p>
                    <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </footer>
            </body>
        </html>
        """
        return html
    
    def send_daily_summary(self, to_email, violations_summary):
        """Send daily summary of violations to manager"""
        try:
            subject = f"Daily Traffic Safety Report - {datetime.now().strftime('%Y-%m-%d')}"
            body = f"""
Dear Manager,

Here is your daily traffic safety summary:

Total Violations Today: {violations_summary['total']}
High Severity: {violations_summary['high']}
Medium Severity: {violations_summary['medium']}
Low Severity: {violations_summary['low']}

Most Common Violation: {violations_summary['most_common']}

Please review and take necessary actions.

Best regards,
Traffic Safety AI System
            """
            
            return self.send_email(to_email, subject, body)
            
        except Exception as e:
            logger.error(f"Failed to send daily summary: {str(e)}")
            return False
