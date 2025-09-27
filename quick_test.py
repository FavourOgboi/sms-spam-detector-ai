#!/usr/bin/env python3
"""
Quick test to reproduce the exact issue
"""

import requests
import json

def test_reset_with_token():
    """Test with the exact token from the frontend logs"""
    
    # The token from your frontend logs
    token = "Im9nYm9pZmF2b3VyaWZlYW55aWNodWt3dUBnbWFpbC5jb20"  # This is the token you showed
    
    print("🧪 Testing Reset Password with Exact Token")
    print(f"🎫 Token: {token}")
    
    # Test data exactly like frontend sends
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
        
        print(f"📤 Request: {json.dumps(test_data, indent=2)}")
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("❌ 400 Error - This matches what you're seeing!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_fresh_token():
    """Get a fresh token and test immediately"""
    
    print("\n🔄 Getting Fresh Token...")
    
    # First get a fresh token
    forgot_data = {"email": "ogboifavourifeanyichukwu@gmail.com"}
    
    try:
        forgot_response = requests.post(
            "http://localhost:5000/api/auth/forgot-password",
            json=forgot_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if forgot_response.status_code == 200:
            forgot_result = forgot_response.json()
            if forgot_result.get("resetLink"):
                reset_link = forgot_result["resetLink"]
                if "token=" in reset_link:
                    fresh_token = reset_link.split("token=")[1]
                    print(f"🎫 Fresh Token: {fresh_token[:20]}...")
                    
                    # Test with fresh token
                    reset_data = {
                        "token": fresh_token,
                        "password": "FreshPassword123!"
                    }
                    
                    reset_response = requests.post(
                        "http://localhost:5000/api/auth/reset-password",
                        json=reset_data,
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    
                    print(f"📥 Fresh Token Status: {reset_response.status_code}")
                    print(f"📥 Fresh Token Response: {json.dumps(reset_response.json(), indent=2)}")
                    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔐 Quick Password Reset Test")
    print("=" * 40)
    
    # Test with the exact token from frontend
    test_reset_with_token()
    
    # Test with fresh token
    test_fresh_token()
