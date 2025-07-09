"""
Train SMS Spam Detection Model with Explainable AI
This script trains a machine learning model with proper LIME and SHAP integration
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import os
import re

# Check for explainable AI libraries
try:
    import lime
    import lime.lime_text
    LIME_AVAILABLE = True
    print("✅ LIME available")
except ImportError:
    LIME_AVAILABLE = False
    print("❌ LIME not available - install with: pip install lime")

try:
    import shap
    SHAP_AVAILABLE = True
    print("✅ SHAP available")
except ImportError:
    SHAP_AVAILABLE = False
    print("❌ SHAP not available - install with: pip install shap")

def create_sample_dataset():
    """Create a comprehensive sample SMS dataset"""
    
    # Spam messages with various patterns
    spam_messages = [
        "FREE! Win a $1000 gift card! Click here now!",
        "URGENT! Your account will be suspended. Call 555-SCAM immediately!",
        "Congratulations! You've won a lottery! Send your details to claim prize!",
        "Limited time offer! Get rich quick! Click this link now!",
        "WINNER! You are selected for cash prize! Reply with your bank details!",
        "Free money! No strings attached! Call now to claim your reward!",
        "ALERT: Suspicious activity detected. Verify your account immediately!",
        "You have been chosen! Win big money! Text STOP to opt out!",
        "Exclusive offer! Make money from home! Limited time only!",
        "URGENT: Your payment is overdue. Pay now to avoid penalties!",
        "CONGRATULATIONS! You won $5000! Click to claim now!",
        "FREE iPhone! Limited offer! Call 1-800-SCAM now!",
        "WINNER WINNER! Cash prize waiting! Reply YES to claim!",
        "URGENT ACTION REQUIRED! Account suspended! Click here!",
        "Make $1000 daily from home! No experience needed!",
        "FREE VACATION! You've been selected! Call now!",
        "ALERT! Virus detected! Download our antivirus now!",
        "FINAL NOTICE! Pay immediately or face consequences!",
        "WIN BIG! Lottery winner! Send details to claim!",
        "FREE MONEY! No catch! Limited time offer!"
    ] * 5  # Repeat for more samples
    
    # Legitimate messages
    ham_messages = [
        "Hi! Are we still meeting for lunch tomorrow at 12pm?",
        "Thanks for the meeting today. I'll send the report by Friday.",
        "Can you pick up milk on your way home? Thanks!",
        "The conference call is scheduled for 3pm. Dial-in details attached.",
        "Happy birthday! Hope you have a wonderful day!",
        "Reminder: Doctor appointment tomorrow at 2pm.",
        "Great job on the presentation! The client was impressed.",
        "Movie starts at 7pm. See you at the theater!",
        "Flight delayed by 30 minutes. New arrival time is 8:45pm.",
        "Package delivered successfully. Thank you for your order!",
        "Meeting rescheduled to Thursday 3pm. Conference room B.",
        "Your prescription is ready for pickup at the pharmacy.",
        "Thanks for dinner last night! Had a great time.",
        "Project deadline extended to next Monday. Please update timeline.",
        "Weather forecast shows rain tomorrow. Bring an umbrella!",
        "Bank statement available online. Check your account.",
        "Gym class cancelled today due to instructor illness.",
        "Your order has shipped. Tracking number: ABC123456.",
        "Reminder: Parent-teacher conference on Friday at 4pm.",
        "Team lunch at Italian restaurant. Meet at 12:30pm."
    ] * 5  # Repeat for more samples
    
    # Create DataFrame
    messages = spam_messages + ham_messages
    labels = ['spam'] * len(spam_messages) + ['ham'] * len(ham_messages)
    
    df = pd.DataFrame({
        'message': messages,
        'label': labels
    })
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

def preprocess_text(text):
    """Basic text preprocessing"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def train_models():
    """Train multiple models and select the best one"""
    
    print("🚀 Starting SMS Spam Detection Model Training")
    print("=" * 50)
    
    # Create dataset
    print("📊 Creating dataset...")
    df = create_sample_dataset()
    print(f"   Dataset size: {len(df)} messages")
    print(f"   Distribution: {df['label'].value_counts().to_dict()}")
    
    # Preprocess text
    print("🔄 Preprocessing text...")
    df['processed_message'] = df['message'].apply(preprocess_text)
    df['label_binary'] = df['label'].map({'ham': 0, 'spam': 1})
    
    # Split data
    X = df['processed_message']
    y = df['label_binary']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Training set: {len(X_train)} messages")
    print(f"   Test set: {len(X_test)} messages")
    
    # Create TF-IDF vectorizer
    print("🔄 Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"   Feature matrix shape: {X_train_tfidf.shape}")
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Naive Bayes': MultinomialNB()
    }
    
    print("\n🔄 Training models...")
    model_results = {}
    
    for name, model in models.items():
        print(f"   Training {name}...")
        
        # Train model
        model.fit(X_train_tfidf, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        cv_scores = cross_val_score(model, X_train_tfidf, y_train, cv=5)
        
        model_results[name] = {
            'model': model,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        print(f"      Accuracy: {accuracy:.3f}, CV: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
    
    # Select best model
    best_model_name = max(model_results.keys(), key=lambda k: model_results[k]['accuracy'])
    best_model = model_results[best_model_name]['model']
    
    print(f"\n🏆 Best model: {best_model_name}")
    print(f"   Accuracy: {model_results[best_model_name]['accuracy']:.3f}")
    
    return best_model, vectorizer, best_model_name, model_results, X_test, y_test

def test_explainable_ai(model, vectorizer, model_name):
    """Test LIME and SHAP explanations"""
    
    print(f"\n🧠 Testing Explainable AI for {model_name}")
    print("=" * 50)
    
    # Test messages
    test_messages = [
        "FREE! Win a $1000 gift card! Click here now!",
        "Hi! Are we still meeting for lunch tomorrow?",
        "URGENT! Your account will be suspended!"
    ]
    
    # Test LIME
    if LIME_AVAILABLE:
        print("\n🔍 Testing LIME explanations...")
        
        lime_explainer = lime.lime_text.LimeTextExplainer(
            class_names=['ham', 'spam'],
            feature_selection='auto'
        )
        
        def predict_fn(texts):
            vectors = vectorizer.transform(texts)
            return model.predict_proba(vectors)
        
        for i, message in enumerate(test_messages):
            print(f"\n   Message {i+1}: {message[:40]}...")
            
            explanation = lime_explainer.explain_instance(
                message, predict_fn, num_features=5, labels=[0, 1]
            )
            
            prediction = predict_fn([message])[0]
            pred_class = 'spam' if prediction[1] > 0.5 else 'ham'
            confidence = max(prediction)
            
            print(f"   Prediction: {pred_class} ({confidence:.3f})")
            print(f"   LIME features:")
            for feature, importance in explanation.as_list():
                direction = "→ SPAM" if importance > 0 else "→ HAM"
                print(f"      {feature}: {importance:.3f} {direction}")
    
    # Test SHAP
    if SHAP_AVAILABLE:
        print("\n🔍 Testing SHAP explanations...")
        
        try:
            if hasattr(model, 'coef_'):
                # Linear model
                sample_data = vectorizer.transform(['sample text'])
                shap_explainer = shap.LinearExplainer(model, sample_data)
                explainer_type = "Linear"
            else:
                # Other models - use a simple approach
                def model_predict(X):
                    return model.predict_proba(X)[:, 1]
                
                background = vectorizer.transform(['sample background text'])
                shap_explainer = shap.KernelExplainer(model_predict, background)
                explainer_type = "Kernel"
            
            print(f"   SHAP {explainer_type} explainer initialized")
            
            for i, message in enumerate(test_messages[:2]):  # Test first 2 messages
                print(f"\n   Message {i+1}: {message[:40]}...")
                
                message_tfidf = vectorizer.transform([message])
                prediction = model.predict_proba(message_tfidf)[0]
                pred_class = 'spam' if prediction[1] > 0.5 else 'ham'
                confidence = max(prediction)
                
                print(f"   Prediction: {pred_class} ({confidence:.3f})")
                
                # Get SHAP values (simplified for demo)
                if explainer_type == "Linear":
                    shap_values = shap_explainer.shap_values(message_tfidf)
                    if isinstance(shap_values, list):
                        shap_values = shap_values[1]  # Spam class
                    
                    feature_names = vectorizer.get_feature_names_out()
                    feature_contributions = list(zip(feature_names, shap_values[0]))
                    feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)
                    
                    print(f"   SHAP top features:")
                    for feature, contribution in feature_contributions[:5]:
                        if abs(contribution) > 0.001:
                            direction = "→ SPAM" if contribution > 0 else "→ HAM"
                            print(f"      {feature}: {contribution:.3f} {direction}")
                
        except Exception as e:
            print(f"   ⚠️  SHAP error: {e}")
    
    print(f"\n✅ Explainable AI testing completed!")

def save_model(model, vectorizer, model_name, model_results):
    """Save the trained model and metadata"""
    
    print(f"\n💾 Saving model and components...")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model and vectorizer
    model_path = f'models/spam_model_{model_name.lower().replace(" ", "_")}.joblib'
    vectorizer_path = 'models/tfidf_vectorizer.joblib'
    metadata_path = 'models/model_metadata.json'
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    
    # Save metadata
    metadata = {
        'model_name': model_name,
        'model_type': type(model).__name__,
        'accuracy': float(model_results[model_name]['accuracy']),
        'cv_mean': float(model_results[model_name]['cv_mean']),
        'cv_std': float(model_results[model_name]['cv_std']),
        'feature_count': len(vectorizer.vocabulary_),
        'lime_available': LIME_AVAILABLE,
        'shap_available': SHAP_AVAILABLE,
        'explainable_ai': True,
        'version': '1.0'
    }
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"   Model saved to: {model_path}")
    print(f"   Vectorizer saved to: {vectorizer_path}")
    print(f"   Metadata saved to: {metadata_path}")
    
    return model_path, vectorizer_path, metadata_path

if __name__ == "__main__":
    # Train models
    model, vectorizer, model_name, results, X_test, y_test = train_models()
    
    # Test explainable AI
    test_explainable_ai(model, vectorizer, model_name)
    
    # Save everything
    save_model(model, vectorizer, model_name, results)
    
    print(f"\n🎉 Training completed successfully!")
    print(f"🎯 Best model: {model_name}")
    print(f"📊 Accuracy: {results[model_name]['accuracy']:.3f}")
    print(f"🔍 Explainable AI: LIME={LIME_AVAILABLE}, SHAP={SHAP_AVAILABLE}")
    print(f"\n💡 Next steps:")
    print(f"   1. Run the backend: python enhanced_backend.py")
    print(f"   2. Test predictions with explainable AI")
    print(f"   3. View explanations in the frontend")
