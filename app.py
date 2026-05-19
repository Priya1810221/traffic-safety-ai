# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
from datetime import datetime
from notifications import EmailNotifier
from data_generator import ViolationDataGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
email_notifier = EmailNotifier()
data_generator = ViolationDataGenerator()
violation_queue = []

# Store active monitors
monitors = {}
monitoring_active = False


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'monitoring_active': monitoring_active
    })


@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    """Start real-time monitoring for employees"""
    global monitoring_active
    try:
        data = request.json
        employee_ids = data.get('employee_ids', [])
        manager_email = data.get('manager_email')
        check_interval = data.get('check_interval', 5)  # seconds
        
        if not employee_ids or not manager_email:
            return jsonify({'error': 'Missing employee_ids or manager_email'}), 400
        
        # Start monitoring in a background thread
        if not monitoring_active:
            monitoring_active = True
            monitor_thread = threading.Thread(
                target=monitor_violations,
                args=(employee_ids, manager_email, check_interval)
            )
            monitor_thread.daemon = True
            monitor_thread.start()
            
            logger.info(f"Started monitoring for employees: {employee_ids}")
            return jsonify({
                'message': 'Monitoring started successfully',
                'employee_ids': employee_ids,
                'manager_email': manager_email,
                'timestamp': datetime.now().isoformat()
            }), 200
        else:
            return jsonify({'message': 'Monitoring already active'}), 200
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    """Stop real-time monitoring"""
    global monitoring_active
    monitoring_active = False
    logger.info("Monitoring stopped")
    return jsonify({'message': 'Monitoring stopped', 'timestamp': datetime.now().isoformat()}), 200


@app.route('/api/violations', methods=['GET'])
def get_violations():
    """Retrieve all recorded violations"""
    return jsonify({
        'total_violations': len(violation_queue),
        'violations': violation_queue,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/violations/<employee_id>', methods=['GET'])
def get_employee_violations(employee_id):
    """Retrieve violations for a specific employee"""
    employee_violations = [v for v in violation_queue if v['employee_id'] == employee_id]
    return jsonify({
        'employee_id': employee_id,
        'total_violations': len(employee_violations),
        'violations': employee_violations,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/clear-violations', methods=['DELETE'])
def clear_violations():
    """Clear all recorded violations"""
    global violation_queue
    violation_queue = []
    logger.info("Violation queue cleared")
    return jsonify({'message': 'All violations cleared', 'timestamp': datetime.now().isoformat()}), 200


def monitor_violations(employee_ids, manager_email, check_interval):
    """Monitor employees for traffic violations in real-time"""
    global monitoring_active, violation_queue
    
    logger.info(f"Monitoring thread started for {len(employee_ids)} employees")
    
    while monitoring_active:
        try:
            for employee_id in employee_ids:
                # Generate random violation data
                violation = data_generator.generate_violation(employee_id)
                
                if violation:
                    violation_queue.append(violation)
                    logger.warning(f"VIOLATION DETECTED: {violation}")
                    
                    # Send notification email in real-time
                    send_notification(
                        manager_email=manager_email,
                        violation=violation,
                        employee_id=employee_id
                    )
            
            # Wait for the specified interval before next check
            time.sleep(check_interval)
        except Exception as e:
            logger.error(f"Error in monitoring loop: {str(e)}")
            time.sleep(check_interval)
    
    logger.info("Monitoring thread stopped")


def send_notification(manager_email, violation, employee_id):
    """Send notification to manager"""
    try:
        subject = f"ALERT: Traffic Rule Violation - Employee {employee_id}"
        body = f"""
        TRAFFIC SAFETY ALERT
        ====================
        
        Employee ID: {violation['employee_id']}
        Violation Type: {violation['violation_type']}
        Description: {violation['description']}
        Timestamp: {violation['timestamp']}
        Location: {violation['location']}
        Severity: {violation['severity']}
        
        Action Required: Please review this violation and take appropriate action.
        
        ---
        This is an automated message from the Traffic Safety Monitoring System.
        """
        
        email_notifier.send_email(
            to_email=manager_email,
            subject=subject,
            body=body
        )
        
        logger.info(f"Notification sent to {manager_email} for employee {employee_id}")
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")


if __name__ == '__main__':
    logger.info("Starting Traffic Safety Notification System")
    app.run(debug=True, host='0.0.0.0', port=5000)
