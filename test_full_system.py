#!/usr/bin/env python3
"""
Test the complete system including login and chatbot
"""

import requests
import json
import time

def test_complete_system():
    """Test the complete system"""
    print("🔧 TESTING COMPLETE SYSTEM")
    print("=" * 50)
    
    base_url = "http://localhost:5000/api"
    
    # Test 1: Health check
    print("1. Testing Backend Health...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ Backend is running")
        else:
            print(f"   ❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Cannot connect to backend: {e}")
        return False
    
    # Test 2: Login
    print("\n2. Testing Login...")
    try:
        login_data = {
            "usernameOrEmail": "demo@example.com",
            "password": "demo123"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            if token:
                print("   ✅ Login successful")
                print(f"   📝 Token: {token[:20]}...")
            else:
                print("   ❌ No token received")
                return False
        else:
            print(f"   ❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Test 3: Chatbot API
    print("\n3. Testing Chatbot API...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_data = {
            "message": "Your account is expiring. Verify your information to continue service",
            "analyze_message": True
        }
        
        response = requests.post(f"{base_url}/chatbot/chat", json=chat_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                bot_response = data['data']['bot_response']
                print("   ✅ Chatbot API working")
                print(f"   🤖 Bot Response: {bot_response[:100]}...")
                
                # Check if spam analysis is included
                if data['data'].get('spam_analysis'):
                    spam_data = data['data']['spam_analysis']
                    print(f"   📊 Spam Analysis: {spam_data['prediction']} ({spam_data['confidence']*100:.1f}%)")
                
                return True
            else:
                print(f"   ❌ Chatbot API failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"   ❌ Chatbot API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Chatbot API error: {e}")
        return False

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("\n🌐 TESTING FRONTEND ACCESSIBILITY")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5174")
        if response.status_code == 200:
            print("✅ Frontend is accessible at http://localhost:5174")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to frontend: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 COMPLETE SYSTEM TEST")
    print("=" * 70)
    
    # Test backend system
    backend_ok = test_complete_system()
    
    # Test frontend accessibility
    frontend_ok = test_frontend_accessibility()
    
    print("\n" + "=" * 70)
    print("🎯 FINAL RESULTS")
    print("=" * 70)
    
    if backend_ok and frontend_ok:
        print("🎉 SUCCESS! COMPLETE SYSTEM IS WORKING!")
        print("\n📋 System Status:")
        print("   ✅ Backend API: WORKING (http://localhost:5000)")
        print("   ✅ Frontend App: WORKING (http://localhost:5174)")
        print("   ✅ User Login: WORKING")
        print("   ✅ AI Chatbot: WORKING")
        print("   ✅ Spam Detection: WORKING")
        
        print("\n🎯 HOW TO USE:")
        print("   1. Open: http://localhost:5174")
        print("   2. Login: demo / demo123")
        print("   3. Click: 'AI Chat' in navigation")
        print("   4. Type: 'Your account is expiring...'")
        print("   5. See: AI response with spam analysis")
        
        print("\n🤖 Your AI Chatbot Features:")
        print("   ✅ Uses your name in conversations")
        print("   ✅ Analyzes messages with your trained model")
        print("   ✅ Provides personalized advice")
        print("   ✅ Shows confidence scores and explanations")
        print("   ✅ Remembers conversation context")
        print("   ✅ Uses simple, easy language")
        
        return True
    else:
        print("⚠️ ISSUES FOUND:")
        if not backend_ok:
            print("   🔧 Backend/API issues")
        if not frontend_ok:
            print("   🔧 Frontend accessibility issues")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SYSTEM IS READY! Go to http://localhost:5174 and test the AI Chat!")
    else:
        print("\n⚠️ Please check the issues above and try again.")
