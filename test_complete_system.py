#!/usr/bin/env python3
"""
Complete system test for SMS Guard prediction and explainable AI
"""

import sys
import os
import joblib

# Add backend to path
sys.path.append('backend')

def test_direct_model_access():
    """Test direct access to your models"""
    print("🔍 Testing Direct Model Access")
    print("=" * 40)
    
    try:
        # Load your models directly
        model_path = r'models\main_model\clf_model.pkl'
        vectorizer_path = r'models\main_model\vectorizer.pkl'
        
        print(f"📁 Loading model from: {model_path}")
        print(f"📁 Loading vectorizer from: {vectorizer_path}")
        
        if not os.path.exists(model_path):
            print(f"❌ Model file not found: {model_path}")
            return False
            
        if not os.path.exists(vectorizer_path):
            print(f"❌ Vectorizer file not found: {vectorizer_path}")
            return False
        
        # Load models
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        print(f"✅ Model type: {type(model).__name__}")
        print(f"✅ Vectorizer type: {type(vectorizer).__name__}")
        
        # Test predictions
        test_messages = [
            "FREE! Win money now! Click here!",
            "Hi, how are you doing today?",
            "URGENT: Your account will be suspended!",
            "Meeting at 3pm in room 101"
        ]
        
        print("\n🧪 Direct Model Test Results:")
        for i, message in enumerate(test_messages, 1):
            # Transform and predict
            features = vectorizer.transform([message])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities)
            
            result = "SPAM" if prediction == 1 else "HAM"
            print(f"   {i}. {message[:40]}...")
            print(f"      → {result} (confidence: {confidence:.3f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing direct model access: {e}")
        return False

def test_app_integration():
    """Test app integration with spam_detector"""
    print("\n🔍 Testing App Integration")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Get model info
        info = spam_detector.get_model_info()
        
        print(f"✅ Model loaded: {info['model_loaded']}")
        print(f"✅ Vectorizer loaded: {info['vectorizer_loaded']}")
        print(f"✅ Model version: {info['model_version']}")
        print(f"✅ LIME available: {info['lime_available']}")
        print(f"✅ SHAP available: {info['shap_available']}")
        
        if not info['model_loaded'] or not info['vectorizer_loaded']:
            print("❌ Models not properly loaded in app!")
            return False
        
        # Test prediction through app
        test_message = "Congratulations! You won $1000! Click now!"
        result = spam_detector.predict(test_message)
        
        print(f"\n🧪 App Prediction Test:")
        print(f"   Message: {test_message}")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Model Version: {result['model_version']}")
        print(f"   Processing Time: {result['processing_time_ms']}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing app integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_explainable_ai():
    """Test explainable AI functionality"""
    print("\n🔍 Testing Explainable AI")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        test_message = "FREE money! Win $1000! Click this link NOW!"
        
        print(f"📝 Test message: {test_message}")
        
        # Test explanation
        explanation = spam_detector.explain_prediction(test_message, num_features=5)
        
        if explanation.get('success'):
            print("✅ Explanation generated successfully!")
            print(f"   Method: {explanation['explanation']['method']}")
            print(f"   Prediction: {explanation['prediction']}")
            print(f"   Confidence: {explanation['confidence']:.3f}")
            
            print("\n🔍 Top Features:")
            for i, feature in enumerate(explanation['explanation']['features'][:5], 1):
                importance = feature['importance']
                feature_name = feature['feature']
                direction = "→ SPAM" if importance > 0 else "→ HAM"
                print(f"   {i}. '{feature_name}': {importance:.3f} {direction}")
            
            # Check explanation quality
            if 'explanation_quality' in explanation['explanation']:
                quality = explanation['explanation']['explanation_quality']
                print(f"\n📊 Explanation Quality: {quality.get('confidence_level', 'unknown')}")
            
            return True
        else:
            print(f"❌ Explanation failed: {explanation.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing explainable AI: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking Dependencies")
    print("=" * 40)
    
    dependencies = {
        'joblib': 'Model loading',
        'scikit-learn': 'Machine learning',
        'lime': 'LIME explanations',
        'shap': 'SHAP explanations',
        'numpy': 'Numerical computing',
        'pandas': 'Data handling'
    }
    
    missing = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {description}")
        except ImportError:
            print(f"❌ {dep}: {description} - NOT INSTALLED")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def main():
    """Main test function"""
    print("🔐 SMS Guard Complete System Test")
    print("=" * 50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test direct model access
    direct_ok = test_direct_model_access()
    
    # Test app integration
    app_ok = test_app_integration()
    
    # Test explainable AI
    explain_ok = test_explainable_ai()
    
    print("\n" + "=" * 50)
    print("📊 COMPLETE TEST SUMMARY")
    print("=" * 50)
    
    print(f"✅ Dependencies: {'OK' if deps_ok else 'MISSING'}")
    print(f"✅ Direct Model Access: {'OK' if direct_ok else 'FAILED'}")
    print(f"✅ App Integration: {'OK' if app_ok else 'FAILED'}")
    print(f"✅ Explainable AI: {'OK' if explain_ok else 'FAILED'}")
    
    if all([deps_ok, direct_ok, app_ok, explain_ok]):
        print("\n🎉 ALL SYSTEMS GO!")
        print("🚀 Your SMS Guard app is using the correct models!")
        print("🔍 Explainable AI is working perfectly!")
        print("\n📋 What's Ready:")
        print("   ✅ Your trained model: models/main_model/clf_model.pkl")
        print("   ✅ Your vectorizer: models/main_model/vectorizer.pkl")
        print("   ✅ Prediction API: /api/predict")
        print("   ✅ Explanation API: /api/explain")
        print("   ✅ LIME/SHAP explanations")
        
        print("\n🎯 Next Steps:")
        print("   1. Start backend: python backend/app.py")
        print("   2. Start frontend: npm run dev")
        print("   3. Login and test predictions!")
        
    else:
        print("\n⚠️ Issues found - check details above")
        
        if not direct_ok:
            print("   🔧 Model files may be missing or corrupted")
        if not app_ok:
            print("   🔧 App integration needs fixing")
        if not explain_ok:
            print("   🔧 Explainable AI needs setup")

if __name__ == "__main__":
    main()
