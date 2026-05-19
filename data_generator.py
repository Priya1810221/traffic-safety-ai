# data_generator.py
import random
from datetime import datetime, timedelta
import csv
import json
import logging

logger = logging.getLogger(__name__)

class ViolationDataGenerator:
    """Generates random traffic violation data for testing and simulation"""
    
    VIOLATION_TYPES = [
        'No Left Check Before Crossing',
        'No Right Check Before Crossing',
        'No Front Check Before Crossing',
        'Crossed Road Without Zebra Crossing',
        'Not Following Signal at Zebra Crossing',
        'Jaywalking',
        'Running Across Road',
        'Distracted Crossing (Using Phone)'
    ]
    
    LOCATIONS = [
        'Main Gate Zebra Crossing',
        'Office Building Front Road',
        'Parking Lot Exit',
        'Metro Station Entrance',
        'Shopping Mall Crossing',
        'Highway Intersection',
        'Street Market Crossing',
        'Bus Stop Area',
        'Traffic Signal Junction',
        'Pedestrian Overpass'
    ]
    
    SEVERITY_LEVELS = ['Low', 'Medium', 'High']
    
    def __init__(self):
        self.violation_counter = 0
        self.employees = self._load_employees()
    
    def _load_employees(self):
        """Load employee data from CSV"""
        employees = []
        try:
            with open('data/employees.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(row)
            logger.info(f"Loaded {len(employees)} employees from CSV")
        except FileNotFoundError:
            logger.warning("employees.csv not found. Using default sample data.")
            employees = self._get_sample_employees()
        return employees
    
    def _get_sample_employees(self):
        """Get sample employee data"""
        return [
            {'employee_id': 'EMP001', 'employee_name': 'Rajesh Kumar', 'manager_email': 'manager1@company.com'},
            {'employee_id': 'EMP002', 'employee_name': 'Priya Singh', 'manager_email': 'manager2@company.com'},
            {'employee_id': 'EMP003', 'employee_name': 'Amit Patel', 'manager_email': 'manager3@company.com'},
            {'employee_id': 'EMP004', 'employee_name': 'Neha Gupta', 'manager_email': 'manager4@company.com'},
            {'employee_id': 'EMP005', 'employee_name': 'Vikram Desai', 'manager_email': 'manager5@company.com'},
        ]
    
    def generate_violation(self, employee_id, probability=0.3):
        """Generate a random violation with given probability"""
        # Random probability to generate violation
        if random.random() > probability:
            return None
        
        # Find employee details
        employee = next((e for e in self.employees if e.get('employee_id') == employee_id), None)
        if not employee:
            logger.warning(f"Employee {employee_id} not found")
            return None
        
        self.violation_counter += 1
        timestamp = datetime.now() - timedelta(seconds=random.randint(0, 3600))
        
        violation = {
            'violation_id': f"VIO-{timestamp.strftime('%Y%m%d%H%M%S')}-{self.violation_counter:04d}",
            'employee_id': employee_id,
            'employee_name': employee.get('employee_name'),
            'violation_type': random.choice(self.VIOLATION_TYPES),
            'location': random.choice(self.LOCATIONS),
            'severity': random.choice(self.SEVERITY_LEVELS),
            'timestamp': timestamp.isoformat(),
            'description': self._generate_description(),
            'manager_email': employee.get('manager_email')
        }
        
        logger.info(f"Generated violation: {violation['violation_id']}")
        return violation
    
    def _generate_description(self):
        """Generate description for violation"""
        descriptions = [
            'Employee crossed the road without looking both ways.',
            'Employee crossed at unauthorized location.',
            'Employee did not wait for green signal.',
            'Employee was distracted while crossing.',
            'Employee ran across the road unsafely.',
            'Employee ignored zebra crossing signals.',
        ]
        return random.choice(descriptions)
    
    def generate_batch_violations(self, num_violations=10):
        """Generate multiple random violations for testing"""
        violations = []
        for _ in range(num_violations):
            employee = random.choice(self.employees)
            violation = self.generate_violation(employee.get('employee_id'))
            if violation:
                violations.append(violation)
        return violations
    
    def export_violations_to_json(self, violations, filename='violations_export.json'):
        """Export violations to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(violations, f, indent=2)
            logger.info(f"Exported {len(violations)} violations to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting violations: {str(e)}")
            return False
    
    def export_violations_to_csv(self, violations, filename='violations_export.csv'):
        """Export violations to CSV file"""
        try:
            if not violations:
                logger.warning("No violations to export")
                return False
            
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=violations[0].keys())
                writer.writeheader()
                writer.writerows(violations)
            logger.info(f"Exported {len(violations)} violations to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting violations to CSV: {str(e)}")
            return False
    
    def get_all_employees(self):
        """Return all employees"""
        return self.employees
    
    def get_employee(self, employee_id):
        """Get specific employee details"""
        return next((e for e in self.employees if e.get('employee_id') == employee_id), None)
