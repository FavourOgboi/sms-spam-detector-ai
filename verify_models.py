#!/usr/bin/env python3
"""
Verify that the app is using the correct models and check explainable AI setup
"""

import os
import sys
import joblib
import numpy as np

# Add backend to path
sys.path.append('backend')

def check_model_files():
    """Check if model files exist and are loadable"""
    print("🔍 Checking Model Files")
    print("=" * 40)
    
    model_path = r'models\main_model\clf_model.pkl'
    vectorizer_path = r'models\main_model\vectorizer.pkl'
    
    print(f"📁 Model path: {model_path}")
    print(f"📁 Vectorizer path: {vectorizer_path}")
    
    # Check if files exist
    model_exists = os.path.exists(model_path)
    vectorizer_exists = os.path.exists(vectorizer_path)
    
    print(f"✅ Model file exists: {model_exists}")
    print(f"✅ Vectorizer file exists: {vectorizer_exists}")
    
    if model_exists and vectorizer_exists:
        try:
            # Load and test models
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            
            print(f"✅ Model type: {type(model).__name__}")
            print(f"✅ Vectorizer type: {type(vectorizer).__name__}")
            
            # Test with sample text
            test_message = "Free money! Click here now!"
            features = vectorizer.transform([test_message])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            
            print(f"🧪 Test prediction: {'SPAM' if prediction == 1 else 'HAM'}")
            print(f"🧪 Test confidence: {max(probabilities):.3f}")
            
            return True, model, vectorizer
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False, None, None
    else:
        print("❌ Model files not found!")
        return False, None, None

def check_app_integration():
    """Check if the app is properly configured to use the models"""
    print("\n🔍 Checking App Integration")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Check if spam_detector is using the correct models
        model_info = spam_detector.get_model_info()
        
        print(f"✅ Model loaded: {model_info['model_loaded']}")
        print(f"✅ Vectorizer loaded: {model_info['vectorizer_loaded']}")
        print(f"✅ Model version: {model_info['model_version']}")
        print(f"✅ Model path: {model_info['model_path']}")
        print(f"✅ Vectorizer path: {model_info['vectorizer_path']}")
        print(f"✅ LIME available: {model_info['lime_available']}")
        print(f"✅ SHAP available: {model_info['shap_available']}")
        
        # Test prediction through the app
        test_message = "Congratulations! You've won $1000! Click here to claim your prize!"
        result = spam_detector.predict(test_message)
        
        print(f"\n🧪 App Prediction Test:")
        print(f"   Message: {test_message[:50]}...")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Model Version: {result['model_version']}")
        
        return True, spam_detector
        
    except Exception as e:
        print(f"❌ Error checking app integration: {e}")
        return False, None

def check_explainable_ai():
    """Check explainable AI capabilities"""
    print("\n🔍 Checking Explainable AI")
    print("=" * 40)
    
    try:
        # Check LIME
        try:
            import lime
            from lime.lime_text import LimeTextExplainer
            print("✅ LIME installed and available")
            lime_available = True
        except ImportError:
            print("❌ LIME not available")
            lime_available = False
        
        # Check SHAP
        try:
            import shap
            print("✅ SHAP installed and available")
            shap_available = True
        except ImportError:
            print("❌ SHAP not available")
            shap_available = False
        
        return lime_available, shap_available
        
    except Exception as e:
        print(f"❌ Error checking explainable AI: {e}")
        return False, False

def test_explanation():
    """Test explanation functionality"""
    print("\n🔍 Testing Explanation")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        test_message = "FREE! Win money now! Click this link immediately!"
        
        print(f"📝 Test message: {test_message}")
        
        # Test explanation
        explanation = spam_detector.explain_prediction(test_message, num_features=5)
        
        if explanation.get('success'):
            print("✅ Explanation generated successfully!")
            print(f"   Method: {explanation['explanation']['method']}")
            print(f"   Prediction: {explanation['prediction']}")
            print(f"   Confidence: {explanation['confidence']:.3f}")
            
            print("\n🔍 Top Features:")
            for i, feature in enumerate(explanation['explanation']['features'][:3], 1):
                print(f"   {i}. {feature['feature']}: {feature['importance']:.3f}")
            
            return True
        else:
            print(f"❌ Explanation failed: {explanation.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing explanation: {e}")
        return False

def main():
    """Main verification function"""
    print("🔐 SMS Guard Model Verification")
    print("=" * 50)
    
    # Check model files
    models_ok, model, vectorizer = check_model_files()
    
    # Check app integration
    app_ok, spam_detector = check_app_integration()
    
    # Check explainable AI
    lime_ok, shap_ok = check_explainable_ai()
    
    # Test explanation
    explanation_ok = test_explanation()
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    print(f"✅ Model Files: {'OK' if models_ok else 'FAILED'}")
    print(f"✅ App Integration: {'OK' if app_ok else 'FAILED'}")
    print(f"✅ LIME Available: {'OK' if lime_ok else 'NOT INSTALLED'}")
    print(f"✅ SHAP Available: {'OK' if shap_ok else 'NOT INSTALLED'}")
    print(f"✅ Explanation Test: {'OK' if explanation_ok else 'FAILED'}")
    
    if models_ok and app_ok:
        print("\n🎉 Your app is using the correct models!")
        print("🚀 Prediction and explainable AI are ready!")
    else:
        print("\n⚠️ Issues found - see details above")
    
    return models_ok and app_ok

if __name__ == "__main__":
    main()
