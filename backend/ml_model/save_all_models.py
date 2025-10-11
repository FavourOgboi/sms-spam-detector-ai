"""
Script to train all models and save them as .pkl files for production use.
Run this ONCE locally to generate the .pkl files, then commit them to your repo for use in production.
"""

import os
import pandas as pd
import numpy as np
import string
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    RandomForestClassifier, AdaBoostClassifier, BaggingClassifier,
    ExtraTreesClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier
)
try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

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

# --- Load Data ---
DATA_PATH = os.path.join(os.path.dirname(__file__), '../../ml_notebooks/main_notebook/spam.csv')
df = pd.read_csv(DATA_PATH, encoding='latin-1')
df = df.rename(columns={'v1': 'target', 'v2': 'text'})
df = df[['target', 'text']].dropna()
df['target'] = df['target'].map({'ham': 0, 'spam': 1})
df['transformed_text'] = df['text'].apply(transform_text)

# --- Feature Extraction ---
tfidf = TfidfVectorizer(ngram_range=(1,2), max_features=4000)
X = tfidf.fit_transform(df['transformed_text'])
y = df['target'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# --- Model Definitions ---
models = {
    "SVC": SVC(kernel='sigmoid', gamma=1.0, probability=True, random_state=42),
    "KNeighbors": KNeighborsClassifier(),
    "MultinomialNB": MultinomialNB(),
    "DecisionTree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "LogisticRegression": LogisticRegression(solver='liblinear', penalty='l1', random_state=42),
    "RandomForest": RandomForestClassifier(n_estimators=50, random_state=42),
    "AdaBoost": AdaBoostClassifier(n_estimators=50, random_state=42, algorithm='SAMME'),
    "Bagging": BaggingClassifier(n_estimators=50, random_state=42),
    "ExtraTrees": ExtraTreesClassifier(n_estimators=50, random_state=42),
    "GradientBoosting": GradientBoostingClassifier(n_estimators=50, random_state=42),
}
if XGBClassifier is not None:
    models["XGBoost"] = XGBClassifier(n_estimators=50, random_state=42, eval_metric='logloss')

# --- Ensemble (Voting and Stacking) ---
voting = VotingClassifier(
    estimators=[
        ('svc', models["SVC"]),
        ('nb', models["MultinomialNB"]),
        ('et', models["ExtraTrees"])
    ],
    voting='soft'
)
stacking = StackingClassifier(
    estimators=[
        ('svc', models["SVC"]),
        ('nb', models["MultinomialNB"]),
        ('et', models["ExtraTrees"])
    ],
    final_estimator=RandomForestClassifier(n_estimators=50, random_state=42)
)

ensembles = {
    "VotingEnsemble": voting,
    "StackingEnsemble": stacking
}

# --- Training/Fitting and Saving ---
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(model, name):
    path = os.path.join(MODEL_DIR, f"{name}.pkl")
    joblib.dump(model, path)
    print(f"Saved {name} to {path}")

def save_vectorizer(vectorizer):
    path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    joblib.dump(vectorizer, path)
    print(f"Saved TFIDF vectorizer to {path}")

print("Training and saving all models...")

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    save_model(model, name)

for name, model in ensembles.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    save_model(model, name)

save_vectorizer(tfidf)

print("All models and vectorizer saved to:", MODEL_DIR)
