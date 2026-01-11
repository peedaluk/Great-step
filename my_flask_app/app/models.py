from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user data"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Profile info (to be filled after registration)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    college = db.Column(db.String(200))
    year = db.Column(db.String(20))
    
    # Account status
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_greatstep_registered = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    otps = db.relationship('OTP', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class OTP(db.Model):
    """OTP model for email verification and login"""
    __tablename__ = 'otps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(20), nullable=False)  # 'registration', 'login', 'reset_password'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    
    @staticmethod
    def generate_code():
        """Generate a 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def create_otp(cls, user_id, purpose, expiry_minutes=10):
        """Create a new OTP for a user"""
        # Invalidate any existing OTPs for this user and purpose
        cls.query.filter_by(
            user_id=user_id, 
            purpose=purpose, 
            is_used=False
        ).update({'is_used': True})
        
        otp = cls(
            user_id=user_id,
            code=cls.generate_code(),
            purpose=purpose,
            expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes)
        )
        db.session.add(otp)
        db.session.commit()
        return otp
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_used and datetime.utcnow() < self.expires_at
    
    def use(self):
        """Mark OTP as used"""
        self.is_used = True
        db.session.commit()
    
    def __repr__(self):
        return f'<OTP {self.code} for user {self.user_id}>'


class PendingRegistration(db.Model):
    """Temporary storage for users who haven't verified email yet"""
    __tablename__ = 'pending_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    
    # Profile info
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    mobile = db.Column(db.String(15))
    college = db.Column(db.String(200))
    year = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = generate_password_hash(password)
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP code"""
        return ''.join(random.choices(string.digits, k=6))
    
    @classmethod
    def create(cls, email, password, first_name=None, last_name=None, mobile=None, college=None, year=None, expiry_minutes=10):
        """Create a new pending registration"""
        # Remove any existing pending registration for this email
        cls.query.filter_by(email=email).delete()
        
        pending = cls(
            email=email,
            otp_code=cls.generate_otp(),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            college=college,
            year=year,
            expires_at=datetime.utcnow() + timedelta(minutes=expiry_minutes)
        )
        pending.set_password(password)
        db.session.add(pending)
        db.session.commit()
        return pending
    
    def is_valid(self):
        """Check if pending registration is still valid"""
        return datetime.utcnow() < self.expires_at
    
    def __repr__(self):
        return f'<PendingRegistration {self.email}>'


class GreatStepRegistration(db.Model):
    """Standalone table for Great Step event registrations (not linked to User table)"""
    __tablename__ = 'greatstep_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User details (stored independently)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    college = db.Column(db.String(200), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    
    # Payment details
    razorpay_order_id = db.Column(db.String(100), nullable=False)
    razorpay_payment_id = db.Column(db.String(100))
    razorpay_signature = db.Column(db.String(256))
    amount_paid = db.Column(db.Integer, nullable=False)  # Amount in paise
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    payment_completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<GreatStepRegistration {self.email} - {self.payment_status}>'
