#!/usr/bin/env python3
"""
Quick test to verify backend and create demo user if needed
"""
import requests
import json

def test_and_fix_backend():
    print("🔧 QUICK LOGIN FIX TEST")
    print("=" * 50)
    
    # Test 1: Check if backend is running
    print("1. Testing backend connection...")
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   🔧 Make sure to run: cd backend && python run.py")
        return False
    
    # Test 2: Try demo login
    print("\n2. Testing demo login...")
    login_data = {
        "usernameOrEmail": "demo",
        "password": "demo123"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/auth/login',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Demo login works!")
                return True
            else:
                print(f"❌ Login failed: {result.get('error')}")
        else:
            print(f"❌ Login request failed")
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
    
    # Test 3: Try registration
    print("\n3. Testing registration...")
    register_data = {
        "username": "testuser123",
        "email": "test123@example.com", 
        "password": "testpass123"
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/auth/register',
            json=register_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                print("✅ Registration works!")
                return True
            else:
                print(f"❌ Registration failed: {result.get('error')}")
        else:
            print(f"❌ Registration request failed")
            
    except Exception as e:
        print(f"❌ Registration test error: {e}")
    
    return False

if __name__ == "__main__":
    print("🎯 INSTRUCTIONS:")
    print("1. Start backend: cd backend && python run.py")
    print("2. Run this test: python quick_login_test.py")
    print("3. If this works, the issue is in the frontend")
    print()
    
    success = test_and_fix_backend()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 BACKEND IS WORKING!")
        print("\n✅ Next steps:")
        print("1. Start frontend: npm run dev")
        print("2. Open browser: http://localhost:5173")
        print("3. Open Developer Tools (F12)")
        print("4. Go to Console tab")
        print("5. Try login with: demo / demo123")
        print("6. Check console for detailed logs")
        print("\n🔍 Look for these logs:")
        print("   🚀 Login form submitted")
        print("   🔐 AuthContext: Starting login process")
        print("   🌐 API Service: Making login request")
        print("   📥 Response data")
    else:
        print("❌ BACKEND HAS ISSUES!")
        print("🔧 Fix backend first, then test frontend")
    
    print("=" * 50)
