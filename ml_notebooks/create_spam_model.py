"""
SMS Spam Detection Model Training Script

This script creates and trains a spam detection model that can be used
in the Flask backend. Run this script to generate the model files.

Usage:
    python create_spam_model.py
"""

import pandas as pd
import numpy as np
import re
import joblib
import os
from datetime import datetime
import json

# Machine Learning libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def create_sample_dataset():
    """Create a sample dataset for training"""
    
    # Sample spam messages
    spam_messages = [
        "FREE! Win a £1000 cash prize! Text WIN to 12345 now!",
        "URGENT! Your account will be closed. Click here immediately!",
        "Congratulations! You've won a lottery! Call now to claim your prize!",
        "Limited time offer! Get 50% off on all products. Buy now!",
        "WINNER! You have been selected for a special reward. Claim now!",
        "Free entry to win a brand new iPhone! Text IPHONE to 54321",
        "Your loan has been approved! Get cash now with no credit check!",
        "STOP! You owe money. Pay now or face legal action!",
        "Amazing deal! Buy one get one free! Limited time only!",
        "You have won $10000! Click this link to claim your money!",
        "Free ringtones! Text RING to 12345 for unlimited downloads!",
        "Urgent: Your bank account has been compromised. Verify now!",
        "Get rich quick! Make $5000 per week working from home!",
        "Final notice: Your subscription will expire. Renew now!",
        "Exclusive offer just for you! 90% discount on luxury items!"
    ] * 20  # Repeat to get more samples
    
    # Sample legitimate messages
    ham_messages = [
        "Hi, how are you doing today?",
        "Can you pick up some milk on your way home?",
        "Thanks for the great dinner last night!",
        "Meeting is scheduled for 3 PM tomorrow",
        "Happy birthday! Hope you have a wonderful day!",
        "Don't forget about the doctor's appointment",
        "The weather is really nice today, isn't it?",
        "I'll be running a bit late for our meeting",
        "Could you send me the report when you get a chance?",
        "Let's grab lunch together this weekend",
        "The project deadline has been extended to next week",
        "I really enjoyed the movie we watched yesterday",
        "Please call me when you get this message",
        "The package should arrive by Friday",
        "Looking forward to seeing you at the party!"
    ] * 20  # Repeat to get more samples
    
    # Create dataset
    messages = spam_messages + ham_messages
    labels = ['spam'] * len(spam_messages) + ['ham'] * len(ham_messages)
    
    df = pd.DataFrame({
        'message': messages,
        'label': labels
    })
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    return df

def preprocess_text(text):
    """Preprocess SMS text for machine learning"""
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep letters, numbers, and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def train_model():
    """Train the spam detection model"""
    
    print("Creating sample dataset...")
    df = create_sample_dataset()
    
    print(f"Dataset created with {len(df)} samples")
    print(f"Spam messages: {len(df[df['label'] == 'spam'])}")
    print(f"Ham messages: {len(df[df['label'] == 'ham'])}")
    
    # Preprocess messages
    print("Preprocessing text...")
    df['processed_message'] = df['message'].apply(preprocess_text)
    
    # Convert labels to binary
    df['label_binary'] = df['label'].map({'ham': 0, 'spam': 1})
    
    # Split the data
    X = df['processed_message']
    y = df['label_binary']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Create TF-IDF vectorizer
    print("Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    # Fit and transform the training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"TF-IDF matrix shape: {X_train_tfidf.shape}")
    
    # Train models
    models = {
        'Naive Bayes': MultinomialNB(),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
    }
    
    best_model = None
    best_accuracy = 0
    best_model_name = ""
    
    print("\nTraining models...")
    for name, model in models.items():
        print(f"Training {name}...")
        
        # Train the model
        model.fit(X_train_tfidf, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_tfidf)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"{name} Accuracy: {accuracy:.4f}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name
    
    print(f"\nBest Model: {best_model_name} with accuracy: {best_accuracy:.4f}")
    
    # Save the best model and vectorizer
    models_dir = '../backend/ml_model/models'
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'spam_model.pkl')
    vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
    
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    print(f"\nModel saved to: {model_path}")
    print(f"Vectorizer saved to: {vectorizer_path}")
    
    # Save model metadata
    vectorizer_params = vectorizer.get_params()
    # Convert non-serializable objects to strings
    for key, value in vectorizer_params.items():
        if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
            vectorizer_params[key] = str(value)

    metadata = {
        'model_type': best_model_name,
        'accuracy': best_accuracy,
        'training_date': datetime.now().isoformat(),
        'features': X_train_tfidf.shape[1],
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'vectorizer_params': vectorizer_params
    }
    
    metadata_path = os.path.join(models_dir, 'model_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: {metadata_path}")
    
    # Test the saved model
    print("\nTesting the saved model...")
    test_messages = [
        "Hi, how are you doing today?",
        "FREE! Win a £1000 cash prize! Text WIN to 12345 now!",
        "Can you pick up some milk on your way home?",
        "URGENT! Your account will be closed. Click here immediately!",
        "Thanks for the great dinner last night!"
    ]
    
    loaded_model = joblib.load(model_path)
    loaded_vectorizer = joblib.load(vectorizer_path)
    
    for message in test_messages:
        processed = preprocess_text(message)
        features = loaded_vectorizer.transform([processed])
        prediction = loaded_model.predict(features)[0]
        probability = loaded_model.predict_proba(features)[0]
        confidence = max(probability)
        
        label = 'SPAM' if prediction == 1 else 'HAM'
        print(f"Message: {message[:50]}...")
        print(f"Prediction: {label} (Confidence: {confidence:.3f})")
        print("-" * 50)
    
    print("\nModel training completed successfully!")
    print("The model is now ready to be used in the Flask backend.")

if __name__ == "__main__":
    train_model()
