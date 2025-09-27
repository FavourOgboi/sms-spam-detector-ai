#!/usr/bin/env python3
"""
Fix the notebook model issue by ensuring proper model loading and prediction
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import json
from sklearn.exceptions import NotFittedError

def fix_model_loading():
    """Fix the model loading issue in the notebook"""
    print("🔧 Fixing Model Loading Issue")
    print("=" * 40)
    
    # Check if models exist
    model_path = 'models/main_model/clf_model.pkl'
    vectorizer_path = 'models/main_model/vectorizer.pkl'
    
    print(f"📁 Checking model: {model_path}")
    print(f"📁 Checking vectorizer: {vectorizer_path}")
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
        
    if not os.path.exists(vectorizer_path):
        print(f"❌ Vectorizer file not found: {vectorizer_path}")
        return False
    
    try:
        # Load the models
        clf = joblib.load(model_path)
        tfidf = joblib.load(vectorizer_path)
        
        print(f"✅ Model loaded: {type(clf).__name__}")
        print(f"✅ Vectorizer loaded: {type(tfidf).__name__}")
        
        # Test the models
        test_message = "FREE! Win money now! Click here!"
        
        # Transform the message (assuming basic preprocessing)
        test_features = tfidf.transform([test_message])
        prediction = clf.predict(test_features)[0]
        
        print(f"🧪 Test prediction: {'SPAM' if prediction == 1 else 'HAM'}")
        
        if hasattr(clf, 'predict_proba'):
            proba = clf.predict_proba(test_features)[0]
            confidence = max(proba)
            print(f"🧪 Test confidence: {confidence:.3f}")
        
        return True, clf, tfidf
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return False, None, None

def create_fixed_prediction_cell():
    """Create a fixed prediction cell for the notebook"""
    print("\n🔧 Creating Fixed Prediction Code")
    print("=" * 40)
    
    fixed_code = '''
# FIXED: Proper model loading and prediction
import joblib
import numpy as np
import json
from sklearn.exceptions import NotFittedError

# Load the trained models
try:
    # Load your trained model and vectorizer
    clf = joblib.load('../../models/main_model/clf_model.pkl')
    tfidf = joblib.load('../../models/main_model/vectorizer.pkl')
    
    print("✅ Models loaded successfully!")
    print(f"Model type: {type(clf).__name__}")
    print(f"Vectorizer type: {type(tfidf).__name__}")
    
    # Test message
    sample_message = "Money is not going to be given to you for free even if you perform all the tasks."
    
    # For prediction, we need to preprocess the text the same way as during training
    # If you have a transform_text function, use it. Otherwise, use basic preprocessing:
    
    def basic_preprocess(text):
        """Basic text preprocessing"""
        import re
        # Convert to lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\\s+', ' ', text).strip()
        return text
    
    # Preprocess the message
    try:
        # Try to use the transform_text function if it exists
        if 'transform_text' in globals():
            processed_message = transform_text(sample_message)
        else:
            processed_message = basic_preprocess(sample_message)
    except:
        processed_message = basic_preprocess(sample_message)
    
    # Transform to features
    sample_features = tfidf.transform([processed_message])
    
    # Make prediction
    prediction = clf.predict(sample_features)[0]
    
    # Get probabilities if available
    proba = None
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(sample_features)[0].tolist()
    elif hasattr(clf, "decision_function"):
        try:
            decision_scores = clf.decision_function(sample_features)[0]
            # Convert decision function to probability-like scores
            proba = [1 / (1 + np.exp(decision_scores)), 1 / (1 + np.exp(-decision_scores))]
        except:
            proba = None
    
    # Create result
    result = {
        "input": sample_message,
        "processed": processed_message,
        "prediction": int(prediction),
        "label": "Spam" if prediction == 1 else "Ham",
        "proba": proba,
        "model_type": type(clf).__name__,
        "vectorizer_type": type(tfidf).__name__
    }
    
    print("\\n🎉 PREDICTION SUCCESS!")
    print(json.dumps(result, indent=2))
    
except FileNotFoundError as e:
    print(f"❌ Model files not found: {e}")
    print("Make sure you have:")
    print("  - ../../models/main_model/clf_model.pkl")
    print("  - ../../models/main_model/vectorizer.pkl")
    
except NotFittedError as e:
    print("❌ Model is not fitted. Please train the model first.")
    
except Exception as e:
    print(f"❌ Error during prediction: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Save the fixed code to a file
    with open('fixed_prediction_cell.py', 'w') as f:
        f.write(fixed_code)
    
    print("✅ Fixed prediction code saved to: fixed_prediction_cell.py")
    print("📋 Copy this code to replace the problematic cell in your notebook")
    
    return fixed_code

def create_model_training_fix():
    """Create a fix for the model training section"""
    print("\n🔧 Creating Model Training Fix")
    print("=" * 40)
    
    training_fix = '''
# FIXED: Proper model training and saving
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Make sure the models directory exists
os.makedirs('../../models/main_model', exist_ok=True)

# Define the ensemble classifier (same as in your notebook)
clf = VotingClassifier(
    estimators=[
        ('mnb', MultinomialNB()),
        ('svc', SVC(probability=True, random_state=2)),
        ('lr', LogisticRegression(random_state=2))
    ],
    voting='soft'
)

# Train the model
print("🚀 Training ensemble model...")
clf.fit(X_train, y_train)

# Test the model
y_pred = clf.predict(X_test)
from sklearn.metrics import accuracy_score, precision_score

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print(f"✅ Model trained successfully!")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")

# Save the trained model and vectorizer
print("💾 Saving models...")
joblib.dump(clf, '../../models/main_model/clf_model.pkl')
joblib.dump(tfidf, '../../models/main_model/vectorizer.pkl')

print("✅ Models saved successfully!")
print("  - clf_model.pkl: Trained ensemble classifier")
print("  - vectorizer.pkl: TF-IDF vectorizer")
'''
    
    with open('fixed_training_cell.py', 'w') as f:
        f.write(training_fix)
    
    print("✅ Fixed training code saved to: fixed_training_cell.py")
    
    return training_fix

def test_current_models():
    """Test the current models to see if they work"""
    print("\n🧪 Testing Current Models")
    print("=" * 40)
    
    success, clf, tfidf = fix_model_loading()
    
    if success:
        print("✅ Your models are working correctly!")
        print("The issue is in the notebook cell, not the models themselves.")
        
        # Test with multiple messages
        test_messages = [
            "FREE! Win money now! Click here!",
            "Hi mom, can you pick me up at 3pm?",
            "URGENT: Your account will be suspended!",
            "Meeting scheduled for tomorrow at 2pm"
        ]
        
        print("\n🧪 Testing with sample messages:")
        for i, message in enumerate(test_messages, 1):
            try:
                features = tfidf.transform([message])
                prediction = clf.predict(features)[0]
                result = "SPAM" if prediction == 1 else "HAM"
                
                if hasattr(clf, 'predict_proba'):
                    proba = clf.predict_proba(features)[0]
                    confidence = max(proba)
                    print(f"   {i}. {message[:30]}... → {result} ({confidence:.3f})")
                else:
                    print(f"   {i}. {message[:30]}... → {result}")
                    
            except Exception as e:
                print(f"   {i}. Error: {e}")
        
        return True
    else:
        print("❌ Models have issues - need to retrain")
        return False

def main():
    """Main function to fix the notebook issue"""
    print("🔧 SMS Guard Notebook Model Fix")
    print("=" * 50)
    
    # Test current models
    models_ok = test_current_models()
    
    # Create fixed code
    create_fixed_prediction_cell()
    create_model_training_fix()
    
    print("\n" + "=" * 50)
    print("📊 FIX SUMMARY")
    print("=" * 50)
    
    if models_ok:
        print("✅ Your models are working correctly!")
        print("✅ The issue is in the notebook cell code")
        print("✅ Fixed prediction code created")
        
        print("\n🔧 TO FIX YOUR NOTEBOOK:")
        print("1. Open your notebook")
        print("2. Find the cell with 'Model is not fitted' error")
        print("3. Replace it with code from: fixed_prediction_cell.py")
        print("4. Run the cell - it should work now!")
        
    else:
        print("⚠️ Models need to be retrained")
        print("✅ Fixed training code created")
        
        print("\n🔧 TO FIX YOUR NOTEBOOK:")
        print("1. Use code from: fixed_training_cell.py")
        print("2. Train the models properly")
        print("3. Then use: fixed_prediction_cell.py")
    
    print("\n🎯 The root cause:")
    print("   - The 'clf' variable in your notebook wasn't properly defined")
    print("   - Or the model wasn't fitted before prediction")
    print("   - Fixed code ensures proper model loading and error handling")

if __name__ == "__main__":
    main()
