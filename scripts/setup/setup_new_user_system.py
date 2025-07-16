#!/usr/bin/env python3
"""
Setup script for new user system (no demo user)
"""

import sys
import os
import subprocess
import time

def remove_demo_user():
    """Remove demo user from database"""
    print("🧹 Removing demo user...")
    try:
        sys.path.append('backend')
        from app import create_app
        from models import db, User
        
        app = create_app()
        
        with app.app_context():
            demo_user = User.query.filter_by(username='demo').first()
            
            if demo_user:
                db.session.delete(demo_user)
                db.session.commit()
                print("✅ Demo user removed")
            else:
                print("ℹ️  No demo user found")
            
            users = User.query.all()
            print(f"👥 Users in database: {len(users)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_backend_health():
    """Test if backend is healthy"""
    print("\n🏥 Testing backend health...")
    try:
        import requests
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend returned {response.status_code}")
    except:
        print("❌ Backend not responding")
    return False

def create_test_user():
    """Create a test user to verify system works"""
    print("\n👤 Creating test user...")
    try:
        import requests
        import random
        import string
        
        # Generate random user
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        user_data = {
            "username": f"testuser_{random_id}",
            "email": f"test_{random_id}@example.com",
            "password": "testpass123"
        }
        
        # Register user
        response = requests.post("http://localhost:5000/api/auth/register", json=user_data)
        
        if response.status_code == 201:
            print(f"✅ Test user created: {user_data['username']}")
            
            # Test login
            login_data = {
                "usernameOrEmail": user_data["username"],
                "password": user_data["password"]
            }
            
            login_response = requests.post("http://localhost:5000/api/auth/login", json=login_data)
            
            if login_response.status_code == 200:
                print("✅ Test user can login")
                return True
            else:
                print("❌ Test user cannot login")
        else:
            print(f"❌ Failed to create test user: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
    
    return False

def main():
    """Main setup function"""
    print("🎯 Setting Up New User System")
    print("=" * 50)
    
    # Step 1: Remove demo user
    remove_demo_user()
    
    # Step 2: Check if backend is running
    if not test_backend_health():
        print("\n💡 Start backend with:")
        print("   cd backend && python run.py")
        print("\nThen run this script again to test user creation.")
        return
    
    # Step 3: Test user creation
    if create_test_user():
        print("\n🎉 New user system is working!")
        print("\n📋 Next steps:")
        print("1. Go to http://localhost:5173")
        print("2. Click 'Register' to create your account")
        print("3. Sign in and start using SMS Guard")
    else:
        print("\n💥 User creation test failed")
        print("Check backend logs for errors")

if __name__ == "__main__":
    main()
