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
    """
    Handles email notifications for traffic rule violations.
    Supports real-time alerts to managers about employee violations.
    """
    
    def __init__(self):
        """
        Initialize email notifier with SMTP configuration.
        
        Environment variables required:
        - SMTP_SERVER: Email server address (default: smtp.gmail.com)
        - SMTP_PORT: Email server port (default: 587)
        - SENDER_EMAIL: Email address to send from
        - SENDER_PASSWORD: Email password or app-specific password
        """
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your_app_password')
        self.sender_name = "Traffic Safety AI System"
        
        logger.info(f"Email Notifier initialized with SMTP server: {self.smtp_server}")
    
    def send_email(self, to_email, subject, body, is_html=False):
        """
        Send email notification to manager.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body content
            is_html (bool): Whether body is HTML formatted
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Validate email
            if not to_email or '@' not in to_email:
                logger.error(f"Invalid email address: {to_email}")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
            
            # Attach body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"✅ Email sent successfully to {to_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("❌ SMTP Authentication failed. Check email credentials.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"❌ Error sending email: {str(e)}")
            return False
    
    def send_violation_alert(self, manager_email, violation_data):
        """
        Send formatted violation alert email to manager.
        
        Args:
            manager_email (str): Manager's email address
            violation_data (dict): Violation details including employee info, type, location, etc.
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"🚨 ALERT: Traffic Violation Detected - Employee {violation_data.get('employee_id', 'N/A')}"
            
            # Create HTML formatted email
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="background-color: #fff; padding: 20px; border-radius: 5px; border-left: 5px solid #ff6b6b;">
                        <h2 style="color: #ff6b6b; margin-top: 0;">⚠️ Traffic Rule Violation Alert</h2>
                        
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
                            <p style="margin: 5px 0;"><strong>Severity:</strong> <span style="color: #ff6b6b; font-weight: bold;">{violation_data.get('severity', 'MEDIUM').upper()}</span></p>
                        </div>
                        
                        <h3 style="color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px;">Employee Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; font-weight: bold; width: 150px;">Employee ID:</td>
                                <td style="padding: 8px;">{violation_data.get('employee_id', 'N/A')}</td>
                            </tr>
                            <tr style="background-color: #f9f9f9;">
                                <td style="padding: 8px; font-weight: bold;">Employee Name:</td>
                                <td style="padding: 8px;">{violation_data.get('employee_name', 'N/A')}</td>
                            </tr>
                        </table>
                        
                        <h3 style="color: #333; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-top: 20px;">Violation Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px; font-weight: bold; width: 150px;">Violation Type:</td>
                                <td style="padding: 8px;">{violation_data.get('violation_type', 'N/A')}</td>
                            </tr>
                            <tr style="background-color: #f9f9f9;">
                                <td style="padding: 8px; font-weight: bold;">Location:</td>
                                <td style="padding: 8px;">{violation_data.get('location', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; font-weight: bold;">Timestamp:</td>
                                <td style="padding: 8px;">{violation_data.get('timestamp', 'N/A')}</td>
                            </tr>
                            <tr style="background-color: #f9f9f9;">
                                <td style="padding: 8px; font-weight: bold;">Description:</td>
                                <td style="padding: 8px;">{violation_data.get('description', 'N/A')}</td>
                            </tr>
                        </table>
                        
                        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <p style="margin: 0; color: #333;">
                                <strong>Action Required:</strong> Please review the violation details and take appropriate action with the employee. 
                                Repeated violations may require disciplinary measures.
                            </p>
                        </div>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 20px; text-align: center;">
                            This is an automated alert from the Traffic Safety AI System<br>
                            Do not reply to this email
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return self.send_email(manager_email, subject, html_body, is_html=True)
            
        except Exception as e:
            logger.error(f"Error sending violation alert: {str(e)}")
            return False
    
    def send_daily_summary(self, manager_email, violations_summary):
        """
        Send daily summary of violations to manager.
        
        Args:
            manager_email (str): Manager's email address
            violations_summary (dict): Summary data including count, employees, etc.
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"📊 Daily Traffic Safety Report - {datetime.now().strftime('%Y-%m-%d')}"
            
            violations_list = "".join([
                f"<li>{v['employee_name']} ({v['employee_id']}) - {v['violation_type']} at {v['location']}</li>"
                for v in violations_summary.get('violations', [])
            ])
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Daily Traffic Safety Report</h2>
                    <p>Total Violations: <strong>{violations_summary.get('total_violations', 0)}</strong></p>
                    <p>Affected Employees: <strong>{violations_summary.get('affected_employees', 0)}</strong></p>
                    <h3>Violations:</h3>
                    <ul>
                        {violations_list if violations_list else '<li>No violations recorded today</li>'}
                    </ul>
                </body>
            </html>
            """
            
            return self.send_email(manager_email, subject, html_body, is_html=True)
            
        except Exception as e:
            logger.error(f"Error sending daily summary: {str(e)}")
            return False


if __name__ == "__main__":
    # Test the notifier
    notifier = EmailNotifier()
    test_violation = {
        'employee_id': 'EMP001',
        'employee_name': 'John Doe',
        'violation_type': 'Crossed at non-zebra crossing',
        'location': 'Main Street, Intersection 5',
        'timestamp': datetime.now().isoformat(),
        'severity': 'HIGH',
        'description': 'Employee crossed the road without checking surroundings and not at designated zebra crossing'
    }
    
    test_email = "manager@example.com"
    result = notifier.send_violation_alert(test_email, test_violation)
    print(f"Email send result: {result}")
