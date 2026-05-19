# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Email settings
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    
    # Monitoring settings
    VIOLATION_CHECK_INTERVAL = 10  # seconds
    VIOLATION_PROBABILITY = 0.3  # 30% chance of violation in each check
    
    # Data settings
    EMPLOYEES_CSV = 'data/employees.csv'
    VIOLATIONS_CSV = 'data/violations_export.csv'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    VIOLATION_PROBABILITY = 0.8  # Higher probability for testing

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    VIOLATION_CHECK_INTERVAL = 5  # seconds (faster in production)

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'testing':
        return TestingConfig()
    elif env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()
