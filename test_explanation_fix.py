#!/usr/bin/env python3
"""
Test the enhanced explanation functionality
"""
import requests
import json

def test_explanation():
    print("🔍 Testing Enhanced Explanation Feature")
    print("=" * 50)
    
    # Test message
    test_message = "Congratulations! You've won a free prize! Click now to claim your money!"
    
    # First, test if backend is running
    try:
        health_response = requests.get('http://localhost:5000/api/health', timeout=5)
        if health_response.status_code != 200:
            print("❌ Backend not running. Start with: npm run dev")
            return
        print("✅ Backend is running")
    except:
        print("❌ Cannot connect to backend. Start with: npm run dev")
        return
    
    # Login first
    print("\n🔐 Logging in...")
    login_data = {
        "usernameOrEmail": "demo",
        "password": "demo123"
    }
    
    try:
        login_response = requests.post('http://localhost:5000/api/auth/login', json=login_data)
        if login_response.status_code != 200:
            print("❌ Login failed")
            return
        
        token = login_response.json()['data']['token']
        print("✅ Login successful")
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Test prediction
    print(f"\n📊 Testing prediction for: '{test_message[:50]}...'")
    headers = {"Authorization": f"Bearer {token}"}
    
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
            else:
                print(f"❌ Prediction failed: {pred_result.get('error')}")
                return
        else:
            print(f"❌ Prediction request failed: {pred_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return
    
    # Test explanation
    print(f"\n🔍 Testing explanation...")
    
    try:
        exp_response = requests.post(
            'http://localhost:5000/api/explain',
            json={"message": test_message, "num_features": 10},
            headers=headers
        )
        
        print(f"Response status: {exp_response.status_code}")
        
        if exp_response.status_code == 200:
            exp_result = exp_response.json()
            print(f"Response: {json.dumps(exp_result, indent=2)}")
            
            if exp_result['success']:
                explanation = exp_result['data']
                print("\n🎉 EXPLANATION SUCCESS!")
                print(f"Method: {explanation.get('explanation', {}).get('method', 'Unknown')}")
                print(f"Summary: {explanation.get('explanation', {}).get('summary', 'No summary')}")
                
                features = explanation.get('explanation', {}).get('features', [])
                if features:
                    print(f"\nTop {len(features)} features:")
                    for i, feature in enumerate(features[:5]):
                        print(f"  {i+1}. '{feature['feature']}' → {feature['direction']} ({feature['importance']:.3f})")
                else:
                    print("No features found")
                    
            else:
                print(f"❌ Explanation failed: {explanation.get('error')}")
                fallback = explanation.get('fallback_explanation')
                if fallback:
                    print(f"Fallback method: {fallback.get('method')}")
                    print(f"Fallback summary: {fallback.get('summary')}")
        else:
            print(f"❌ Explanation request failed: {exp_response.status_code}")
            print(f"Response: {exp_response.text}")
            
    except Exception as e:
        print(f"❌ Explanation error: {e}")

if __name__ == "__main__":
    test_explanation()
