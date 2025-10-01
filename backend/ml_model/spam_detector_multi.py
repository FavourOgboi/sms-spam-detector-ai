"""
SMS Spam Detector - Multi-Model Evaluation Script

- Loads and preprocesses SMS spam data (spam.csv)
- Trains or loads all major models used in the notebook
- Evaluates each model on the test set and on a custom input message
- Prints detailed metrics and prediction for each model
- Also evaluates the best ensemble (stacking or voting) and prints the same

To run:
    python spam_detector_multi.py

Author: [Ogboi Favour Ifeanyi]
"""

import pandas as pd
import numpy as np
import re
import string
import joblib
import sys

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
)
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

# --- Text Preprocessing ---
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
import os
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

# --- Training/Fitting ---
def fit_and_eval(model, name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:,1]
    elif hasattr(model, "decision_function"):
        y_proba = model.decision_function(X_test)
    else:
        y_proba = None
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_proba) if y_proba is not None else None
    report = classification_report(y_test, y_pred, target_names=['Ham', 'Spam'])
    return {
        "model": model,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "roc_auc": roc,
        "classification_report": report
    }

model_results = {}
for name, model in models.items():
    model_results[name] = fit_and_eval(model, name)
for name, model in ensembles.items():
    model_results[name] = fit_and_eval(model, name)

# --- API Functions ---

def explain_consensus_prediction(msg, num_features=5):
    """
    Return the top spam/ham indicator words for the consensus prediction.
    Uses LIME if available, else falls back to Naive Bayes feature log probabilities.
    """
    clean = transform_text(msg)
    features = tfidf.transform([clean])
    # Use MultinomialNB if available, else fallback to first model
    nb_model = None
    for name, r in model_results.items():
        if name == "MultinomialNB":
            nb_model = r["model"]
            break
    if nb_model is None:
        nb_model = list(model_results.values())[0]["model"]
    # Try LIME explanation if available
    try:
        import lime
        import lime.lime_text
        explainer = lime.lime_text.LimeTextExplainer(class_names=['ham', 'spam'], verbose=False, mode='classification')
        def predict_proba_for_lime(texts):
            feats = [transform_text(t) for t in texts]
            X = tfidf.transform(feats)
            return nb_model.predict_proba(X)
        explanation = explainer.explain_instance(msg, predict_proba_for_lime, num_features=num_features, labels=[0, 1], num_samples=1000)
        top_words = []
        for word, importance in explanation.as_list():
            direction = "spam" if importance > 0 else "ham"
            top_words.append({
                "feature": word,
                "importance": abs(importance),
                "direction": direction
            })
        top_words = sorted(top_words, key=lambda x: x["importance"], reverse=True)[:num_features]
        return {
            "success": True,
            "top_features": top_words,
            "summary": (
                "Spam indicators: " +
                ", ".join([w["feature"] for w in top_words if w["direction"] == "spam"]) +
                " | Ham indicators: " +
                ", ".join([w["feature"] for w in top_words if w["direction"] == "ham"])
            )
        }
    except Exception as e:
        # Fallback to NB feature log prob explanation
        feature_names = tfidf.get_feature_names_out()
        if hasattr(nb_model, "feature_log_prob_"):
            log_prob = nb_model.feature_log_prob_
            word_scores = []
            for word in clean.split():
                if word in feature_names:
                    idx = list(feature_names).index(word)
                    spam_score = log_prob[1][idx]
                    ham_score = log_prob[0][idx]
                    diff = spam_score - ham_score
                    word_scores.append({
                        "feature": word,
                        "importance": abs(diff),
                        "direction": "spam" if diff > 0 else "ham"
                    })
            word_scores.sort(key=lambda x: x["importance"], reverse=True)
            top_words = word_scores[:num_features]
            return {
                "success": True,
                "top_features": top_words,
                "summary": (
                    "Spam indicators: " +
                    ", ".join([w["feature"] for w in top_words if w["direction"] == "spam"]) +
                    " | Ham indicators: " +
                    ", ".join([w["feature"] for w in top_words if w["direction"] == "ham"])
                )
            }
        else:
            return {
                "success": False,
                "error": "Model does not support feature explanation"
            }


def get_best_accuracy():
    """Return the highest accuracy among all models."""
    return max([r["accuracy"] for r in model_results.values()])

def get_all_metrics():
    """Return all metrics for all models."""
    return {name: {k: v for k, v in r.items() if k != "model"} for name, r in model_results.items()}

def predict_consensus(msg):
    """Return consensus prediction and per-model predictions for a message."""
    clean = transform_text(msg)
    features = tfidf.transform([clean])
    model_results_dict = {}
    for name, r in model_results.items():
        model = r["model"]
        pred = model.predict(features)[0]
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(features)[0][1]
            conf = float(proba)
        elif hasattr(model, "decision_function"):
            df = model.decision_function(features)
            conf = float(1 / (1 + np.exp(-df)))
        else:
            conf = None
        model_results_dict[name] = {
            "prediction": "spam" if pred == 1 else "ham",
            "confidence": conf
        }
    # Consensus
    from collections import Counter
    votes = [r["prediction"].capitalize() for r in model_results_dict.values() if r["prediction"] in ["spam", "ham"]]
    vote_counts = Counter(votes)
    majority = vote_counts.most_common(1)[0][0] if vote_counts else "Unknown"
    majority_count = vote_counts[majority] if majority != "Unknown" else 0
    total_votes = sum(vote_counts.values())
    agreement_percentage = majority_count / total_votes if total_votes > 0 else 0
    spam_votes = vote_counts.get("Spam", 0)
    ham_votes = vote_counts.get("Ham", 0)
    # Weighted vote: average confidence for spam/ham
    spam_confidences = [r["confidence"] for r in model_results_dict.values() if r["prediction"] == "spam" and isinstance(r["confidence"], (int, float))]
    ham_confidences = [r["confidence"] for r in model_results_dict.values() if r["prediction"] == "ham" and isinstance(r["confidence"], (int, float))]
    avg_spam_conf = np.mean(spam_confidences) if spam_confidences else 0
    avg_ham_conf = np.mean(ham_confidences) if ham_confidences else 0
    weighted_vote = "Spam" if avg_spam_conf > avg_ham_conf else "Ham" if avg_ham_conf > avg_spam_conf else "Unknown"
    # Average confidence of majority-vote models
    if majority == "Spam":
        avg_majority_conf = avg_spam_conf
    elif majority == "Ham":
        avg_majority_conf = avg_ham_conf
    else:
        avg_majority_conf = 0
    # Truthful consensus confidence: agreement * avg_majority_conf
    consensus_confidence = round(agreement_percentage * avg_majority_conf * 100, 1)
    return {
        "consensus": {
            "majority_vote": majority,
            "weighted_vote": weighted_vote,
            "confidence": consensus_confidence,
            "majority_count": majority_count,
            "total_votes": total_votes,
            "spam_votes": spam_votes,
            "ham_votes": ham_votes
        },
        "model_results": model_results_dict
    }

# --- Main Interactive Loop ---
if __name__ == "__main__":
    print("All models loaded and ready.")
    print("Enter an SMS message to test all models (or type 'exit' to quit):")
    while True:
        try:
            input_message = input("\nEnter an SMS message: ").strip()
        except EOFError:
            break 
        if input_message.lower() == "exit":
            break
        result = predict_consensus(input_message)
        print("\nModel Results:")
        print("{:<20} {:<10} {:<10}".format("Model", "Prediction", "Confidence"))
        for model_name, model_res in result["model_results"].items():
            print("{:<20} {:<10} {:<10}".format(
                model_name,
                model_res.get("prediction", "N/A"),
                f"{model_res.get('confidence', 'N/A'):.2f}" if isinstance(model_res.get("confidence"), (int, float)) else "N/A"
            ))
        consensus = result["consensus"]
        print(f"\nConsensus: {consensus['majority_vote']} ({consensus['majority_count']} out of {consensus['total_votes']}) with confidence {consensus['confidence']}%")
        print("\n" + "="*60 + "\n")
