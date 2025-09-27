#!/usr/bin/env python3
"""
Quick fix to restore working prediction
"""

import os
import sys
import joblib

def check_and_fix():
    """Check models and create a working version"""
    print("🔧 Quick Fix for Prediction Error")
    print("=" * 40)
    
    # Check model files
    model_path = r'models\main_model\clf_model.pkl'
    vectorizer_path = r'models\main_model\vectorizer.pkl'
    
    print(f"📁 Checking: {model_path}")
    print(f"📁 Checking: {vectorizer_path}")
    
    model_exists = os.path.exists(model_path)
    vectorizer_exists = os.path.exists(vectorizer_path)
    
    print(f"✅ Model exists: {model_exists}")
    print(f"✅ Vectorizer exists: {vectorizer_exists}")
    
    if model_exists and vectorizer_exists:
        try:
            # Test loading
            print("🔧 Testing model loading...")
            model = joblib.load(model_path)
            vectorizer = joblib.load(vectorizer_path)
            
            print(f"✅ Model: {type(model).__name__}")
            print(f"✅ Vectorizer: {type(vectorizer).__name__}")
            
            # Test prediction
            test_message = "hello world"
            features = vectorizer.transform([test_message])
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            
            print(f"🧪 Test prediction: {'SPAM' if prediction == 1 else 'HAM'}")
            print(f"🧪 Confidence: {max(probabilities):.3f}")
            
            print("\n✅ Models are working correctly!")
            print("The issue is likely in the SpamDetector class or NLTK setup.")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing models: {e}")
            return False
    else:
        print("❌ Model files not found!")
        print("You need to run your notebook and save the models first.")
        return False

def create_simple_fix():
    """Create a simple working version"""
    print("\n🔧 Creating Simple Fix")
    print("=" * 40)
    
    fix_code = '''
# SIMPLE FIX: Add this to your notebook to test the exact same prediction

import joblib
import re

# Load your models
model = joblib.load('../../models/main_model/clf_model.pkl')
vectorizer = joblib.load('../../models/main_model/vectorizer.pkl')

def simple_preprocess(text):
    """Simple preprocessing that should work"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\\s]', '', text)
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

def simple_predict(message):
    """Simple prediction function"""
    processed = simple_preprocess(message)
    features = vectorizer.transform([processed])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    return {
        'message': message,
        'processed': processed,
        'prediction': 'spam' if prediction == 1 else 'ham',
        'confidence': max(probabilities),
        'model_type': type(model).__name__
    }

# Test it
test_message = "Money is not going to be given to you for free even if you perform all the tasks."
result = simple_predict(test_message)

print("🧪 Simple Prediction Test:")
for key, value in result.items():
    print(f"   {key}: {value}")
'''
    
    with open('simple_prediction_test.py', 'w') as f:
        f.write(fix_code)
    
    print("✅ Created simple_prediction_test.py")
    print("📋 Run this in your notebook to test predictions directly")

def main():
    """Main fix function"""
    models_ok = check_and_fix()
    create_simple_fix()
    
    print("\n" + "=" * 40)
    print("📊 QUICK FIX SUMMARY")
    print("=" * 40)
    
    if models_ok:
        print("✅ Your models are working fine!")
        print("✅ The issue is in the app configuration")
        
        print("\n🔧 IMMEDIATE SOLUTIONS:")
        print("1. Run simple_prediction_test.py in your notebook")
        print("2. This will show you the exact prediction your models make")
        print("3. Compare with what the app shows")
        
        print("\n💡 LIKELY CAUSES:")
        print("- NLTK not properly installed/configured")
        print("- SpamDetector class initialization issue")
        print("- Backend not starting properly")
        
        print("\n🚀 QUICK TEST:")
        print("1. Open your notebook")
        print("2. Run the code in simple_prediction_test.py")
        print("3. See what prediction you get")
        print("4. This should match your earlier notebook result")
        
    else:
        print("❌ Models have issues")
        print("🔧 You need to retrain and save models from notebook")

if __name__ == "__main__":
    main()
