#!/usr/bin/env python3
"""
Test the accuracy fix - ensure app shows correct model accuracy
"""

import sys
import os
sys.path.append('backend')

def test_model_accuracy():
    """Test that the backend returns correct model accuracy"""
    print("🧪 Testing Model Accuracy Fix")
    print("=" * 50)
    
    try:
        from models import UserStats
        
        # Test the calculate_stats method
        # Using user_id 1 (should exist or create empty stats)
        stats = UserStats.calculate_stats(1)
        
        print(f"📊 Backend Stats:")
        print(f"   Model Accuracy: {stats['accuracy']:.4f} ({stats['accuracy']*100:.2f}%)")
        
        # Check if it matches your notebook accuracy
        expected_accuracy = 0.9816  # Your notebook result
        actual_accuracy = stats['accuracy']
        
        accuracy_correct = abs(actual_accuracy - expected_accuracy) < 0.001
        
        print(f"\n📓 Expected from notebook: {expected_accuracy:.4f} ({expected_accuracy*100:.2f}%)")
        print(f"🤖 Backend returns: {actual_accuracy:.4f} ({actual_accuracy*100:.2f}%)")
        print(f"✅ Accuracy correct: {accuracy_correct}")
        
        # Check accuracyData structure
        if 'accuracyData' in stats:
            acc_data = stats['accuracyData']
            print(f"\n📈 Accuracy Data Structure:")
            print(f"   Training: {acc_data['trainingAccuracy']:.4f}")
            print(f"   Validation: {acc_data['validationAccuracy']:.4f}")
            print(f"   Real-time: {acc_data['realTimeAccuracy']:.4f}")
            
            structure_correct = all(
                abs(acc_data[key] - expected_accuracy) < 0.001 
                for key in ['trainingAccuracy', 'validationAccuracy', 'realTimeAccuracy']
            )
            print(f"✅ Structure correct: {structure_correct}")
        else:
            structure_correct = False
            print("❌ Missing accuracyData structure")
        
        return accuracy_correct and structure_correct
        
    except Exception as e:
        print(f"❌ Error testing accuracy: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction_confidence():
    """Test that predictions return actual model confidence"""
    print("\n🧪 Testing Prediction Confidence")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Test message from your notebook
        test_message = "Money is not going to be given to you for free even if you perform all the tasks."
        
        print(f"📝 Test message: {test_message}")
        
        # Get prediction
        result = spam_detector.predict(test_message)
        
        print(f"🤖 Prediction result:")
        print(f"   Prediction: {result['prediction'].upper()}")
        print(f"   Confidence: {result['confidence']:.4f} ({result['confidence']*100:.1f}%)")
        print(f"   Model version: {result['model_version']}")
        
        # Check if confidence comes from model (not hardcoded)
        confidence_valid = 0.0 <= result['confidence'] <= 1.0
        using_trained_model = result['model_version'] != 'fallback_1.0.0'
        
        print(f"\n📊 Confidence Analysis:")
        print(f"   ✅ Valid range (0-1): {confidence_valid}")
        print(f"   ✅ Using trained model: {using_trained_model}")
        
        # Expected from notebook: HAM with high confidence (1.0)
        expected_prediction = "ham"
        prediction_correct = result['prediction'].lower() == expected_prediction
        
        print(f"   ✅ Prediction matches notebook: {prediction_correct}")
        
        return confidence_valid and using_trained_model and prediction_correct
        
    except Exception as e:
        print(f"❌ Error testing prediction: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🔧 Model Accuracy & Confidence Fix Test")
    print("=" * 60)
    
    # Test backend accuracy
    accuracy_ok = test_model_accuracy()
    
    # Test prediction confidence
    confidence_ok = test_prediction_confidence()
    
    print("\n" + "=" * 60)
    print("📊 FIX TEST RESULTS")
    print("=" * 60)
    
    print(f"✅ Backend Accuracy: {'OK' if accuracy_ok else 'FAILED'}")
    print(f"✅ Prediction Confidence: {'OK' if confidence_ok else 'FAILED'}")
    
    if accuracy_ok and confidence_ok:
        print("\n🎉 ALL FIXES SUCCESSFUL!")
        print("\n📋 What's Fixed:")
        print("   ✅ Backend returns 98.16% accuracy (from your notebook)")
        print("   ✅ Frontend will show correct model accuracy")
        print("   ✅ Predictions use actual model confidence")
        print("   ✅ No more hardcoded 95% or 80% values")
        
        print("\n🚀 Your App Now Shows:")
        print("   📊 Model Accuracy: 98.2% (your actual trained model)")
        print("   🎯 Real Confidence: From model's predict_proba()")
        print("   📈 Explanation Page: Updated with your model stats")
        
        print("\n🎯 Next Steps:")
        print("   1. Restart backend: python backend/app.py")
        print("   2. Start frontend: npm run dev")
        print("   3. Check Dashboard - should show 98.2% accuracy")
        print("   4. Test predictions - confidence from actual model")
        
    else:
        print("\n⚠️ Issues still exist:")
        if not accuracy_ok:
            print("   🔧 Backend accuracy calculation problems")
        if not confidence_ok:
            print("   🔧 Prediction confidence issues")

if __name__ == "__main__":
    main()
