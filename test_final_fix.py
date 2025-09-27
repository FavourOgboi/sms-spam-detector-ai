#!/usr/bin/env python3
"""
Final test to verify the app uses only your trained models
"""

import sys
import os
sys.path.append('backend')

def test_model_loading():
    """Test that models load correctly"""
    print("🔧 Testing Model Loading")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        info = spam_detector.get_model_info()
        
        print(f"✅ Model loaded: {info['model_loaded']}")
        print(f"✅ Vectorizer loaded: {info['vectorizer_loaded']}")
        print(f"✅ NLTK available: {info.get('nltk_available', False)}")
        print(f"✅ Preprocessing: {info.get('preprocessing', 'unknown')}")
        
        if not info['model_loaded'] or not info['vectorizer_loaded']:
            print("❌ Models not loaded!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_exact_prediction():
    """Test prediction with exact message from notebook"""
    print("\n🧪 Testing Exact Prediction")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Exact message from your notebook test
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        
        print(f"📝 Test message: {test_message}")
        
        # Get prediction
        result = spam_detector.predict(test_message)
        
        print(f"🤖 App prediction: {result['prediction'].upper()}")
        print(f"🎯 App confidence: {result['confidence']:.3f}")
        print(f"📊 Model version: {result['model_version']}")
        
        # Expected from notebook
        expected_prediction = "ham"
        expected_confidence_range = (0.9, 1.0)  # Should be very confident HAM
        
        print(f"\n📓 Expected from notebook:")
        print(f"   Prediction: {expected_prediction.upper()}")
        print(f"   Confidence: High (0.9-1.0)")
        
        # Check results
        prediction_correct = result['prediction'].lower() == expected_prediction
        confidence_in_range = expected_confidence_range[0] <= result['confidence'] <= expected_confidence_range[1]
        using_trained_model = result['model_version'] != 'fallback_1.0.0'
        
        print(f"\n📊 Results:")
        print(f"   ✅ Prediction correct: {prediction_correct}")
        print(f"   ✅ Confidence in range: {confidence_in_range}")
        print(f"   ✅ Using trained model: {using_trained_model}")
        
        return prediction_correct and confidence_in_range and using_trained_model
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return False

def test_preprocessing():
    """Test that preprocessing matches notebook"""
    print("\n🔧 Testing Preprocessing")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        processed = spam_detector.preprocess_text(test_message)
        
        print(f"📝 Original: {test_message}")
        print(f"🔧 Processed: {processed}")
        
        # Expected from notebook (with stemming and stopword removal)
        expected = "money go given free even perform task"
        
        print(f"📓 Expected: {expected}")
        
        match = processed == expected
        print(f"✅ Preprocessing match: {match}")
        
        if not match:
            print(f"⚠️ Difference detected:")
            print(f"   Got:      '{processed}'")
            print(f"   Expected: '{expected}'")
        
        return match
        
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return False

def main():
    """Main test function"""
    print("🎯 Final Fix Verification")
    print("=" * 50)
    
    # Test model loading
    loading_ok = test_model_loading()
    
    # Test preprocessing
    preprocessing_ok = test_preprocessing()
    
    # Test prediction
    prediction_ok = test_exact_prediction()
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    
    print(f"✅ Model Loading: {'OK' if loading_ok else 'FAILED'}")
    print(f"✅ Preprocessing: {'OK' if preprocessing_ok else 'FAILED'}")
    print(f"✅ Prediction: {'OK' if prediction_ok else 'FAILED'}")
    
    all_ok = loading_ok and preprocessing_ok and prediction_ok
    
    if all_ok:
        print("\n🎉 SUCCESS! App now matches notebook exactly!")
        print("\n📋 What's Fixed:")
        print("   ✅ Removed fallback prediction system")
        print("   ✅ App uses ONLY your trained models")
        print("   ✅ Exact same preprocessing as notebook")
        print("   ✅ Same predictions as notebook")
        print("   ✅ Removed demo files")
        
        print("\n🚀 Your frontend will now show:")
        print("   - Same predictions as notebook")
        print("   - Same confidence levels")
        print("   - Using your StackingClassifier model")
        
    else:
        print("\n⚠️ Issues still exist:")
        if not loading_ok:
            print("   🔧 Model loading problems")
        if not preprocessing_ok:
            print("   🔧 Preprocessing doesn't match notebook")
        if not prediction_ok:
            print("   🔧 Predictions don't match notebook")

if __name__ == "__main__":
    main()
