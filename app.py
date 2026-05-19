# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import json
from datetime import datetime
from notifications import EmailNotifier
from data_generator import ViolationDataGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
email_notifier = EmailNotifier()
data_generator = ViolationDataGenerator()
violation_queue = []

# Store active monitors
monitors = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    """Start real-time monitoring for an employee"""
    try:
        data = request.json
        employee_id = data.get('employee_id')
        manager_email = data.get('manager_email')
        
        if not employee_id or not manager_email:
            return jsonify({'error': 'employee_id and manager_email are required'}), 400
        
        # Start monitoring thread
        if employee_id not in monitors:
            thread = threading.Thread(
                target=monitor_employee,
                args=(employee_id, manager_email),
                daemon=True
            )
            monitors[employee_id] = {
                'thread': thread,
                'active': True,
                'manager_email': manager_email,
                'start_time': datetime.now().isoformat()
            }
            thread.start()
            logger.info(f"Started monitoring for employee {employee_id}")
            return jsonify({
                'message': f'Monitoring started for employee {employee_id}',
                'employee_id': employee_id
            }), 200
        else:
            return jsonify({'error': 'Already monitoring this employee'}), 400
            
    except Exception as e:
        logger.error(f"Error starting monitoring: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stop-monitoring/<employee_id>', methods=['POST'])
def stop_monitoring(employee_id):
    """Stop real-time monitoring for an employee"""
    try:
        if employee_id in monitors:
            monitors[employee_id]['active'] = False
            del monitors[employee_id]
            logger.info(f"Stopped monitoring for employee {employee_id}")
            return jsonify({'message': f'Monitoring stopped for employee {employee_id}'}), 200
        else:
            return jsonify({'error': 'Employee not being monitored'}), 404
            
    except Exception as e:
        logger.error(f"Error stopping monitoring: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/violations', methods=['GET'])
def get_violations():
    """Get all recorded violations"""
    try:
        return jsonify({
            'total_violations': len(violation_queue),
            'violations': violation_queue[-50:]  # Return last 50 violations
        }), 200
    except Exception as e:
        logger.error(f"Error fetching violations: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/violations/<employee_id>', methods=['GET'])
def get_employee_violations(employee_id):
    """Get violations for a specific employee"""
    try:
        employee_violations = [v for v in violation_queue if v['employee_id'] == employee_id]
        return jsonify({
            'employee_id': employee_id,
            'total_violations': len(employee_violations),
            'violations': employee_violations
        }), 200
    except Exception as e:
        logger.error(f"Error fetching employee violations: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/monitoring-status', methods=['GET'])
def get_monitoring_status():
    """Get status of all active monitors"""
    try:
        status = {}
        for emp_id, monitor_info in monitors.items():
            status[emp_id] = {
                'active': monitor_info['active'],
                'manager_email': monitor_info['manager_email'],
                'start_time': monitor_info['start_time']
            }
        return jsonify({
            'active_monitors': len(status),
            'monitors': status
        }), 200
    except Exception as e:
        logger.error(f"Error fetching monitoring status: {str(e)}")
        return jsonify({'error': str(e)}), 500


def monitor_employee(employee_id, manager_email):
    """Monitor employee for traffic violations in real-time"""
    logger.info(f"Starting real-time monitoring for employee {employee_id}")
    
    while monitors.get(employee_id, {}).get('active', False):
        try:
            # Generate random violation data
            violation = data_generator.generate_violation(employee_id)
            
            if violation:
                # Add to violation queue
                violation_queue.append(violation)
                logger.warning(f"Violation detected for {employee_id}: {violation['violation_type']}")
                
                # Send email notification to manager
                email_subject = f"⚠️ Traffic Safety Alert: Employee {employee_id} Violation Detected"
                email_body = f"""
Dear Manager,

A traffic rule violation has been detected:

Employee ID: {violation['employee_id']}
Employee Name: {violation['employee_name']}
Violation Type: {violation['violation_type']}
Location: {violation['location']}
Timestamp: {violation['timestamp']}
Severity: {violation['severity']}
Description: {violation['description']}

Please take appropriate action.

Best regards,
Traffic Safety AI System
                """
                
                email_notifier.send_email(
                    to_email=manager_email,
                    subject=email_subject,
                    body=email_body
                )
                logger.info(f"Notification email sent to {manager_email}")
            
            # Sleep for 10 seconds before checking next violation
            time.sleep(10)
            
        except Exception as e:
            logger.error(f"Error in monitoring thread for {employee_id}: {str(e)}")
            time.sleep(5)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
