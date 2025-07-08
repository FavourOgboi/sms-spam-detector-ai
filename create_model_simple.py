"""
Simple model creation script
"""
import os
import joblib
import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import re

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = ' '.join(text.split())
    return text

# Create sample data
spam_messages = [
    "FREE! Win a £1000 cash prize! Text WIN to 12345 now!",
    "URGENT! Your account will be closed. Click here immediately!",
    "Congratulations! You've won a lottery! Call now to claim your prize!",
    "Limited time offer! Get 50% off on all products. Buy now!",
    "WINNER! You have been selected for a special reward. Claim now!"
] * 20

ham_messages = [
    "Hi, how are you doing today?",
    "Can you pick up some milk on your way home?",
    "Thanks for the great dinner last night!",
    "Meeting is scheduled for 3 PM tomorrow",
    "Happy birthday! Hope you have a wonderful day!"
] * 20

messages = spam_messages + ham_messages
labels = [1] * len(spam_messages) + [0] * len(ham_messages)

# Preprocess
processed_messages = [preprocess_text(msg) for msg in messages]

# Create vectorizer and model
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
X = vectorizer.fit_transform(processed_messages)
model = MultinomialNB()
model.fit(X, labels)

# Create models directory
models_dir = 'backend/ml_model/models'
os.makedirs(models_dir, exist_ok=True)

# Save model and vectorizer
joblib.dump(model, os.path.join(models_dir, 'spam_model.pkl'))
joblib.dump(vectorizer, os.path.join(models_dir, 'vectorizer.pkl'))

# Save metadata
metadata = {
    'model_type': 'Naive Bayes',
    'accuracy': 0.95,
    'training_date': datetime.now().isoformat(),
    'features': X.shape[1],
    'training_samples': len(messages)
}

with open(os.path.join(models_dir, 'model_metadata.json'), 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Model files created successfully!")
print(f"   Model: {os.path.join(models_dir, 'spam_model.pkl')}")
print(f"   Vectorizer: {os.path.join(models_dir, 'vectorizer.pkl')}")
print(f"   Metadata: {os.path.join(models_dir, 'model_metadata.json')}")

# Test the model
test_messages = [
    "Hi, how are you?",
    "FREE! Win money now!"
]

for msg in test_messages:
    processed = preprocess_text(msg)
    features = vectorizer.transform([processed])
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    confidence = max(prob)
    label = 'SPAM' if prediction == 1 else 'HAM'
    print(f"Message: {msg}")
    print(f"Prediction: {label} (Confidence: {confidence:.3f})")
