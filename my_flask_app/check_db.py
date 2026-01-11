#!/usr/bin/env python
"""Quick script to check database contents"""
import os
import sys

# Add the app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from app.models import User, PendingRegistration

with app.app_context():
    print("=== USERS ===")
    users = User.query.all()
    if not users:
        print("  No users found!")
    for u in users:
        print(f"  ID: {u.id}, Email: {u.email}, Verified: {u.is_verified}")
        print(f"    Password Hash: {u.password_hash[:50]}..." if u.password_hash else "    No password hash!")
    
    print("\n=== PENDING REGISTRATIONS ===")
    pendings = PendingRegistration.query.all()
    if not pendings:
        print("  No pending registrations!")
    for p in pendings:
        print(f"  ID: {p.id}, Email: {p.email}, OTP: {p.otp_code}")
        print(f"    Password Hash: {p.password_hash[:50]}..." if p.password_hash else "    No password hash!")
