#!/usr/bin/env python3
"""
Complete Password Reset System Test
Tests the full password reset flow from request to completion
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:5173"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "NewPassword123!"

def test_password_reset_flow():
    """Test the complete password reset flow"""
    print("🧪 Testing Complete Password Reset System")
    print("=" * 50)
    
    # Step 1: Test forgot password endpoint
    print("\n1️⃣ Testing Forgot Password Request")
    print("-" * 30)
    
    forgot_data = {"email": TEST_EMAIL}
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/auth/forgot-password",
            json=forgot_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📤 Request: POST /api/auth/forgot-password")
        print(f"📤 Data: {json.dumps(forgot_data, indent=2)}")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                print("✅ Forgot password request successful!")
                
                # Extract reset link if available (development mode)
                reset_link = response_data.get("resetLink")
                if reset_link:
                    print(f"🔗 Reset link: {reset_link}")
                    
                    # Extract token from reset link
                    if "token=" in reset_link:
                        token = reset_link.split("token=")[1].split("&")[0]
                        print(f"🎫 Extracted token: {token[:20]}...")
                        
                        # Step 2: Test reset password endpoint
                        print("\n2️⃣ Testing Password Reset")
                        print("-" * 30)
                        
                        reset_data = {
                            "token": token,
                            "password": TEST_PASSWORD
                        }
                        
                        # Wait a moment to simulate user action
                        time.sleep(1)
                        
                        reset_response = requests.post(
                            f"{BACKEND_URL}/api/auth/reset-password",
                            json=reset_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        print(f"📤 Request: POST /api/auth/reset-password")
                        print(f"📤 Data: {json.dumps({'token': token[:20] + '...', 'password': '***'}, indent=2)}")
                        print(f"📥 Status: {reset_response.status_code}")
                        print(f"📥 Response: {json.dumps(reset_response.json(), indent=2)}")
                        
                        if reset_response.status_code == 200:
                            reset_response_data = reset_response.json()
                            if reset_response_data.get("success"):
                                print("✅ Password reset successful!")
                                
                                # Step 3: Test token reuse (should fail)
                                print("\n3️⃣ Testing Token Reuse Prevention")
                                print("-" * 30)
                                
                                reuse_response = requests.post(
                                    f"{BACKEND_URL}/api/auth/reset-password",
                                    json=reset_data,
                                    headers={"Content-Type": "application/json"}
                                )
                                
                                print(f"📤 Request: POST /api/auth/reset-password (reuse)")
                                print(f"📥 Status: {reuse_response.status_code}")
                                print(f"📥 Response: {json.dumps(reuse_response.json(), indent=2)}")
                                
                                if reuse_response.status_code == 400:
                                    print("✅ Token reuse prevention working!")
                                else:
                                    print("❌ Token reuse prevention failed!")
                                
                            else:
                                print(f"❌ Password reset failed: {reset_response_data.get('error')}")
                        else:
                            print(f"❌ Password reset request failed with status {reset_response.status_code}")
                    else:
                        print("❌ No token found in reset link")
                else:
                    print("ℹ️ No reset link provided (email would be sent in production)")
            else:
                print(f"❌ Forgot password failed: {response_data.get('error')}")
        else:
            print(f"❌ Forgot password request failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the backend is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Password Reset System Test Complete!")
    print("\n📋 Frontend URLs to test:")
    print(f"  🔗 Forgot Password: {FRONTEND_URL}/forgot-password")
    print(f"  🔗 Login Page: {FRONTEND_URL}/login")
    
    return True

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health")
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running! Start it with: python backend/app.py")
        return False

if __name__ == "__main__":
    print(f"🚀 Password Reset System Test")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check backend health first
    if test_backend_health():
        test_password_reset_flow()
    else:
        print("\n💡 To start the backend:")
        print("   cd backend && python app.py")
        print("\n💡 To start the frontend:")
        print("   npm run dev")
