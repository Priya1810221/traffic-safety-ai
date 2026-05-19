# Traffic Safety AI System - CSV Templates

## Overview
This directory contains CSV templates for managing employee data and violation records in the Traffic Safety AI System.

## Files

### 1. employees.csv
Contains employee information for the organization.

**Columns:**
- `employee_id`: Unique identifier for the employee (e.g., EMP001)
- `employee_name`: Full name of the employee
- `department`: Department the employee belongs to
- `manager_email`: Email address of the employee's manager (for notifications)
- `phone_number`: Contact phone number of the employee
- `date_of_joining`: Date when the employee joined the organization

**Usage:**
This file is used to:
- Link employees to their managers for violation notifications
- Track employee information
- Generate reports by department

### 2. violations_sample.csv
Sample violation records for reference and testing.

**Columns:**
- `violation_id`: Unique identifier for each violation
- `employee_id`: ID of the employee who committed the violation
- `employee_name`: Name of the employee
- `violation_type`: Type of traffic rule violation
- `location`: Where the violation occurred
- `severity`: Level of severity (Low, Medium, High)
- `timestamp`: Date and time of the violation
- `description`: Detailed description of the violation
- `manager_email`: Email of the manager to notify

**Usage:**
This file serves as:
- A template for violation records
- Sample data for testing the system
- Reference for violation categorization

## How to Use

1. **Update employees.csv** with your organization's actual employee data
2. **Import employees.csv** into the application database
3. The system will automatically generate violation records when detected
4. Violation records can be exported and analyzed using the provided tools

## Violation Types

The system recognizes the following violation types:
- No Left Check Before Crossing
- No Right Check Before Crossing
- No Front Check Before Crossing
- Crossed Road Without Zebra Crossing
- Not Following Signal at Zebra Crossing
- Jaywalking
- Running Across Road
- Distracted Crossing (Using Phone)

## Severity Levels

- **Low**: Minor safety concerns
- **Medium**: Moderate risk violations
- **High**: Critical safety violations requiring immediate action

## Notes

- Ensure all email addresses are valid
- Date format: YYYY-MM-DD
- Employee IDs must be unique
- Keep backups of your CSV files
