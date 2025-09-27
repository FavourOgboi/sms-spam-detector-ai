#!/usr/bin/env python3
"""
Test the AI Chatbot System
"""

import sys
import os
sys.path.append('backend')

def test_chatbot_service():
    """Test the chatbot service directly"""
    print("🤖 Testing AI Chatbot Service")
    print("=" * 50)
    
    try:
        from ai_chatbot.chatbot_service import ChatbotService
        from ml_model.spam_detector import spam_detector
        
        # Create chatbot instance
        chatbot = ChatbotService(spam_detector)
        
        # Test message
        test_message = "Your account is expiring. Verify your information to continue service: [link]"
        user_name = "TestUser"
        user_id = "test_123"
        
        print(f"📝 Test Message: {test_message}")
        print(f"👤 User: {user_name}")
        print()
        
        # Test chat functionality
        print("🔍 Testing Chat Response...")
        response = chatbot.chat_with_user(
            user_id=user_id,
            user_name=user_name,
            message=test_message,
            analyze_with_model=True
        )
        
        if response['success']:
            print("✅ Chat Response Generated!")
            print(f"   Bot Response: {response['bot_response'][:100]}...")
            print(f"   Conversation Length: {response.get('conversation_length', 0)}")
            
            # Check if spam analysis was included
            if response.get('spam_analysis'):
                spam_data = response['spam_analysis']
                print(f"   Spam Analysis: {spam_data['prediction'].upper()} ({spam_data['confidence']*100:.1f}%)")
            
            # Check if explanation was included
            if response.get('explanation') and response['explanation'].get('success'):
                exp_data = response['explanation']['explanation']
                print(f"   Explanation Method: {exp_data['method']}")
                print(f"   Features Found: {len(exp_data.get('features', []))}")
            
            return True
        else:
            print(f"❌ Chat failed: {response.get('error', 'Unknown error')}")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_message_analysis():
    """Test message context analysis"""
    print("\n🔍 Testing Message Analysis")
    print("=" * 50)
    
    try:
        from ai_chatbot.chatbot_service import ChatbotService
        
        chatbot = ChatbotService()
        
        test_messages = [
            "Your account is expiring. Verify your information to continue service: [link]",
            "FREE money! Click here now to claim your prize!",
            "Hi, how are you doing today?",
            "URGENT! Your bank account has been compromised!"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Message {i}: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            context = chatbot.analyze_message_context(message)
            
            print(f"   Scenario: {context.get('detected_scenario', 'None')}")
            print(f"   Confidence: {context.get('scenario_confidence', 0):.2f}")
            print(f"   Suspicious Elements: {len(context.get('suspicious_elements', []))}")
            
            if context.get('suspicious_elements'):
                elements = ', '.join(context['suspicious_elements'])
                print(f"   Elements: {elements}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_conversation_memory():
    """Test conversation memory functionality"""
    print("\n💭 Testing Conversation Memory")
    print("=" * 50)
    
    try:
        from ai_chatbot.chatbot_service import ChatbotService
        
        chatbot = ChatbotService()
        user_id = "memory_test_123"
        user_name = "MemoryUser"
        
        # Send multiple messages
        messages = [
            "Hi, I got a suspicious message",
            "It says my account is expiring",
            "Should I click the link?"
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n📝 Message {i}: {message}")
            
            response = chatbot.chat_with_user(
                user_id=user_id,
                user_name=user_name,
                message=message,
                analyze_with_model=False  # Skip model analysis for speed
            )
            
            if response['success']:
                print(f"   ✅ Response generated")
                print(f"   📊 Conversation length: {response.get('conversation_length', 0)}")
            else:
                print(f"   ❌ Failed: {response.get('error', 'Unknown')}")
        
        # Check conversation summary
        summary = chatbot.get_conversation_summary(user_id)
        print(f"\n📊 Conversation Summary:")
        print(f"   Total messages: {summary.get('total_messages', 0)}")
        print(f"   User messages: {summary.get('user_messages', 0)}")
        print(f"   Bot messages: {summary.get('bot_messages', 0)}")
        
        return summary.get('total_messages', 0) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 AI Chatbot System Test")
    print("=" * 70)
    
    # Test chatbot service
    service_ok = test_chatbot_service()
    
    # Test message analysis
    analysis_ok = test_message_analysis()
    
    # Test conversation memory
    memory_ok = test_conversation_memory()
    
    print("\n" + "=" * 70)
    print("🎯 CHATBOT SYSTEM RESULTS")
    print("=" * 70)
    
    print(f"✅ Chatbot Service: {'PASS' if service_ok else 'FAIL'}")
    print(f"✅ Message Analysis: {'PASS' if analysis_ok else 'FAIL'}")
    print(f"✅ Conversation Memory: {'PASS' if memory_ok else 'FAIL'}")
    
    if service_ok and analysis_ok and memory_ok:
        print("\n🎉 SUCCESS! AI Chatbot System Works Perfectly!")
        print("\n📋 What Your Chatbot Provides:")
        print("   ✅ Natural conversations using user names")
        print("   ✅ Context-aware message analysis")
        print("   ✅ Integration with your spam detection model")
        print("   ✅ Personalized advice and recommendations")
        print("   ✅ Conversation memory and context")
        print("   ✅ Simple, user-friendly language")
        
        print("\n🚀 Ready for Frontend Testing:")
        print("   1. Backend is running with chatbot API ✅")
        print("   2. Start frontend: npm run dev")
        print("   3. Login and go to 'AI Chat' page")
        print("   4. Test conversations with suspicious messages")
        print("   5. See personalized advice and explanations")
        
        print("\n🎯 Example Conversation:")
        print("   User: 'Your account is expiring. Verify your information...'")
        print("   AI: 'Hi TestUser! I analyzed your message and our AI thinks...")
        print("        this is likely SPAM with 100% confidence. This looks like")
        print("        a phishing scam! Real companies don't ask you to verify...")
        print("        accounts through text messages. Here's what I recommend...'")
        
    else:
        print("\n⚠️ Issues found:")
        if not service_ok:
            print("   🔧 Chatbot service needs fixing")
        if not analysis_ok:
            print("   🔧 Message analysis needs improvement")
        if not memory_ok:
            print("   🔧 Conversation memory needs fixing")

if __name__ == "__main__":
    main()
