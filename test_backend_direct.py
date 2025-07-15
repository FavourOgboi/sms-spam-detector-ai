#!/usr/bin/env python3
"""
Direct backend test - bypasses frontend completely
"""
import requests
import json

def test_backend_direct():
    print("🧪 DIRECT BACKEND TEST")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing Health Endpoint...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code != 200:
            print("❌ Health check failed!")
            return False
        else:
            print("✅ Health check passed!")
            
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure backend is running on port 5000")
        return False
    
    # Test 2: Demo login
    print("\n2. Testing Demo Login...")
    try:
        login_data = {
            "usernameOrEmail": "demo",
            "password": "demo123"
        }
        
        print(f"   Sending: {json.dumps(login_data, indent=2)}")
        
        response = requests.post(
            'http://localhost:5000/api/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        print(f"   Response Body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Demo login successful!")
                token = result['data']['token']
                print(f"   Token: {token[:50]}...")
                return token
            else:
                print(f"❌ Login failed: {result.get('error')}")
                return None
        else:
            print(f"❌ Login request failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None
    
    # Test 3: Registration
    print("\n3. Testing Registration...")
    try:
        import random
        import string
        suffix = ''.join(random.choices(string.ascii_lowercase, k=4))
        
        register_data = {
            "username": f"testuser{suffix}",
            "email": f"test{suffix}@example.com",
            "password": "testpass123"
        }
        
        print(f"   Sending: {json.dumps(register_data, indent=2)}")
        
        response = requests.post(
            'http://localhost:5000/api/auth/register',
            json=register_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                print("✅ Registration successful!")
                return True
            else:
                print(f"❌ Registration failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Registration request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 INSTRUCTIONS:")
    print("1. Make sure backend is running: cd backend && python run.py")
    print("2. Run this test: python test_backend_direct.py")
    print("3. Copy ALL output and share with developer")
    print()
    
    test_backend_direct()
    
    print("\n" + "=" * 50)
    print("📋 PLEASE SHARE:")
    print("1. ALL output from backend terminal")
    print("2. ALL output from this test script")
    print("3. Any error messages you see")
    print("=" * 50)
