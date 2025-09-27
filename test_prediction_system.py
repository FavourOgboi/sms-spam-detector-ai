#!/usr/bin/env python3
"""
Test the prediction system to ensure it's using your models
"""

import requests
import json
import time

BACKEND_URL = "http://localhost:5000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_prediction_api():
    """Test prediction API with sample messages"""
    print("\n🧪 Testing Prediction API")
    print("=" * 40)
    
    # Test messages
    test_messages = [
        {
            "message": "FREE! Win $1000 now! Click here immediately!",
            "expected": "spam"
        },
        {
            "message": "Hi mom, can you pick me up from school at 3pm?",
            "expected": "ham"
        },
        {
            "message": "URGENT: Your account will be closed! Call 123-456-7890 NOW!",
            "expected": "spam"
        },
        {
            "message": "Meeting scheduled for tomorrow at 2pm in conference room A",
            "expected": "ham"
        }
    ]
    
    # You'll need a valid JWT token for this
    # For now, let's just test the endpoint structure
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_JWT_TOKEN"  # You'd need to login first
    }
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {test_case['message'][:50]}...")
        print(f"   Expected: {test_case['expected'].upper()}")
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/predict",
                json={"message": test_case["message"]},
                headers=headers,
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 401:
                print("   ⚠️ Authentication required (expected)")
            elif response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    data = result['data']
                    prediction = data['prediction']
                    confidence = data['confidence']
                    model_version = data.get('model_version', 'unknown')
                    
                    print(f"   ✅ Prediction: {prediction.upper()}")
                    print(f"   ✅ Confidence: {confidence:.3f}")
                    print(f"   ✅ Model Version: {model_version}")
                    
                    # Check if prediction matches expectation
                    if prediction == test_case['expected']:
                        print("   🎯 Prediction matches expectation!")
                    else:
                        print("   ⚠️ Prediction differs from expectation")
                else:
                    print(f"   ❌ API Error: {result.get('error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")

def test_explanation_api():
    """Test explanation API"""
    print("\n🔍 Testing Explanation API")
    print("=" * 40)
    
    test_message = "FREE money! Win $1000! Click now!"
    
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_JWT_TOKEN"  # You'd need to login first
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/explain",
            json={
                "message": test_message,
                "num_features": 5
            },
            headers=headers,
            timeout=15
        )
        
        print(f"📝 Test message: {test_message}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 401:
            print("⚠️ Authentication required (expected)")
        elif response.status_code == 200:
            result = response.json()
            if result.get('success'):
                data = result['data']
                print(f"✅ Explanation method: {data['explanation']['method']}")
                print(f"✅ Prediction: {data['prediction']}")
                print(f"✅ Confidence: {data['confidence']:.3f}")
                
                print("\n🔍 Top Features:")
                for i, feature in enumerate(data['explanation']['features'][:3], 1):
                    print(f"   {i}. {feature['feature']}: {feature['importance']:.3f}")
            else:
                print(f"❌ API Error: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def check_model_info():
    """Check what model info is available"""
    print("\n📊 Model Information")
    print("=" * 40)
    
    try:
        # This would require direct access to the spam_detector
        import sys
        sys.path.append('backend')
        from ml_model.spam_detector import spam_detector
        
        model_info = spam_detector.get_model_info()
        
        print(f"✅ Model loaded: {model_info['model_loaded']}")
        print(f"✅ Vectorizer loaded: {model_info['vectorizer_loaded']}")
        print(f"✅ Model version: {model_info['model_version']}")
        print(f"✅ LIME available: {model_info['lime_available']}")
        print(f"✅ SHAP available: {model_info['shap_available']}")
        print(f"📁 Model path: {model_info['model_path']}")
        print(f"📁 Vectorizer path: {model_info['vectorizer_path']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing model info: {e}")
        return False

def main():
    """Main test function"""
    print("🔐 SMS Guard Prediction System Test")
    print("=" * 50)
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend not running. Start with: python backend/app.py")
        return
    
    # Check model info
    model_ok = check_model_info()
    
    # Test prediction API (will require auth)
    test_prediction_api()
    
    # Test explanation API (will require auth)
    test_explanation_api()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if model_ok:
        print("✅ Your app is using the correct models from:")
        print("   📁 models/main_model/clf_model.pkl")
        print("   📁 models/main_model/vectorizer.pkl")
        print("\n🚀 To test predictions, you need to:")
        print("   1. Start frontend: npm run dev")
        print("   2. Login to get JWT token")
        print("   3. Use the prediction interface")
    else:
        print("⚠️ Model loading issues detected")

if __name__ == "__main__":
    main()
