#!/usr/bin/env python3
"""
Debug model loading to see what's happening
"""

import sys
import os
sys.path.append('backend')

def debug_model_loading():
    """Debug the model loading process"""
    print("🔍 Debugging Model Loading")
    print("=" * 50)
    
    # Check file paths
    model_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\clf_model.pkl'
    vectorizer_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\vectorizer.pkl'
    
    print(f"📁 Model path: {model_path}")
    print(f"📁 Vectorizer path: {vectorizer_path}")
    
    print(f"✅ Model exists: {os.path.exists(model_path)}")
    print(f"✅ Vectorizer exists: {os.path.exists(vectorizer_path)}")
    
    if os.path.exists(model_path) and os.path.exists(vectorizer_path):
        try:
            import joblib
            
            print("\n🔧 Loading models directly...")
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            
            print(f"✅ Model type: {type(model).__name__}")
            print(f"✅ Vectorizer type: {type(vectorizer).__name__}")
            
            # Test direct prediction
            test_message = "Money is not going to be given to you for free even if you perform all the tasks."
            
            # Basic preprocessing
            import re
            processed = test_message.lower()
            processed = re.sub(r'[^a-zA-Z\s]', '', processed)
            processed = re.sub(r'\s+', ' ', processed).strip()
            
            print(f"\n🧪 Direct model test:")
            print(f"   Original: {test_message}")
            print(f"   Processed: {processed}")
            
            features = vectorizer.transform([processed])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            
            print(f"   Prediction: {'SPAM' if prediction == 1 else 'HAM'}")
            print(f"   Probabilities: {probabilities}")
            print(f"   Confidence: {max(probabilities):.3f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("❌ Model files not found!")
        return False

def debug_spam_detector():
    """Debug the spam_detector instance"""
    print("\n🔍 Debugging SpamDetector Instance")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Check model info
        info = spam_detector.get_model_info()
        
        print(f"✅ Model loaded: {info['model_loaded']}")
        print(f"✅ Vectorizer loaded: {info['vectorizer_loaded']}")
        print(f"✅ NLTK available: {info.get('nltk_available', 'Unknown')}")
        print(f"✅ Preprocessing: {info.get('preprocessing', 'Unknown')}")
        
        # Check if models are actually None
        print(f"\n🔧 Internal state:")
        print(f"   spam_detector.model is None: {spam_detector.model is None}")
        print(f"   spam_detector.vectorizer is None: {spam_detector.vectorizer is None}")
        
        if spam_detector.model is not None:
            print(f"   Model type: {type(spam_detector.model).__name__}")
        if spam_detector.vectorizer is not None:
            print(f"   Vectorizer type: {type(spam_detector.vectorizer).__name__}")
        
        # Test prediction
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        result = spam_detector.predict(test_message)
        
        print(f"\n🧪 SpamDetector prediction:")
        print(f"   Message: {test_message}")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        print(f"   Model version: {result['model_version']}")
        
        # Check if it's using fallback
        if result['model_version'] == 'fallback_1.0.0':
            print("⚠️ USING FALLBACK PREDICTION! Models not loaded properly.")
            return False
        else:
            print("✅ Using trained models!")
            return True
            
    except Exception as e:
        print(f"❌ Error with SpamDetector: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    print("🔧 SMS Guard Model Loading Debug")
    print("=" * 60)
    
    # Debug direct model loading
    direct_ok = debug_model_loading()
    
    # Debug spam_detector instance
    detector_ok = debug_spam_detector()
    
    print("\n" + "=" * 60)
    print("📊 DEBUG SUMMARY")
    print("=" * 60)
    
    print(f"✅ Direct Model Loading: {'OK' if direct_ok else 'FAILED'}")
    print(f"✅ SpamDetector Instance: {'OK' if detector_ok else 'FAILED'}")
    
    if direct_ok and not detector_ok:
        print("\n🔧 ISSUE IDENTIFIED:")
        print("   - Models load fine directly")
        print("   - SpamDetector is using fallback system")
        print("   - Need to fix SpamDetector initialization")
        
    elif not direct_ok:
        print("\n🔧 ISSUE IDENTIFIED:")
        print("   - Models themselves have problems")
        print("   - Check model files and paths")
        
    elif direct_ok and detector_ok:
        print("\n🎉 EVERYTHING WORKING!")
        print("   - Models load correctly")
        print("   - SpamDetector uses trained models")
        print("   - Issue might be elsewhere")

if __name__ == "__main__":
    main()
