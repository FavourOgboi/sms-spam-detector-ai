#!/usr/bin/env python3
"""
Debug Password Reset API
Quick test to verify the API endpoints are working correctly
"""

import requests
import json

BACKEND_URL = "http://localhost:5000"

def test_forgot_password():
    """Test forgot password endpoint"""
    print("🧪 Testing Forgot Password API")
    print("-" * 40)
    
    # Test with the newly registered user
    test_data = {
        "email": "ogboifavourifeanyichukwu@gmail.com"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/forgot-password",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📤 Request: {json.dumps(test_data, indent=2)}")
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") and response_data.get("resetLink"):
                reset_link = response_data["resetLink"]
                print(f"🔗 Reset Link: {reset_link}")
                
                # Extract token
                if "token=" in reset_link:
                    token = reset_link.split("token=")[1]
                    print(f"🎫 Token: {token[:20]}...")
                    
                    # Test reset password
                    test_reset_password(token)
                    
        return response.json()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_reset_password(token):
    """Test reset password endpoint"""
    print("\n🔑 Testing Reset Password API")
    print("-" * 40)
    
    test_data = {
        "token": token,
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/reset-password",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📤 Request: {json.dumps({'token': token[:20] + '...', 'password': '***'}, indent=2)}")
        print(f"📥 Status Code: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        return response.json()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_backend_health():
    """Test backend health"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Password Reset API Debug Tool")
    print("=" * 50)
    
    if test_backend_health():
        print()
        test_forgot_password()
    else:
        print("\n💡 Make sure backend is running: python backend/app.py")
