#!/usr/bin/env python3
"""
Fix database and test password reset
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models import db, User, PasswordResetToken
import requests
import json

def fix_database():
    """Create database tables and test"""
    print("🔧 Fixing Database...")
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if user exists
        user = User.query.filter_by(email="ogboifavourifeanyichukwu@gmail.com").first()
        if user:
            print(f"✅ User found: {user.username}")
            
            # Create a test token
            reset_token = PasswordResetToken.create_for_user(user, hours_valid=1)
            print(f"✅ Test token created: {reset_token.token[:20]}...")
            
            # Test the token
            test_reset_password(reset_token.token)
        else:
            print("❌ User not found")

def test_reset_password(token):
    """Test reset password with token"""
    print(f"\n🧪 Testing Reset Password")
    print(f"🎫 Token: {token[:20]}...")
    
    test_data = {
        "token": token,
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/auth/reset-password",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Password reset successful!")
        else:
            print("❌ Password reset failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔐 Database Fix and Test")
    print("=" * 30)
    fix_database()
