import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    # Railway provides DATABASE_URL for PostgreSQL
    # Falls back to SQLite for local development
    _db_url = os.environ.get('DATABASE_URL')
    
    # Clean up the URL if it exists
    if _db_url:
        _db_url = _db_url.strip()  # Remove whitespace
        _db_url = _db_url.strip("'").strip('"')  # Remove accidental quotes
        
    SQLALCHEMY_DATABASE_URI = _db_url or 'sqlite:///app.db'
    
    # Fix for Railway's postgres:// vs postgresql:// issue
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)

    print(f"[{'Production' if os.environ.get('FLASK_ENV') == 'production' else 'Dev'}] Configured Database URI: {SQLALCHEMY_DATABASE_URI.split('@')[-1] if '@' in SQLALCHEMY_DATABASE_URI else 'sqlite/local'}")

    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Brevo Email Configuration
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL') or 'noreply@tmes.com'
    SENDER_NAME = os.environ.get('SENDER_NAME') or 'TMES IIT Kharagpur'
    
    # OTP Configuration
    OTP_EXPIRY_MINUTES = 10
    
    # Razorpay Configuration
    RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID') or 'rzp_test_xxxxxxxxxxxx'
    RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET') or 'your_razorpay_secret'
    
    # Great Step Registration Fee (in paise, 100 paise = 1 INR)
    GREATSTEP_REGISTRATION_FEE = int(os.environ.get('GREATSTEP_REGISTRATION_FEE', 50000))  # Default: ₹500
    
    # Main Admin Email (Protected)
    MAIN_ADMIN_EMAIL = os.environ.get('MAIN_ADMIN_EMAIL')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
