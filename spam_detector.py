"""
SMS Spam Detector - Standalone Python Script

- Loads and preprocesses SMS spam data (spam.csv)
- Trains a robust spam classifier (RandomForest with TF-IDF + domain features)
- Handles class imbalance
- Evaluates with accuracy, precision, recall, F1, ROC-AUC
- Allows prediction on custom text input

To run:
    python spam_detector.py

Author: [Your Name]
"""

import pandas as pd
import numpy as np
import re
import string

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
)
from sklearn.utils.class_weight import compute_class_weight

# Optional: Uncomment if you want to use SMOTE for balancing
# from imblearn.over_sampling import SMOTE

# 1. Load Data
import os
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ml_notebooks/main_notebook/spam.csv'))
df = pd.read_csv(DATA_PATH, encoding='latin-1')
df = df.rename(columns={'v1': 'target', 'v2': 'text'})
df = df[['target', 'text']].dropna()
df['target'] = df['target'].map({'ham': 0, 'spam': 1})

# 2. Text Preprocessing
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if w.isalnum()]
    tokens = [w for w in tokens if w not in stop_words and w not in string.punctuation]
    tokens = [ps.stem(w) for w in tokens]
    return " ".join(tokens)

df['transformed_text'] = df['text'].apply(transform_text)

# 3. Feature Engineering
def has_url(text):
    return int(bool(re.search(r"http[s]?://|www\\.", text)))

def digit_count(text):
    return sum(c.isdigit() for c in text)

def special_char_count(text):
    return sum(c in string.punctuation for c in text)

df['has_url'] = df['text'].apply(has_url)
df['digit_count'] = df['text'].apply(digit_count)
df['special_char_count'] = df['text'].apply(special_char_count)
df['msg_length'] = df['text'].apply(len)

# 4. TF-IDF Vectorization (with n-grams)
tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=4000)
X_tfidf = tfidf.fit_transform(df['transformed_text'])

# Combine TF-IDF with domain features
domain_features = df[['has_url', 'digit_count', 'special_char_count', 'msg_length']].values
from scipy.sparse import hstack
X = hstack([X_tfidf, domain_features])
y = df['target'].values

# 5. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 6. (Class imbalance handling not needed for MultinomialNB)

# 7. Model Training (MultinomialNB)
nb = MultinomialNB()
nb.fit(X_train, y_train)
model = nb

# 8. Evaluation
y_pred = model.predict(X_test)
if hasattr(model, "predict_proba"):
    y_proba = model.predict_proba(X_test)[:,1]
else:
    y_proba = None

_accuracy = accuracy_score(y_test, y_pred)
_precision = precision_score(y_test, y_pred)
_recall = recall_score(y_test, y_pred)
_f1 = f1_score(y_test, y_pred)
_roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else None
_classification_report = classification_report(y_test, y_pred, target_names=['Ham', 'Spam'])

def get_accuracy():
    """Return the highest accuracy achieved during training."""
    return _accuracy

def get_metrics():
    """Return all main metrics as a dict."""
    return {
        "accuracy": _accuracy,
        "precision": _precision,
        "recall": _recall,
        "f1": _f1,
        "roc_auc": _roc_auc,
        "classification_report": _classification_report
    }

if __name__ == "__main__":
    print("\n=== SMS Spam Detector Results ===")
    print("Accuracy:  {:.4f}".format(_accuracy))
    print("Precision: {:.4f}".format(_precision))
    print("Recall:    {:.4f}".format(_recall))
    print("F1-score:  {:.4f}".format(_f1))
    if _roc_auc is not None:
        print("ROC-AUC:   {:.4f}".format(_roc_auc))
    print("\nClassification Report:")
    print(_classification_report)

# 9. Predict on Custom Input
def predict_message(msg):
    clean = transform_text(msg)
    features = tfidf.transform([clean])
    dom = np.array([
        has_url(msg),
        digit_count(msg),
        special_char_count(msg),
        len(msg)
    ]).reshape(1, -1)
    from scipy.sparse import hstack
    X_input = hstack([features, dom])
    pred = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)[0][1] if hasattr(model, "predict_proba") else None
    label = "Spam" if pred == 1 else "Ham"
    return label, proba

if __name__ == "__main__":
    print("\nTry the model on your own message!")
    sample = input("Enter an SMS message: ")
    label, proba = predict_message(sample)
    print(f"\nPrediction: {label} (probability: {proba:.3f})" if proba is not None else f"\nPrediction: {label}")
