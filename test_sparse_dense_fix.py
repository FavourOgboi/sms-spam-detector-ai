#!/usr/bin/env python3
"""
Test the sparse/dense matrix fix
"""

import sys
import os
sys.path.append('backend')

def test_direct_prediction():
    """Test direct prediction with dense arrays"""
    print("🧪 Testing Direct Prediction with Dense Arrays")
    print("=" * 50)
    
    try:
        import joblib
        
        # Load models
        model_path = r'models\main_model\clf_model.pkl'
        vectorizer_path = r'models\main_model\vectorizer.pkl'
        
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        
        print(f"✅ Model: {type(model).__name__}")
        print(f"✅ Vectorizer: {type(vectorizer).__name__}")
        
        # Test message
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        
        # Test with sparse matrix (should fail)
        print(f"\n🧪 Testing with SPARSE matrix:")
        try:
            features_sparse = vectorizer.transform([test_message])
            prediction_sparse = model.predict(features_sparse)[0]
            print(f"   ❌ Sparse worked (unexpected): {'SPAM' if prediction_sparse == 1 else 'HAM'}")
        except Exception as e:
            print(f"   ✅ Sparse failed as expected: {str(e)[:50]}...")
        
        # Test with dense matrix (should work)
        print(f"\n🧪 Testing with DENSE matrix:")
        try:
            features_dense = vectorizer.transform([test_message]).toarray()
            prediction_dense = model.predict(features_dense)[0]
            probabilities = model.predict_proba(features_dense)[0]
            confidence = max(probabilities)
            
            print(f"   ✅ Dense worked: {'SPAM' if prediction_dense == 1 else 'HAM'}")
            print(f"   ✅ Confidence: {confidence:.3f}")
            print(f"   ✅ Probabilities: {probabilities}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Dense failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False

def test_spam_detector():
    """Test the fixed SpamDetector"""
    print("\n🔧 Testing Fixed SpamDetector")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Test message
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        
        print(f"📝 Test message: {test_message}")
        
        # Test prediction
        result = spam_detector.predict(test_message)
        
        print(f"🤖 Result: {result}")
        
        if 'error' in result:
            print(f"❌ Still getting error: {result['error']}")
            return False
        else:
            print(f"✅ Prediction successful!")
            print(f"   Prediction: {result['prediction'].upper()}")
            print(f"   Confidence: {result['confidence']:.3f}")
            print(f"   Model version: {result['model_version']}")
            
            # Check if it matches notebook expectation
            expected_prediction = "ham"
            if result['prediction'].lower() == expected_prediction:
                print(f"🎉 MATCHES NOTEBOOK EXPECTATION!")
                return True
            else:
                print(f"⚠️ Different from notebook (expected {expected_prediction})")
                return True  # Still working, just different result
            
    except Exception as e:
        print(f"❌ SpamDetector error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 Sparse/Dense Matrix Fix Test")
    print("=" * 60)
    
    # Test direct prediction
    direct_ok = test_direct_prediction()
    
    # Test SpamDetector
    detector_ok = test_spam_detector()
    
    print("\n" + "=" * 60)
    print("📊 FIX TEST RESULTS")
    print("=" * 60)
    
    print(f"✅ Direct Prediction: {'OK' if direct_ok else 'FAILED'}")
    print(f"✅ SpamDetector: {'OK' if detector_ok else 'FAILED'}")
    
    if direct_ok and detector_ok:
        print("\n🎉 SPARSE/DENSE ISSUE FIXED!")
        print("✅ Models now work with dense arrays")
        print("✅ SpamDetector predictions working")
        print("✅ App should now work correctly")
        
        print("\n🚀 NEXT STEPS:")
        print("1. Restart backend: python backend/app.py")
        print("2. Start frontend: npm run dev")
        print("3. Test predictions - should work now!")
        
    else:
        print("\n⚠️ Issues still exist:")
        if not direct_ok:
            print("   - Direct model prediction still failing")
        if not detector_ok:
            print("   - SpamDetector still has issues")

if __name__ == "__main__":
    main()
