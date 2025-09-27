#!/usr/bin/env python3
"""
Simple test to check if backend works
"""

import sys
import os
sys.path.append('backend')

def test_basic_import():
    """Test basic imports"""
    print("🔧 Testing Basic Imports")
    print("=" * 30)
    
    try:
        print("Importing spam_detector...")
        from ml_model.spam_detector import spam_detector
        print("✅ SpamDetector imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_prediction():
    """Test simple prediction"""
    print("\n🧪 Testing Simple Prediction")
    print("=" * 30)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Simple test message
        test_message = "Hello world"
        print(f"Testing message: {test_message}")
        
        result = spam_detector.predict(test_message)
        print(f"Result: {result}")
        
        if 'error' in result:
            print(f"❌ Prediction error: {result['error']}")
            return False
        else:
            print(f"✅ Prediction successful: {result['prediction']}")
            return True
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test"""
    print("🔍 Simple Backend Test")
    print("=" * 40)
    
    import_ok = test_basic_import()
    
    if import_ok:
        prediction_ok = test_simple_prediction()
    else:
        prediction_ok = False
    
    print("\n" + "=" * 40)
    print("📊 RESULTS")
    print("=" * 40)
    
    print(f"✅ Import: {'OK' if import_ok else 'FAILED'}")
    print(f"✅ Prediction: {'OK' if prediction_ok else 'FAILED'}")
    
    if import_ok and prediction_ok:
        print("\n🎉 Backend is working!")
    else:
        print("\n❌ Backend has issues")

if __name__ == "__main__":
    main()
