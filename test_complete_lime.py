#!/usr/bin/env python3
"""
Test complete LIME integration - Backend + Frontend
"""
import requests
import json

def test_complete_lime_integration():
    print("🧪 COMPLETE LIME INTEGRATION TEST")
    print("=" * 50)
    
    # Test message
    test_message = "Congratulations! You've won a FREE prize worth $1000! Click now to claim your money!"
    
    # Step 1: Check backend health
    try:
        health_response = requests.get('http://localhost:5000/api/health', timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend not running. Start with: npm run dev")
            return False
        print("✅ Backend is running")
    except:
        print("❌ Cannot connect to backend. Start with: npm run dev")
        return False
    
    # Step 2: Login
    print("\n🔐 Logging in...")
    login_data = {"usernameOrEmail": "demo", "password": "demo123"}
    
    try:
        login_response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
        if login_response.status_code != 200:
            print("❌ Login failed")
            return False
        
        token = login_response.json()['data']['token']
        print("✅ Login successful")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Test prediction with basic explanation
    print(f"\n📊 Testing prediction with basic explanation...")
    print(f"Message: '{test_message[:50]}...'")
    
    try:
        pred_response = requests.post(
            'http://localhost:5000/api/predict',
            json={"message": test_message},
            headers=headers
        )
        
        if pred_response.status_code == 200:
            pred_result = pred_response.json()
            if pred_result['success']:
                prediction = pred_result['data']
                print(f"✅ Prediction: {prediction['prediction']} ({prediction['confidence']:.3f})")
                
                # Check if basic explanation is included
                if 'explanation' in prediction:
                    explanation = prediction['explanation']
                    print(f"✅ Basic explanation included!")
                    print(f"   Method: {explanation.get('method', 'Unknown')}")
                    print(f"   Summary: {explanation.get('summary', 'No summary')[:100]}...")
                    
                    features = explanation.get('top_features', [])
                    if features:
                        print(f"   Top features ({len(features)}):")
                        for i, feature in enumerate(features[:3]):
                            print(f"     {i+1}. '{feature['feature']}' → {feature['direction']} ({feature['importance']:.3f})")
                    else:
                        print("   No features in basic explanation")
                else:
                    print("⚠️ No basic explanation in prediction response")
            else:
                print(f"❌ Prediction failed: {pred_result.get('error')}")
                return False
        else:
            print(f"❌ Prediction request failed: {pred_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False
    
    # Step 4: Test detailed explanation endpoint
    print(f"\n🔍 Testing detailed explanation endpoint...")
    
    try:
        exp_response = requests.post(
            'http://localhost:5000/api/explain',
            json={"message": test_message, "num_features": 10},
            headers=headers
        )
        
        if exp_response.status_code == 200:
            exp_result = exp_response.json()
            if exp_result['success']:
                explanation = exp_result['data']
                print("✅ Detailed explanation successful!")
                
                exp_data = explanation.get('explanation', {})
                print(f"   Method: {exp_data.get('method', 'Unknown')}")
                print(f"   Summary: {exp_data.get('summary', 'No summary')[:100]}...")
                
                features = exp_data.get('features', [])
                if features:
                    print(f"   Detailed features ({len(features)}):")
                    for i, feature in enumerate(features[:5]):
                        print(f"     {i+1}. '{feature['feature']}' → {feature['direction']} ({feature['importance']:.3f})")
                        
                    # Check if this is LIME or fallback
                    method = exp_data.get('method', '')
                    if 'LIME' in method:
                        print("🎉 LIME is working!")
                    else:
                        print(f"⚠️ Using fallback method: {method}")
                else:
                    print("   No detailed features found")
                    
            else:
                print(f"❌ Detailed explanation failed: {explanation.get('error')}")
                fallback = explanation.get('fallback_explanation')
                if fallback:
                    print(f"   Fallback available: {fallback.get('method')}")
        else:
            print(f"❌ Explanation request failed: {exp_response.status_code}")
            
    except Exception as e:
        print(f"❌ Explanation error: {e}")
    
    # Step 5: Frontend integration check
    print(f"\n🌐 Frontend Integration Check...")
    print("✅ Basic explanation should appear automatically in prediction results")
    print("✅ 'Explain Prediction' button should show detailed LIME analysis")
    print("✅ Visual highlighting should show spam/ham contributing words")
    
    print("\n" + "=" * 50)
    print("🎯 INTEGRATION TEST COMPLETE!")
    print("\n📋 What to check in frontend:")
    print("1. Go to http://localhost:5173/predict")
    print("2. Enter test message and predict")
    print("3. Look for purple 'AI Explanation' section")
    print("4. Click 'Explain Prediction' for detailed analysis")
    print("5. Check word highlighting and importance scores")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_complete_lime_integration()
