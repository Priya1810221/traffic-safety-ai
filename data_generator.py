# data_generator.py
import random
from datetime import datetime, timedelta
import json

class ViolationDataGenerator:
    """Generates random traffic violation data for testing and simulation"""
    
    def __init__(self):
        # Sample employee data
        self.employees = [
            {'id': 'EMP001', 'name': 'Rajesh Kumar', 'department': 'Sales'},
            {'id': 'EMP002', 'name': 'Priya Singh', 'department': 'HR'},
            {'id': 'EMP003', 'name': 'Amit Patel', 'department': 'IT'},
            {'id': 'EMP004', 'name': 'Neha Gupta', 'department': 'Marketing'},
            {'id': 'EMP005', 'name': 'Vikram Desai', 'department': 'Finance'},
            {'id': 'EMP006', 'name': 'Anjali Verma', 'department': 'Operations'},
            {'id': 'EMP007', 'name': 'Rohan Sharma', 'department': 'Sales'},
            {'id': 'EMP008', 'name': 'Divya Kapoor', 'department': 'IT'},
        ]
        
        # Traffic rule violations
        self.violation_types = [
            'No Left Check Before Crossing',
            'No Right Check Before Crossing',
            'No Front Check Before Crossing',
            'Crossed Road Without Zebra Crossing',
            'Not Following Signal at Zebra Crossing',
            'Jaywalking',
            'Running Across Road',
            'Distracted Crossing (Using Phone)'
        ]
        
        # Common locations
        self.locations = [
            'Main Gate Zebra Crossing',
            'Office Building Front Road',
            'Parking Lot Exit',
            'Metro Station Entrance',
            'Shopping Mall Crossing',
            'Highway Intersection',
            'Street Market Crossing',
            'Bus Stop Area',
            'Railway Station Crossing',
            'Park Entrance'
        ]
        
        # Severity levels
        self.severity_levels = ['Low', 'Medium', 'High']
        
        # Descriptions for violations
        self.violation_descriptions = {
            'No Left Check Before Crossing': 'Employee did not look to the left before crossing the road.',
            'No Right Check Before Crossing': 'Employee did not look to the right before crossing the road.',
            'No Front Check Before Crossing': 'Employee did not check for incoming traffic from the front.',
            'Crossed Road Without Zebra Crossing': 'Employee crossed the road at a location other than designated zebra crossing.',
            'Not Following Signal at Zebra Crossing': 'Employee crossed during red signal at zebra crossing.',
            'Jaywalking': 'Employee crossed the road illegally at an unauthorized location.',
            'Running Across Road': 'Employee ran across the road instead of walking safely.',
            'Distracted Crossing (Using Phone)': 'Employee was using phone/distracted while crossing the road.'
        }
    
    def generate_violation(self, employee_id=None):
        """Generate a random violation with 30% probability"""
        # 70% chance of no violation, 30% chance of violation
        if random.random() > 0.3:
            return None
        
        # Select random employee if not specified
        if employee_id:
            employee = next((e for e in self.employees if e['id'] == employee_id), None)
            if not employee:
                employee = random.choice(self.employees)
        else:
            employee = random.choice(self.employees)
        
        # Select random violation type
        violation_type = random.choice(self.violation_types)
        
        # Determine severity based on violation type
        if 'Without Zebra' in violation_type or 'Signal' in violation_type or 'Jaywalking' in violation_type:
            severity = random.choice(['Medium', 'High'])
        elif 'Running' in violation_type or 'Distracted' in violation_type:
            severity = random.choice(['Low', 'Medium'])
        else:
            severity = 'Low'
        
        # Create violation record
        violation = {
            'employee_id': employee['id'],
            'employee_name': employee['name'],
            'department': employee['department'],
            'violation_type': violation_type,
            'location': random.choice(self.locations),
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
            'description': self.violation_descriptions[violation_type],
            'violation_id': f"VIO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
        }
        
        return violation
    
    def generate_batch_violations(self, count=10):
        """Generate multiple violations for batch testing"""
        violations = []
        for i in range(count):
            violation = self.generate_violation()
            if violation:
                violations.append(violation)
        return violations
    
    def get_all_employees(self):
        """Return list of all employees for reference"""
        return self.employees
    
    def get_employee_by_id(self, employee_id):
        """Get employee details by ID"""
        return next((e for e in self.employees if e['id'] == employee_id), None)
    
    def export_violations_to_json(self, violations, filename='violations.json'):
        """Export violations to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(violations, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting violations: {str(e)}")
            return False


# Test the data generator
if __name__ == '__main__':
    generator = ViolationDataGenerator()
    
    print("=" * 60)
    print("Traffic Violation Data Generator - Sample Output")
    print("=" * 60)
    
    # Show all employees
    print("\n--- All Employees ---")
    for emp in generator.get_all_employees():
        print(f"{emp['id']}: {emp['name']} ({emp['department']})")
    
    # Generate sample violations
    print("\n--- Sample Violations ---")
    violations = generator.generate_batch_violations(5)
    for v in violations:
        if v:
            print(f"\nViolation ID: {v['violation_id']}")
            print(f"Employee: {v['employee_name']} ({v['employee_id']})")
            print(f"Type: {v['violation_type']}")
            print(f"Location: {v['location']}")
            print(f"Severity: {v['severity']}")
            print(f"Time: {v['timestamp']}")
            print(f"Description: {v['description']}")
            print("-" * 40)
