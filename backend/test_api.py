"""
Simple API Test Script for SMS Guard Backend

This script tests the basic functionality of the Flask API endpoints.
Run this after starting the Flask server to verify everything works.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print("❌ Health check failed")
            print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    print("-" * 50)

def test_user_registration():
    """Test user registration"""
    print("Testing user registration...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=TEST_USER,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("✅ User registration successful")
            data = response.json()
            if data.get('success') and 'token' in data.get('data', {}):
                print("✅ JWT token received")
                return data['data']['token']
            else:
                print("❌ Invalid response format")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
    
    print("-" * 50)
    return None

def test_user_login():
    """Test user login"""
    print("Testing user login...")
    try:
        login_data = {
            "usernameOrEmail": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ User login successful")
            data = response.json()
            if data.get('success') and 'token' in data.get('data', {}):
                print("✅ JWT token received")
                return data['data']['token']
            else:
                print("❌ Invalid response format")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
    
    print("-" * 50)
    return None

def test_spam_prediction(token):
    """Test spam prediction"""
    if not token:
        print("❌ No token available for prediction test")
        return
    
    print("Testing spam prediction...")
    
    test_messages = [
        "Hi, how are you doing today?",
        "FREE! Win a £1000 cash prize! Text WIN to 12345 now!",
        "Can you pick up some milk on your way home?",
        "URGENT! Your account will be closed. Click here immediately!"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    for message in test_messages:
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json={"message": message},
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    prediction_data = data.get('data', {})
                    prediction = prediction_data.get('prediction', 'unknown')
                    confidence = prediction_data.get('confidence', 0)
                    print(f"✅ Message: {message[:30]}...")
                    print(f"   Prediction: {prediction.upper()} (Confidence: {confidence:.3f})")
                else:
                    print(f"❌ Prediction failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ Prediction request failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Prediction error: {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("-" * 50)

def test_user_stats(token):
    """Test user statistics"""
    if not token:
        print("❌ No token available for stats test")
        return
    
    print("Testing user statistics...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/user/stats", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                stats = data.get('data', {})
                print("✅ User statistics retrieved")
                print(f"   Total Messages: {stats.get('totalMessages', 0)}")
                print(f"   Spam Count: {stats.get('spamCount', 0)}")
                print(f"   Ham Count: {stats.get('hamCount', 0)}")
                print(f"   Spam Rate: {stats.get('spamRate', 0):.2%}")
            else:
                print(f"❌ Stats failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Stats request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats error: {str(e)}")
    
    print("-" * 50)

def main():
    """Run all tests"""
    print("=" * 50)
    print("SMS Guard API Test Suite")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test registration (this might fail if user already exists)
    token = test_user_registration()
    
    # Test login (this should work even if registration failed)
    if not token:
        token = test_user_login()
    
    # Test prediction with authentication
    test_spam_prediction(token)
    
    # Test user statistics
    test_user_stats(token)
    
    print("=" * 50)
    print("Test suite completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
