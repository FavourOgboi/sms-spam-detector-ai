#!/usr/bin/env python3
"""
Test the preprocessing fix to ensure app matches notebook
"""

import sys
sys.path.append('backend')

from ml_model.spam_detector import spam_detector

def test_preprocessing_match():
    """Test that app preprocessing matches notebook"""
    print("🧪 Testing Preprocessing Match")
    print("=" * 50)
    
    # Test message from your example
    test_message = "Money is not going to be given to you for free even if you perform all the tasks."
    
    print(f"📝 Original message:")
    print(f"   {test_message}")
    
    # Test app preprocessing
    processed_app = spam_detector.preprocess_text(test_message)
    print(f"\n🔧 App preprocessing:")
    print(f"   {processed_app}")
    
    # Expected from notebook
    expected_notebook = "money go given free even perform task"
    print(f"\n📓 Expected (notebook):")
    print(f"   {expected_notebook}")
    
    # Check if they match
    if processed_app == expected_notebook:
        print(f"\n✅ PERFECT MATCH! Preprocessing is identical")
        return True
    else:
        print(f"\n⚠️ MISMATCH detected")
        print(f"   App:      '{processed_app}'")
        print(f"   Notebook: '{expected_notebook}'")
        return False

def test_prediction_match():
    """Test that predictions now match"""
    print("\n🎯 Testing Prediction Match")
    print("=" * 50)
    
    test_message = "Money is not going to be given to you for free even if you perform all the tasks."
    
    # Get app prediction
    result = spam_detector.predict(test_message)
    
    print(f"📝 Test message: {test_message}")
    print(f"🤖 App prediction: {result['prediction'].upper()}")
    print(f"🎯 App confidence: {result['confidence']:.3f}")
    
    # Expected from notebook
    expected_prediction = "ham"  # From your notebook result
    expected_confidence = 1.0    # From your notebook result
    
    print(f"\n📓 Expected (notebook):")
    print(f"   Prediction: {expected_prediction.upper()}")
    print(f"   Confidence: {expected_confidence:.3f}")
    
    # Check match
    prediction_match = result['prediction'].lower() == expected_prediction.lower()
    confidence_close = abs(result['confidence'] - expected_confidence) < 0.1
    
    if prediction_match and confidence_close:
        print(f"\n✅ PREDICTIONS MATCH! App now uses notebook models correctly")
        return True
    else:
        print(f"\n⚠️ PREDICTIONS STILL DIFFER")
        if not prediction_match:
            print(f"   Prediction mismatch: {result['prediction']} vs {expected_prediction}")
        if not confidence_close:
            print(f"   Confidence mismatch: {result['confidence']:.3f} vs {expected_confidence:.3f}")
        return False

def test_model_info():
    """Test model information"""
    print("\n📊 Model Information")
    print("=" * 50)
    
    info = spam_detector.get_model_info()
    
    print(f"✅ Model loaded: {info['model_loaded']}")
    print(f"✅ Vectorizer loaded: {info['vectorizer_loaded']}")
    print(f"✅ NLTK available: {info['nltk_available']}")
    print(f"✅ Preprocessing: {info['preprocessing']}")
    print(f"✅ Model version: {info['model_version']}")
    
    return info['model_loaded'] and info['vectorizer_loaded']

def main():
    """Main test function"""
    print("🔧 SMS Guard Preprocessing Fix Test")
    print("=" * 60)
    
    # Test model info
    model_ok = test_model_info()
    
    if not model_ok:
        print("\n❌ Models not loaded properly!")
        return
    
    # Test preprocessing
    preprocessing_ok = test_preprocessing_match()
    
    # Test predictions
    prediction_ok = test_prediction_match()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    print(f"✅ Model Loading: {'OK' if model_ok else 'FAILED'}")
    print(f"✅ Preprocessing Match: {'OK' if preprocessing_ok else 'FAILED'}")
    print(f"✅ Prediction Match: {'OK' if prediction_ok else 'FAILED'}")
    
    if all([model_ok, preprocessing_ok, prediction_ok]):
        print("\n🎉 SUCCESS! App now matches notebook exactly!")
        print("🚀 Your frontend will now show the same results as notebook!")
        
        print("\n📋 What's Fixed:")
        print("   ✅ App uses EXACT same preprocessing as notebook")
        print("   ✅ NLTK tokenization, stopword removal, stemming")
        print("   ✅ Same model, same vectorizer, same preprocessing")
        print("   ✅ Frontend predictions will match notebook")
        
    else:
        print("\n⚠️ Issues still exist - check details above")
        
        if not preprocessing_ok:
            print("   🔧 Preprocessing needs more work")
        if not prediction_ok:
            print("   🔧 Predictions still don't match")

if __name__ == "__main__":
    main()
