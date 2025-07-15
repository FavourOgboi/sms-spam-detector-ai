#!/usr/bin/env python3
"""
Test authentication with the proper backend structure
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_backend_health():
    """Test if backend is running"""
    print("🏥 Testing Backend Health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend is running!")
            print(f"   Message: {result.get('message')}")
            return True
        else:
            print(f"❌ Backend returned {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure to run: cd backend && python run.py")
        return False

def test_demo_login():
    """Test demo user login"""
    print("\n🔐 Testing Demo Login...")
    try:
        login_data = {
            "usernameOrEmail": "demo",
            "password": "demo123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Demo login successful!")
                token = result['data']['token']
                user = result['data']['user']
                print(f"   Token: {token[:20]}...")
                print(f"   User: {user['username']} ({user['email']})")
                return token
            else:
                print(f"❌ Demo login failed: {result.get('error')}")
                return None
        else:
            print(f"❌ Demo login request failed: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Demo login error: {e}")
        return None

def test_user_registration():
    """Test new user registration"""
    print("\n📝 Testing User Registration...")
    
    import random
    import string
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    test_username = f"testuser_{random_suffix}"
    test_email = f"test_{random_suffix}@example.com"
    test_password = "testpass123"
    
    try:
        register_data = {
            "username": test_username,
            "email": test_email,
            "password": test_password
        }
        
        print(f"   Creating user: {test_username}")
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                print("✅ Registration successful!")
                token = result['data']['token']
                user = result['data']['user']
                print(f"   User: {user['username']} ({user['email']})")
                return token
            else:
                print(f"❌ Registration failed: {result.get('error')}")
                return None
        else:
            print(f"❌ Registration request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_protected_endpoints(token):
    """Test protected endpoints"""
    print("\n🔒 Testing Protected Endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test user stats
    try:
        response = requests.get(f"{BASE_URL}/user/stats", headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                stats = result['data']
                print(f"✅ User stats: {stats['totalMessages']} messages")
            else:
                print(f"❌ Stats failed: {result.get('error')}")
        else:
            print(f"❌ Stats request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {e}")

def main():
    print("🧪 TESTING PROPER BACKEND STRUCTURE")
    print("=" * 50)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("\n❌ Backend is not running!")
        print("🔧 Start it with:")
        print("   cd backend")
        print("   python run.py")
        return
    
    # Test 2: Demo login
    demo_token = test_demo_login()
    if demo_token:
        test_protected_endpoints(demo_token)
    
    # Test 3: User registration
    new_user_token = test_user_registration()
    if new_user_token:
        test_protected_endpoints(new_user_token)
    
    # Final result
    print("\n" + "=" * 50)
    if demo_token or new_user_token:
        print("🎉 AUTHENTICATION IS WORKING!")
        print("\n✅ Your backend is properly structured and functional!")
        print("\n🚀 Now test the frontend:")
        print("   1. Run: npm run dev")
        print("   2. Open: http://localhost:5173")
        print("   3. Login with: demo / demo123")
    else:
        print("❌ AUTHENTICATION FAILED!")
        print("🔧 Check the backend logs for errors")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
