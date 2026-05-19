# notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()
logger = logging.getLogger(__name__)

class EmailNotifier:
    """Handles email notifications for traffic safety violations"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your_app_password')
    
    def send_email(self, to_email, subject, body):
        """Send email notification"""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = to_email
            
            # Attach plain text and HTML versions
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            html_body = self._create_html_body(body)
            html_part = MIMEText(html_body, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email and password.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _create_html_body(self, text_body):
        """Convert text body to HTML format"""
        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background-color: #d32f2f;
                        color: white;
                        padding: 20px;
                        border-radius: 8px 8px 0 0;
                        text-align: center;
                    }}
                    .content {{
                        padding: 20px;
                        line-height: 1.6;
                    }}
                    .footer {{
                        background-color: #f9f9f9;
                        padding: 10px;
                        text-align: center;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>⚠️ Traffic Safety Alert</h2>
                    </div>
                    <div class="content">
                        <pre style="white-space: pre-wrap; word-wrap: break-word;">{text_body}</pre>
                    </div>
                    <div class="footer">
                        <p>This is an automated notification from Traffic Safety AI System</p>
                        <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        return html
    
    def send_daily_summary(self, manager_email, violations_data):
        """Send daily summary of violations"""
        try:
            total_violations = len(violations_data)
            high_severity = len([v for v in violations_data if v.get('severity') == 'High'])
            medium_severity = len([v for v in violations_data if v.get('severity') == 'Medium'])
            low_severity = len([v for v in violations_data if v.get('severity') == 'Low'])
            
            subject = f"Daily Traffic Safety Summary - {datetime.now().strftime('%Y-%m-%d')}"
            
            body = f"""
Dear Manager,

Here is your daily traffic safety summary:

Total Violations: {total_violations}
- High Severity: {high_severity}
- Medium Severity: {medium_severity}
- Low Severity: {low_severity}

Please review the violations and take necessary action.

Best regards,
Traffic Safety AI System
            """
            
            return self.send_email(manager_email, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending daily summary: {str(e)}")
            return False
