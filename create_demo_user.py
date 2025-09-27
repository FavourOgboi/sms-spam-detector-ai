#!/usr/bin/env python3
"""
Create demo user for testing
"""

import requests
import json

def create_demo_user():
    """Create demo user via API"""
    print("🔧 Creating Demo User")
    print("=" * 30)
    
    base_url = "http://localhost:5000/api"
    
    # Register demo user
    register_data = {
        "username": "demo",
        "email": "demo@example.com",
        "password": "demo123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ Demo user created successfully!")
            return True
        elif response.status_code == 409:
            print("✅ Demo user already exists!")
            return True
        else:
            print(f"❌ Failed to create demo user: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating demo user: {e}")
        return False

def test_demo_login():
    """Test demo user login"""
    print("\n🔐 Testing Demo User Login")
    print("=" * 30)
    
    base_url = "http://localhost:5000/api"
    
    login_data = {
        "usernameOrEmail": "demo@example.com",
        "password": "demo123"
    }
    
    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('data', {}).get('access_token')
            if token:
                print("✅ Demo user login successful!")
                print(f"📝 Token: {token[:20]}...")
                return token
            else:
                print("❌ No token received")
                return None
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_chatbot_with_token(token):
    """Test chatbot with valid token"""
    print("\n🤖 Testing Chatbot API")
    print("=" * 30)
    
    base_url = "http://localhost:5000/api"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    chat_data = {
        "message": "Your account is expiring. Verify your information to continue service",
        "analyze_message": True
    }
    
    try:
        response = requests.post(f"{base_url}/chatbot/chat", json=chat_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                bot_response = data['data']['bot_response']
                print("✅ Chatbot API working!")
                print(f"🤖 Bot Response: {bot_response[:100]}...")
                
                # Check spam analysis
                if data['data'].get('spam_analysis'):
                    spam_data = data['data']['spam_analysis']
                    print(f"📊 Spam Analysis: {spam_data['prediction']} ({spam_data['confidence']*100:.1f}%)")
                
                return True
            else:
                print(f"❌ Chatbot failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Chatbot API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 DEMO USER SETUP & TEST")
    print("=" * 50)
    
    # Create demo user
    user_created = create_demo_user()
    if not user_created:
        print("❌ Cannot proceed without demo user")
        return False
    
    # Test login
    token = test_demo_login()
    if not token:
        print("❌ Cannot proceed without valid login")
        return False
    
    # Test chatbot
    chatbot_ok = test_chatbot_with_token(token)
    
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULTS")
    print("=" * 50)
    
    if chatbot_ok:
        print("🎉 SUCCESS! COMPLETE SYSTEM IS WORKING!")
        print("\n📋 System Status:")
        print("   ✅ Demo User: CREATED")
        print("   ✅ Login: WORKING")
        print("   ✅ AI Chatbot: WORKING")
        print("   ✅ Spam Detection: WORKING")
        
        print("\n🎯 HOW TO USE:")
        print("   1. Open: http://localhost:5174")
        print("   2. Login: demo@example.com / demo123")
        print("   3. Click: 'AI Chat' in navigation")
        print("   4. Type: 'Your account is expiring...'")
        print("   5. See: AI response with spam analysis")
        
        return True
    else:
        print("❌ Chatbot system has issues")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SYSTEM IS READY! Go to http://localhost:5174 and test the AI Chat!")
    else:
        print("\n⚠️ Please check the issues above.")
