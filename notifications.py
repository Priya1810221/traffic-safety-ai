# notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailNotifier:
    """
    Handles email notifications for traffic violations.
    Supports sending alerts to managers when employees violate traffic rules.
    """
    
    def __init__(self):
        """
        Initialize email notifier with SMTP configuration.
        
        Configuration should be set via environment variables:
        - SMTP_SERVER: SMTP server address (default: smtp.gmail.com)
        - SMTP_PORT: SMTP port (default: 587)
        - SENDER_EMAIL: Email address to send from
        - SENDER_PASSWORD: Email password or app-specific password
        """
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
        self.sender_name = os.getenv('SENDER_NAME', 'Traffic Safety AI System')
        
    def send_email(self, to_email, subject, body, is_html=False):
        """
        Send an email notification.
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject line
            body (str): Email body content
            is_html (bool): Whether the body is HTML formatted (default: False)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message container
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.sender_name} <{self.sender_email}>"
            message['To'] = to_email
            message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            # Attach body
            if is_html:
                message.attach(MIMEText(body, 'html'))
            else:
                message.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent successfully to {to_email}: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed: {str(e)}")
            logger.error("Please check your email credentials in .env file")
            return False
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_violation_alert(self, manager_email, violation_data):
        """
        Send a formatted violation alert email to the manager.
        
        Args:
            manager_email (str): Manager's email address
            violation_data (dict): Dictionary containing violation details
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = f"⚠️ Traffic Safety Alert: Violation Detected for {violation_data.get('employee_name', 'Employee')}"
            
            # Create HTML formatted email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                        <h2 style="color: #d32f2f; text-align: center;">🚨 Traffic Rule Violation Alert</h2>
                        
                        <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3>Violation Details:</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold; width: 30%;">Employee ID:</td>
                                    <td style="padding: 8px;">{violation_data.get('employee_id', 'N/A')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold;">Employee Name:</td>
                                    <td style="padding: 8px;">{violation_data.get('employee_name', 'N/A')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold;">Violation Type:</td>
                                    <td style="padding: 8px;">{violation_data.get('violation_type', 'N/A')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold;">Location:</td>
                                    <td style="padding: 8px;">{violation_data.get('location', 'N/A')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold;">Timestamp:</td>
                                    <td style="padding: 8px;">{violation_data.get('timestamp', 'N/A')}</td>
                                </tr>
                                <tr style="border-bottom: 1px solid #ddd;">
                                    <td style="padding: 8px; font-weight: bold;">Severity:</td>
                                    <td style="padding: 8px;">
                                        <span style="background-color: {'#ff5252' if violation_data.get('severity') == 'High' else '#ff9800' if violation_data.get('severity') == 'Medium' else '#4caf50'}; color: white; padding: 3px 8px; border-radius: 3px;">
                                            {violation_data.get('severity', 'N/A')}
                                        </span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; font-weight: bold; vertical-align: top;">Description:</td>
                                    <td style="padding: 8px;">{violation_data.get('description', 'N/A')}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #ffc107;">
                            <p><strong>Action Required:</strong></p>
                            <p>Please review this violation and take appropriate corrective action with the employee. Repeated violations may require further disciplinary measures.</p>
                        </div>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #666; text-align: center;">
                            This is an automated alert from the Traffic Safety AI System.<br>
                            Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return self.send_email(manager_email, subject, html_body, is_html=True)
            
        except Exception as e:
            logger.error(f"Failed to send violation alert: {str(e)}")
            return False
    
    def send_daily_summary(self, manager_email, violations_list):
        """
        Send a daily summary of all violations to the manager.
        
        Args:
            manager_email (str): Manager's email address
            violations_list (list): List of violation dictionaries
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            if not violations_list:
                subject = "✅ Daily Traffic Safety Report: No Violations"
                body = "Good news! No traffic violations were detected today."
                return self.send_email(manager_email, subject, body)
            
            subject = f"📊 Daily Traffic Safety Report: {len(violations_list)} Violation(s) Detected"
            
            # Create HTML formatted summary
            violation_rows = ""
            for v in violations_list:
                violation_rows += f"""
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 8px;">{v.get('employee_name', 'N/A')}</td>
                    <td style="padding: 8px;">{v.get('violation_type', 'N/A')}</td>
                    <td style="padding: 8px;">{v.get('location', 'N/A')}</td>
                    <td style="padding: 8px;">{v.get('timestamp', 'N/A')}</td>
                    <td style="padding: 8px;">{v.get('severity', 'N/A')}</td>
                </tr>
                """
            
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                        <h2 style="color: #1976d2; text-align: center;">📊 Daily Traffic Safety Report</h2>
                        <p style="text-align: center; color: #666;">Report Date: {datetime.now().strftime('%Y-%m-%d')}</p>
                        
                        <div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Total Violations: {len(violations_list)}</strong></p>
                        </div>
                        
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <thead>
                                <tr style="background-color: #1976d2; color: white;">
                                    <th style="padding: 10px; text-align: left;">Employee Name</th>
                                    <th style="padding: 10px; text-align: left;">Violation Type</th>
                                    <th style="padding: 10px; text-align: left;">Location</th>
                                    <th style="padding: 10px; text-align: left;">Time</th>
                                    <th style="padding: 10px; text-align: left;">Severity</th>
                                </tr>
                            </thead>
                            <tbody>
                                {violation_rows}
                            </tbody>
                        </table>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #666; text-align: center;">
                            This is an automated report from the Traffic Safety AI System.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            return self.send_email(manager_email, subject, html_body, is_html=True)
            
        except Exception as e:
            logger.error(f"Failed to send daily summary: {str(e)}")
            return False


if __name__ == '__main__':
    # Test the email notifier
    notifier = EmailNotifier()
    
    # Example usage
    test_violation = {
        'employee_id': 'EMP001',
        'employee_name': 'John Doe',
        'violation_type': 'Did not check left-right-front before crossing',
        'location': 'Main Street Zebra Crossing',
        'timestamp': datetime.now().isoformat(),
        'severity': 'High',
        'description': 'Employee crossed the road without properly checking all directions at the zebra crossing.'
    }
    
    # Send test email
    # notifier.send_violation_alert('manager@example.com', test_violation)
    print("Email notifier initialized. Configure .env file and uncomment the test email line.")
