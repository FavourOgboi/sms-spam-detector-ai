"""
Enhanced SMS Guard Backend with Advanced ML Model Integration
This version is designed to work with your custom ML models
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import hashlib
import uuid
import json
from datetime import datetime
import os
import pickle
import numpy as np

# Explainable AI libraries
try:
    import lime
    import lime.lime_text
    import shap
    LIME_AVAILABLE = True
    SHAP_AVAILABLE = True
    print("✅ LIME and SHAP available for explainable AI")
except ImportError as e:
    LIME_AVAILABLE = False
    SHAP_AVAILABLE = False
    print(f"⚠️  LIME/SHAP not available: {e}")
    print("   Install with: pip install lime shap")

try:
    from sklearn.pipeline import Pipeline
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

# Database setup
DB_FILE = 'smsguard_enhanced.db'

def init_db():
    """Initialize the enhanced database with more ML model fields"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                bio TEXT DEFAULT '',
                theme TEXT DEFAULT 'light',
                profile_image TEXT DEFAULT '',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced predictions table with more ML model details
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                message TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                model_name TEXT DEFAULT 'keyword_based',
                model_version TEXT DEFAULT '1.0',
                processing_time_ms INTEGER DEFAULT 0,
                feature_count INTEGER DEFAULT 0,
                spam_probability REAL DEFAULT 0.0,
                ham_probability REAL DEFAULT 0.0,
                top_features TEXT DEFAULT '[]',
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Model performance tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                model_version TEXT NOT NULL,
                training_accuracy REAL DEFAULT 0.0,
                validation_accuracy REAL DEFAULT 0.0,
                real_time_accuracy REAL DEFAULT 0.0,
                precision REAL DEFAULT 0.0,
                recall REAL DEFAULT 0.0,
                f1_score REAL DEFAULT 0.0,
                total_predictions INTEGER DEFAULT 0,
                correct_predictions INTEGER DEFAULT 0,
                total_feedback INTEGER DEFAULT 0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # User feedback table for real-time accuracy calculation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prediction_feedback (
                id TEXT PRIMARY KEY,
                prediction_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                actual_label TEXT NOT NULL,
                feedback_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prediction_id) REFERENCES predictions (id)
            )
        ''')
        
        # Create demo user if not exists
        cursor.execute('SELECT id FROM users WHERE username = ?', ('demo',))
        if not cursor.fetchone():
            demo_id = str(uuid.uuid4())
            demo_password = hashlib.sha256('demo123'.encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash, bio)
                VALUES (?, ?, ?, ?, ?)
            ''', (demo_id, 'demo', 'demo@example.com', demo_password, 'Demo user for testing'))
            print("✅ Demo user created")
        
        conn.commit()
        conn.close()
        print("✅ Enhanced database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def get_user_from_token(auth_header):
    """Extract user ID from token"""
    if not auth_header or not auth_header.startswith('Bearer token_'):
        return None
    return auth_header.replace('Bearer token_', '')

class ExplainableAI:
    """Proper Explainable AI using LIME and SHAP"""

    def __init__(self, model, vectorizer, model_type="sklearn"):
        self.model = model
        self.vectorizer = vectorizer
        self.model_type = model_type
        self.lime_explainer = None
        self.shap_explainer = None
        self.setup_explainers()

    def setup_explainers(self):
        """Initialize LIME and SHAP explainers with proper model integration"""
        try:
            if LIME_AVAILABLE and self.model and self.vectorizer:
                # Create LIME text explainer
                self.lime_explainer = lime.lime_text.LimeTextExplainer(
                    class_names=['ham', 'spam'],
                    feature_selection='auto',
                    verbose=False,
                    mode='classification'
                )
                print("✅ LIME explainer initialized with trained model")

            if SHAP_AVAILABLE and self.model and self.vectorizer:
                # Initialize SHAP explainer based on model type
                try:
                    if hasattr(self.model, 'coef_'):  # Linear models (LogisticRegression, SVM)
                        # For linear models, use LinearExplainer
                        # Create a small background dataset
                        background_texts = [
                            "this is a normal message",
                            "free money click now",
                            "meeting tomorrow at 3pm"
                        ]
                        background_features = self.vectorizer.transform(background_texts)

                        self.shap_explainer = shap.LinearExplainer(
                            self.model,
                            background_features,
                            feature_perturbation="interventional"
                        )
                        self.shap_type = "Linear"
                        print("✅ SHAP Linear explainer initialized")

                    elif hasattr(self.model, 'feature_importances_'):  # Tree-based models
                        # For tree models, use TreeExplainer
                        self.shap_explainer = shap.TreeExplainer(self.model)
                        self.shap_type = "Tree"
                        print("✅ SHAP Tree explainer initialized")

                    else:
                        # For other models, use KernelExplainer (slower but universal)
                        def model_predict_proba(X):
                            return self.model.predict_proba(X)

                        # Create background dataset
                        background_texts = ["sample text", "another sample", "background message"]
                        background_features = self.vectorizer.transform(background_texts)

                        self.shap_explainer = shap.KernelExplainer(
                            model_predict_proba,
                            background_features,
                            link="logit"
                        )
                        self.shap_type = "Kernel"
                        print("✅ SHAP Kernel explainer initialized")

                except Exception as shap_error:
                    print(f"⚠️  SHAP initialization error: {shap_error}")
                    self.shap_explainer = None

        except Exception as e:
            print(f"⚠️  Error setting up explainers: {e}")
            self.lime_explainer = None
            self.shap_explainer = None

    def explain_prediction_lime(self, text, num_features=10):
        """Generate genuine LIME explanation using the trained model"""
        if not self.lime_explainer or not self.model or not self.vectorizer:
            return None

        try:
            # Create prediction function that uses the actual trained model
            def predict_fn(texts):
                """Prediction function for LIME using the actual model"""
                vectors = self.vectorizer.transform(texts)
                probabilities = self.model.predict_proba(vectors)
                return probabilities

            # Generate LIME explanation using the model's learned patterns
            explanation = self.lime_explainer.explain_instance(
                text,
                predict_fn,
                num_features=num_features,
                labels=[0, 1],  # ham=0, spam=1
                num_samples=1000  # More samples for better explanation
            )

            # Extract feature importance from LIME's analysis
            lime_features = []
            explanation_list = explanation.as_list()

            # Get the actual prediction for context
            actual_prediction = predict_fn([text])[0]
            spam_prob = actual_prediction[1]

            for feature, importance in explanation_list:
                # Check if feature is actually present in the text
                feature_present = feature.lower() in text.lower()

                # Create detailed explanation based on LIME's analysis
                if importance > 0:
                    explanation_text = f"LIME identified '{feature}' as increasing spam probability by {importance:.3f}. This suggests the model learned this pattern from spam training data."
                else:
                    explanation_text = f"LIME identified '{feature}' as decreasing spam probability by {abs(importance):.3f}. This suggests the model associates this pattern with legitimate messages."

                lime_features.append({
                    'feature': feature,
                    'importance': abs(importance),
                    'contribution': importance,
                    'present': feature_present,
                    'explanation': explanation_text,
                    'method': 'LIME',
                    'confidence': abs(importance) / max([abs(imp) for _, imp in explanation_list]) if explanation_list else 0
                })

            # Sort by importance
            lime_features.sort(key=lambda x: x['importance'], reverse=True)

            return lime_features

        except Exception as e:
            print(f"LIME explanation error: {e}")
            return None

    def explain_prediction_shap(self, text, num_features=10):
        """Generate genuine SHAP explanation using the trained model"""
        if not self.shap_explainer or not self.model or not self.vectorizer:
            return None

        try:
            # Transform text to feature vector
            features = self.vectorizer.transform([text])

            # Generate SHAP values based on explainer type
            if self.shap_type == "Linear":
                # For linear models, SHAP values represent feature contributions
                shap_values = self.shap_explainer.shap_values(features)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]  # Get spam class values
                elif len(shap_values.shape) > 1 and shap_values.shape[1] > 1:
                    shap_values = shap_values[:, 1]  # Get spam class

            elif self.shap_type == "Tree":
                # For tree models
                shap_values = self.shap_explainer.shap_values(features)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]  # Get spam class values

            elif self.shap_type == "Kernel":
                # For kernel explainer (slower but works with any model)
                shap_values = self.shap_explainer.shap_values(features, nsamples=100)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]  # Get spam class values
            else:
                return None

            # Get feature names from vectorizer
            feature_names = self.vectorizer.get_feature_names_out()

            # Handle different SHAP value shapes
            if len(shap_values.shape) > 1:
                feature_contributions = list(zip(feature_names, shap_values[0]))
            else:
                feature_contributions = list(zip(feature_names, shap_values))

            # Sort by absolute contribution (most important features first)
            feature_contributions.sort(key=lambda x: abs(x[1]), reverse=True)

            # Get actual prediction for context
            prediction_proba = self.model.predict_proba(features)[0]
            base_value = self.shap_explainer.expected_value if hasattr(self.shap_explainer, 'expected_value') else 0.5

            shap_features = []
            max_contribution = max([abs(contrib) for _, contrib in feature_contributions]) if feature_contributions else 1

            for feature, contribution in feature_contributions[:num_features]:
                if abs(contribution) > 0.001:  # Only include meaningful contributions
                    # Check if feature is present in text
                    feature_present = feature.lower() in text.lower()

                    # Create detailed explanation
                    if contribution > 0:
                        explanation_text = f"SHAP analysis: '{feature}' contributes +{contribution:.3f} toward spam classification. The model learned this pattern increases spam likelihood."
                    else:
                        explanation_text = f"SHAP analysis: '{feature}' contributes {contribution:.3f} toward ham classification. The model learned this pattern indicates legitimate messages."

                    # Add context about the contribution magnitude
                    contribution_strength = abs(contribution) / max_contribution
                    if contribution_strength > 0.7:
                        strength_desc = "strong"
                    elif contribution_strength > 0.3:
                        strength_desc = "moderate"
                    else:
                        strength_desc = "weak"

                    shap_features.append({
                        'feature': feature,
                        'importance': abs(contribution),
                        'contribution': contribution,
                        'present': feature_present,
                        'explanation': explanation_text,
                        'method': 'SHAP',
                        'strength': strength_desc,
                        'base_value': base_value,
                        'confidence': contribution_strength
                    })

            return shap_features

        except Exception as e:
            print(f"SHAP explanation error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_comprehensive_explanation(self, text, num_features=10):
        """Get explanation using both LIME and SHAP if available"""
        explanations = []

        # Try LIME first
        lime_explanation = self.explain_prediction_lime(text, num_features)
        if lime_explanation:
            explanations.extend(lime_explanation)

        # Try SHAP
        shap_explanation = self.explain_prediction_shap(text, num_features)
        if shap_explanation:
            explanations.extend(shap_explanation)

        # If we have both, combine and deduplicate
        if lime_explanation and shap_explanation:
            # Combine explanations by feature name
            combined = {}
            for exp in explanations:
                feature = exp['feature']
                if feature not in combined:
                    combined[feature] = exp
                    combined[feature]['methods'] = [exp['method']]
                else:
                    # Average the importance scores
                    combined[feature]['importance'] = (
                        combined[feature]['importance'] + exp['importance']
                    ) / 2
                    combined[feature]['methods'].append(exp['method'])
                    combined[feature]['explanation'] = f"Both LIME and SHAP identify this as important (avg importance: {combined[feature]['importance']:.3f})"

            explanations = list(combined.values())

        # Sort by importance
        explanations.sort(key=lambda x: x['importance'], reverse=True)

        return explanations[:num_features]

class MLModelInterface:
    """Interface for integrating your custom ML models with Explainable AI"""

    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_name = "keyword_based"
        self.model_version = "1.0"
        self.training_accuracy = 0.85  # Default for keyword-based
        self.validation_accuracy = 0.85
        self.explainer = None  # Will hold ExplainableAI instance
        self.load_model()
        self.update_model_performance()
    
    def load_model(self):
        """Load trained ML model with explainable AI capabilities"""
        try:
            # Try to load the trained model (joblib format)
            vectorizer_path = 'models/tfidf_vectorizer.joblib'
            metadata_path = 'models/model_metadata.json'

            # Look for any trained model file
            model_files = [
                'models/spam_model_logistic_regression.joblib',
                'models/spam_model_random_forest.joblib',
                'models/spam_model_naive_bayes.joblib',
                'models/spam_model.pkl'  # Fallback to pickle
            ]

            model_path = None
            for path in model_files:
                if os.path.exists(path):
                    model_path = path
                    break

            if model_path and os.path.exists(vectorizer_path):
                # Load model
                if model_path.endswith('.joblib'):
                    self.model = joblib.load(model_path)
                    self.vectorizer = joblib.load(vectorizer_path)
                else:
                    # Fallback to pickle
                    with open(model_path, 'rb') as f:
                        self.model = pickle.load(f)
                    with open(vectorizer_path.replace('.joblib', '.pkl'), 'rb') as f:
                        self.vectorizer = pickle.load(f)

                # Load model metadata
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        self.model_name = metadata.get('model_name', 'Trained ML Model')
                        self.model_version = metadata.get('version', '1.0')
                        self.training_accuracy = metadata.get('accuracy', 0.95)
                        self.validation_accuracy = metadata.get('cv_mean', 0.93)
                        self.feature_count = metadata.get('feature_count', 1000)

                        print(f"✅ Model loaded: {self.model_name} v{self.model_version}")
                        print(f"   Type: {metadata.get('model_type', 'Unknown')}")
                        print(f"   Accuracy: {self.training_accuracy:.3f}")
                        print(f"   CV Score: {self.validation_accuracy:.3f}")
                        print(f"   Features: {self.feature_count}")

                        # Check explainable AI availability
                        lime_available = metadata.get('lime_available', False)
                        shap_available = metadata.get('shap_available', False)
                        print(f"   Explainable AI: LIME={lime_available}, SHAP={shap_available}")
                else:
                    self.model_name = "Trained ML Model"
                    self.model_version = "1.0"
                    self.training_accuracy = 0.95
                    self.validation_accuracy = 0.93
                    self.feature_count = len(self.vectorizer.vocabulary_) if hasattr(self.vectorizer, 'vocabulary_') else 1000

                print("✅ Trained ML model loaded successfully")

                # Initialize Explainable AI with the trained model
                if LIME_AVAILABLE or SHAP_AVAILABLE:
                    self.explainer = ExplainableAI(self.model, self.vectorizer)
                    print("✅ Explainable AI initialized with trained model")
                    print(f"   Model type: {type(self.model).__name__}")
                    print(f"   Features: {len(self.vectorizer.vocabulary_) if hasattr(self.vectorizer, 'vocabulary_') else 'Unknown'}")
                else:
                    print("⚠️  LIME/SHAP not available")
                    print("   Install with: pip install lime shap")

            else:
                print("⚠️  Trained model not found")
                print("   Run: python train_explainable_model.py")
                print("   Using keyword-based fallback")

        except Exception as e:
            print(f"⚠️  Failed to load trained model: {e}")
            print("   Using keyword-based fallback")
            import traceback
            traceback.print_exc()
    
    def predict(self, message):
        """Make prediction with detailed results"""
        import time
        start_time = time.time()
        
        if self.model and self.vectorizer:
            # Use your custom ML model
            return self._predict_with_ml_model(message, start_time)
        else:
            # Fallback to keyword-based prediction
            return self._predict_with_keywords(message, start_time)
    
    def _predict_with_ml_model(self, message, start_time):
        """Prediction using your custom ML model"""
        try:
            # Preprocess message
            processed_message = self._preprocess_text(message)
            
            # Vectorize
            features = self.vectorizer.transform([processed_message])
            
            # Get prediction and probabilities
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Get proper explainable AI results
            if self.explainer:
                # Use LIME/SHAP for real explanations
                top_features = self.explainer.get_comprehensive_explanation(message, num_features=5)
            else:
                # Fallback to basic feature extraction
                top_features = self._get_top_features(features, message)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                'prediction': 'spam' if prediction == 1 else 'ham',
                'confidence': float(max(probabilities)),
                'spam_probability': float(probabilities[1] if len(probabilities) > 1 else probabilities[0]),
                'ham_probability': float(probabilities[0] if len(probabilities) > 1 else 1 - probabilities[0]),
                'model_name': self.model_name,
                'model_version': self.model_version,
                'processing_time_ms': processing_time,
                'feature_count': features.shape[1],
                'top_features': top_features
            }
        except Exception as e:
            print(f"ML model prediction error: {e}")
            return self._predict_with_keywords(message, start_time)
    
    def _predict_with_keywords(self, message, start_time):
        """Fallback keyword-based prediction with explanations"""
        spam_words = ['free', 'win', 'winner', 'urgent', 'click', 'now', 'limited', 'offer', 'prize', 'money', 'cash']
        message_lower = message.lower()

        # Find matching spam words and create explanations
        found_spam_words = [word for word in spam_words if word in message_lower]
        spam_count = len(found_spam_words)

        is_spam = spam_count >= 2
        confidence = min(0.6 + (spam_count * 0.1), 0.95) if is_spam else max(0.4, 0.95 - (spam_count * 0.1))

        processing_time = int((time.time() - start_time) * 1000)

        # Create detailed explanations
        explanations = []

        if is_spam:
            # Explain why it's spam
            for word in found_spam_words:
                explanations.append({
                    'feature': word,
                    'importance': 1.0 / len(found_spam_words),  # Equal weight for keyword model
                    'present': True,
                    'explanation': self._explain_feature(word, message)
                })

            # Add overall explanation
            if spam_count >= 3:
                overall_explanation = f"Message contains {spam_count} spam indicators ({', '.join(found_spam_words)}), strongly suggesting spam"
            else:
                overall_explanation = f"Message contains {spam_count} spam indicators ({', '.join(found_spam_words)}), indicating likely spam"
        else:
            # Explain why it's ham
            if spam_count == 1:
                explanations.append({
                    'feature': found_spam_words[0],
                    'importance': 0.5,
                    'present': True,
                    'explanation': f"Only one spam indicator ('{found_spam_words[0]}') found, insufficient for spam classification"
                })
                overall_explanation = f"Only one potential spam word found ('{found_spam_words[0]}'), message appears legitimate"
            elif spam_count == 0:
                # Look for positive ham indicators
                ham_words = ['thanks', 'please', 'meeting', 'time', 'today', 'work', 'family', 'friend']
                found_ham_words = [word for word in ham_words if word in message_lower]

                if found_ham_words:
                    for word in found_ham_words[:3]:  # Top 3 ham indicators
                        explanations.append({
                            'feature': word,
                            'importance': 1.0 / len(found_ham_words),
                            'present': True,
                            'explanation': self._explain_feature(word, message)
                        })
                    overall_explanation = f"Message contains legitimate language patterns ({', '.join(found_ham_words[:3])})"
                else:
                    overall_explanation = "No spam indicators detected, message appears to be normal communication"
            else:
                overall_explanation = f"Insufficient spam indicators ({spam_count}) for spam classification"

        # Add overall explanation as the first item
        explanations.insert(0, {
            'feature': 'overall_assessment',
            'importance': 1.0,
            'present': True,
            'explanation': overall_explanation
        })

        return {
            'prediction': 'spam' if is_spam else 'ham',
            'confidence': confidence,
            'spam_probability': confidence if is_spam else 1 - confidence,
            'ham_probability': 1 - confidence if is_spam else confidence,
            'model_name': self.model_name,
            'model_version': self.model_version,
            'processing_time_ms': processing_time,
            'feature_count': len(spam_words),
            'top_features': explanations
        }
    
    def _preprocess_text(self, text):
        """Preprocess text for ML model"""
        import re
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = ' '.join(text.split())
        return text
    
    def _get_top_features(self, features, message_text=""):
        """Get top contributing features with explanations"""
        try:
            explanations = []

            if hasattr(self.model, 'feature_importances_'):
                # For tree-based models
                importances = self.model.feature_importances_
                top_indices = np.argsort(importances)[-5:][::-1]

                if hasattr(self.vectorizer, 'get_feature_names_out'):
                    feature_names = self.vectorizer.get_feature_names_out()
                    for idx in top_indices:
                        if idx < len(feature_names):
                            feature_name = feature_names[idx]
                            explanations.append({
                                'feature': feature_name,
                                'importance': float(importances[idx]),
                                'present': feature_name.lower() in message_text.lower(),
                                'explanation': self._explain_feature(feature_name, message_text)
                            })

            elif hasattr(self.vectorizer, 'get_feature_names_out'):
                # For text models with vectorizer
                feature_names = self.vectorizer.get_feature_names_out()
                non_zero = features.nonzero()[1]
                feature_values = features.data

                # Get top features by value
                if len(non_zero) > 0:
                    top_features = sorted(zip(non_zero, feature_values), key=lambda x: x[1], reverse=True)[:5]

                    for feature_idx, feature_value in top_features:
                        if feature_idx < len(feature_names):
                            feature_name = feature_names[feature_idx]
                            explanations.append({
                                'feature': feature_name,
                                'importance': float(feature_value),
                                'present': True,
                                'explanation': self._explain_feature(feature_name, message_text)
                            })

            return explanations[:5]  # Return top 5 explanations

        except Exception as e:
            print(f"Feature extraction error: {e}")
            return []

    def _explain_feature(self, feature, message_text):
        """Generate human-readable explanation for a feature"""
        feature_lower = feature.lower()
        message_lower = message_text.lower()

        # Common spam indicators
        spam_indicators = {
            'free': "The word 'free' is commonly used in spam messages to attract attention",
            'win': "Words like 'win' often appear in scam messages promising prizes",
            'winner': "Claiming someone is a 'winner' is a classic spam tactic",
            'urgent': "Creating urgency is a common manipulation technique in spam",
            'click': "Spam messages often ask users to click on suspicious links",
            'now': "Words like 'now' create false urgency typical of spam",
            'limited': "Claims of 'limited' offers are common in promotional spam",
            'offer': "Unsolicited offers are a hallmark of spam messages",
            'prize': "Prize notifications are frequently used in scam messages",
            'money': "Mentions of money often indicate financial scams",
            'cash': "Cash-related terms are red flags for spam content",
            'congratulations': "Fake congratulations are used to make spam seem legitimate",
            'call': "Spam often includes suspicious phone numbers to call",
            'text': "Instructions to text back are common in SMS spam",
            'stop': "Ironically, 'stop' instructions can indicate spam messages",
            'reply': "Requests to reply are often used to confirm active phone numbers"
        }

        # Common ham (legitimate) indicators
        ham_indicators = {
            'meeting': "Business-related words like 'meeting' suggest legitimate communication",
            'thanks': "Polite expressions like 'thanks' are common in genuine messages",
            'please': "Courteous language indicates normal conversation",
            'time': "References to time often appear in legitimate scheduling messages",
            'today': "Date references suggest real plans or appointments",
            'tomorrow': "Future planning indicates genuine communication",
            'work': "Work-related terms suggest legitimate business communication",
            'home': "Personal location references are common in real messages",
            'family': "Family-related content typically indicates genuine messages",
            'friend': "References to friends suggest personal communication",
            'love': "Emotional expressions often appear in genuine personal messages",
            'sorry': "Apologies are common in real human communication",
            'help': "Genuine requests for help differ from spam 'help' claims"
        }

        # Check for exact matches first
        if feature_lower in spam_indicators:
            return spam_indicators[feature_lower]
        elif feature_lower in ham_indicators:
            return ham_indicators[feature_lower]

        # Check for partial matches
        for spam_word, explanation in spam_indicators.items():
            if spam_word in feature_lower or feature_lower in spam_word:
                return explanation

        for ham_word, explanation in ham_indicators.items():
            if ham_word in feature_lower or feature_lower in ham_word:
                return explanation

        # Handle n-grams and compound features
        if len(feature_lower.split()) > 1:
            return f"The phrase '{feature}' was identified as significant by the model"

        # Check for numbers, URLs, phone patterns
        if any(char.isdigit() for char in feature):
            if 'http' in feature_lower or 'www' in feature_lower:
                return "URLs in messages can indicate spam, especially unsolicited links"
            elif len([c for c in feature if c.isdigit()]) >= 3:
                return "Phone numbers or codes in messages may indicate spam"
            else:
                return "Numeric content was flagged as potentially suspicious"

        # Check for special characters
        if any(char in feature for char in ['!', '$', '%', '*']):
            return "Special characters like '!' or '$' are often used to grab attention in spam"

        # Default explanation
        if feature_lower in message_lower:
            return f"The model identified '{feature}' as a significant indicator based on training data"
        else:
            return f"The absence or low frequency of '{feature}' influenced the prediction"

    def update_model_performance(self):
        """Update model performance in database"""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Check if model performance record exists
            cursor.execute('''
                SELECT id FROM model_performance
                WHERE model_name = ? AND model_version = ?
            ''', (self.model_name, self.model_version))

            existing = cursor.fetchone()

            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE model_performance
                    SET training_accuracy = ?, validation_accuracy = ?, last_updated = ?
                    WHERE model_name = ? AND model_version = ?
                ''', (self.training_accuracy, self.validation_accuracy,
                      datetime.now().isoformat(), self.model_name, self.model_version))
            else:
                # Create new record
                cursor.execute('''
                    INSERT INTO model_performance (
                        id, model_name, model_version, training_accuracy,
                        validation_accuracy, last_updated
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (str(uuid.uuid4()), self.model_name, self.model_version,
                      self.training_accuracy, self.validation_accuracy,
                      datetime.now().isoformat()))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Failed to update model performance: {e}")

    def calculate_real_time_accuracy(self):
        """Calculate real-time accuracy based on user feedback"""
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()

            # Get feedback for this model
            cursor.execute('''
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN p.prediction = f.actual_label THEN 1 ELSE 0 END) as correct
                FROM prediction_feedback f
                JOIN predictions p ON f.prediction_id = p.id
                WHERE p.model_name = ? AND p.model_version = ?
            ''', (self.model_name, self.model_version))

            result = cursor.fetchone()
            conn.close()

            if result and result[0] > 0:
                return result[1] / result[0]  # correct / total
            else:
                return None  # No feedback available

        except Exception as e:
            print(f"Failed to calculate real-time accuracy: {e}")
            return None

# Initialize ML model interface
ml_model = MLModelInterface()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'success': True, 
        'message': 'Enhanced Backend is running!',
        'model_info': {
            'name': ml_model.model_name,
            'version': ml_model.model_version,
            'custom_model_loaded': ml_model.model is not None
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'All fields required'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Username or email already exists'}), 409

        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('''
            INSERT INTO users (id, username, email, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (user_id, username, email, password_hash))

        conn.commit()
        conn.close()

        token = f"token_{user_id}"
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
            'profileImage': '',
            'bio': '',
            'memberSince': datetime.now().strftime('%Y-%m-%d'),
            'isAuthenticated': True,
            'theme': 'light'
        }

        return jsonify({'success': True, 'data': {'token': token, 'user': user_data}}), 201

    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username_or_email = data.get('usernameOrEmail', '').strip()
        password = data.get('password', '')

        if not username_or_email or not password:
            return jsonify({'success': False, 'error': 'Username/email and password required'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        if '@' in username_or_email:
            cursor.execute('SELECT * FROM users WHERE email = ?', (username_or_email.lower(),))
        else:
            cursor.execute('SELECT * FROM users WHERE username = ?', (username_or_email,))

        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 401

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user[3]:
            return jsonify({'success': False, 'error': 'Invalid password'}), 401

        token = f"token_{user[0]}"
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'profileImage': user[6] or '',
            'bio': user[4] or '',
            'memberSince': user[7][:10] if user[7] else datetime.now().strftime('%Y-%m-%d'),
            'isAuthenticated': True,
            'theme': user[5] or 'light'
        }

        return jsonify({'success': True, 'data': {'token': token, 'user': user_data}}), 200

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'error': 'Login failed'}), 500

@app.route('/api/auth/me', methods=['GET'])
def get_me():
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'profileImage': user[6] or '',
            'bio': user[4] or '',
            'memberSince': user[7][:10] if user[7] else datetime.now().strftime('%Y-%m-%d'),
            'isAuthenticated': True,
            'theme': user[5] or 'light'
        }

        return jsonify({'success': True, 'data': user_data}), 200

    except Exception as e:
        print(f"Get me error: {e}")
        return jsonify({'success': False, 'error': 'Failed to get user'}), 500

@app.route('/api/user/profile', methods=['PUT'])
def update_profile():
    """Update user profile information"""
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        bio = data.get('bio', '').strip()
        profile_image = data.get('profileImage', '').strip()

        if not username or not email:
            return jsonify({'success': False, 'error': 'Username and email are required'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Check if username or email already exists for other users
        cursor.execute('''
            SELECT id FROM users
            WHERE (username = ? OR email = ?) AND id != ?
        ''', (username, email, user_id))

        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Username or email already exists'}), 409

        # Update user profile
        cursor.execute('''
            UPDATE users
            SET username = ?, email = ?, bio = ?, profile_image = ?
            WHERE id = ?
        ''', (username, email, bio, profile_image, user_id))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Get updated user data
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()

        if user:
            user_data = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'profileImage': user[6] or '',
                'bio': user[4] or '',
                'memberSince': user[7][:10] if user[7] else datetime.now().strftime('%Y-%m-%d'),
                'isAuthenticated': True,
                'theme': user[5] or 'light'
            }

            return jsonify({'success': True, 'data': user_data}), 200
        else:
            return jsonify({'success': False, 'error': 'Failed to get updated user data'}), 500

    except Exception as e:
        print(f"Update profile error: {e}")
        return jsonify({'success': False, 'error': 'Failed to update profile'}), 500

@app.route('/api/user/password', methods=['PUT'])
def change_password():
    """Change user password"""
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        current_password = data.get('currentPassword', '')
        new_password = data.get('newPassword', '')

        if not current_password or not new_password:
            return jsonify({'success': False, 'error': 'Current and new passwords are required'}), 400

        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'New password must be at least 6 characters'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Verify current password
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify({'success': False, 'error': 'User not found'}), 404

        current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
        if current_password_hash != user[0]:
            conn.close()
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 401

        # Update password
        new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_password_hash, user_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Password updated successfully'}), 200

    except Exception as e:
        print(f"Change password error: {e}")
        return jsonify({'success': False, 'error': 'Failed to change password'}), 500

@app.route('/api/user/delete', methods=['DELETE'])
def delete_account():
    """Delete user account and all associated data"""
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        data = request.get_json()
        password = data.get('password', '') if data else ''

        if not password:
            return jsonify({'success': False, 'error': 'Password confirmation required'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Verify password
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return jsonify({'success': False, 'error': 'User not found'}), 404

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user[0]:
            conn.close()
            return jsonify({'success': False, 'error': 'Incorrect password'}), 401

        # Delete user predictions
        cursor.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))

        # Delete user account
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Account deleted successfully'}), 200

    except Exception as e:
        print(f"Delete account error: {e}")
        return jsonify({'success': False, 'error': 'Failed to delete account'}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
            
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Message required'}), 400
        
        # Make enhanced prediction with your ML model
        prediction_result = ml_model.predict(message)
        
        # Save enhanced prediction to database
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        pred_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO predictions (
                id, user_id, message, prediction, confidence,
                model_name, model_version, processing_time_ms, feature_count,
                spam_probability, ham_probability, top_features, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pred_id, user_id, message, 
            prediction_result['prediction'], prediction_result['confidence'],
            prediction_result['model_name'], prediction_result['model_version'],
            prediction_result['processing_time_ms'], prediction_result['feature_count'],
            prediction_result['spam_probability'], prediction_result['ham_probability'],
            json.dumps(prediction_result['top_features']), timestamp
        ))
        
        conn.commit()
        conn.close()
        
        # Return enhanced result
        # Ensure topFeatures is properly formatted for frontend
        top_features = prediction_result.get('top_features', [])
        if isinstance(top_features, list) and len(top_features) > 0:
            # Check if it's the new format with explanation objects
            if isinstance(top_features[0], dict) and 'explanation' in top_features[0]:
                formatted_features = top_features
            else:
                # Convert old format (list of strings) to new format
                formatted_features = []
                for feature in top_features:
                    if isinstance(feature, str):
                        formatted_features.append({
                            'feature': feature,
                            'importance': 0.5,  # Default importance
                            'present': True,
                            'explanation': f"The word '{feature}' was identified as significant",
                            'method': 'KEYWORD'
                        })
                    else:
                        formatted_features.append(feature)
        else:
            formatted_features = []

        result = {
            'id': pred_id,
            'message': message,
            'prediction': prediction_result['prediction'],
            'confidence': round(prediction_result['confidence'], 4),
            'spamProbability': round(prediction_result['spam_probability'], 4),
            'hamProbability': round(prediction_result['ham_probability'], 4),
            'modelName': prediction_result['model_name'],
            'modelVersion': prediction_result['model_version'],
            'processingTimeMs': prediction_result['processing_time_ms'],
            'featureCount': prediction_result['feature_count'],
            'topFeatures': formatted_features,
            'timestamp': timestamp + 'Z',
            'userId': user_id
        }
        
        return jsonify({'success': True, 'data': result}), 200

    except Exception as e:
        print(f"Enhanced prediction error: {e}")
        return jsonify({'success': False, 'error': 'Prediction failed'}), 500

@app.route('/api/user/stats', methods=['GET'])
def get_enhanced_stats():
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Get all predictions with enhanced data
        cursor.execute('''
            SELECT * FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        predictions = cursor.fetchall()

        # Get model performance data (keep connection open)
        try:
            cursor.execute('''
                SELECT training_accuracy, validation_accuracy, real_time_accuracy
                FROM model_performance
                WHERE model_name = ? AND model_version = ?
            ''', (ml_model.model_name, ml_model.model_version))
            model_perf = cursor.fetchone()
        except sqlite3.OperationalError:
            # Table doesn't exist or other error, use defaults
            model_perf = None

        conn.close()

        if not predictions:
            # Get accuracy from model performance or use defaults
            accuracy_data = {
                'trainingAccuracy': model_perf[0] if model_perf else ml_model.training_accuracy,
                'validationAccuracy': model_perf[1] if model_perf else ml_model.validation_accuracy,
                'realTimeAccuracy': model_perf[2] if model_perf and model_perf[2] else None
            }

            return jsonify({
                'success': True,
                'data': {
                    'totalMessages': 0,
                    'spamCount': 0,
                    'hamCount': 0,
                    'accuracyData': accuracy_data,
                    'spamRate': 0,
                    'avgConfidence': 0,
                    'avgProcessingTime': 0,
                    'modelStats': {},
                    'recentPredictions': []
                }
            }), 200

        # Calculate basic stats
        total_messages = len(predictions)
        spam_count = len([p for p in predictions if p[3] == 'spam'])
        ham_count = total_messages - spam_count
        spam_rate = spam_count / total_messages if total_messages > 0 else 0

        # Calculate enhanced stats
        confidences = [p[4] for p in predictions]  # confidence column
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        processing_times = [p[7] for p in predictions if p[7]]  # processing_time_ms column
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0

        # Model performance stats
        model_stats = {}
        for prediction in predictions:
            model_name = prediction[5] or 'unknown'  # model_name column
            if model_name not in model_stats:
                model_stats[model_name] = {
                    'count': 0,
                    'avgConfidence': 0,
                    'spamCount': 0,
                    'hamCount': 0
                }

            model_stats[model_name]['count'] += 1
            model_stats[model_name]['avgConfidence'] += prediction[4]  # confidence
            if prediction[3] == 'spam':  # prediction column
                model_stats[model_name]['spamCount'] += 1
            else:
                model_stats[model_name]['hamCount'] += 1

        # Calculate averages for model stats
        for model_name in model_stats:
            count = model_stats[model_name]['count']
            model_stats[model_name]['avgConfidence'] = round(
                model_stats[model_name]['avgConfidence'] / count, 4
            ) if count > 0 else 0

        # Recent predictions with enhanced data
        recent = []
        for p in predictions[:10]:
            try:
                top_features = json.loads(p[11]) if p[11] else []  # top_features column
            except:
                top_features = []

            recent.append({
                'id': p[0],
                'message': p[2],
                'prediction': p[3],
                'confidence': p[4],
                'spamProbability': p[9] if p[9] is not None else 0,  # spam_probability
                'hamProbability': p[10] if p[10] is not None else 0,  # ham_probability
                'modelName': p[5] or 'unknown',
                'modelVersion': p[6] or '1.0',
                'processingTimeMs': p[7] or 0,
                'featureCount': p[8] or 0,
                'topFeatures': top_features,
                'timestamp': p[12] + 'Z' if not p[12].endswith('Z') else p[12],
                'userId': p[1]
            })

        # Calculate real-time accuracy if feedback is available
        real_time_accuracy = ml_model.calculate_real_time_accuracy()

        # Prepare accuracy data
        accuracy_data = {
            'trainingAccuracy': model_perf[0] if model_perf else ml_model.training_accuracy,
            'validationAccuracy': model_perf[1] if model_perf else ml_model.validation_accuracy,
            'realTimeAccuracy': real_time_accuracy
        }

        # Enhanced stats response
        stats = {
            'totalMessages': total_messages,
            'spamCount': spam_count,
            'hamCount': ham_count,
            'accuracyData': accuracy_data,
            'spamRate': round(spam_rate, 4),
            'avgConfidence': round(avg_confidence, 4),
            'avgProcessingTime': round(avg_processing_time, 2),
            'modelStats': model_stats,
            'recentPredictions': recent
        }

        return jsonify({'success': True, 'data': stats}), 200

    except Exception as e:
        print(f"Enhanced stats error: {e}")
        return jsonify({'success': False, 'error': 'Failed to get enhanced stats'}), 500

@app.route('/api/user/predictions', methods=['GET'])
def get_enhanced_predictions():
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        predictions = cursor.fetchall()
        conn.close()

        result = []
        for p in predictions:
            try:
                top_features = json.loads(p[11]) if p[11] else []
            except:
                top_features = []

            result.append({
                'id': p[0],
                'message': p[2],
                'prediction': p[3],
                'confidence': p[4],
                'spamProbability': p[9] if p[9] is not None else 0,
                'hamProbability': p[10] if p[10] is not None else 0,
                'modelName': p[5] or 'unknown',
                'modelVersion': p[6] or '1.0',
                'processingTimeMs': p[7] or 0,
                'featureCount': p[8] or 0,
                'topFeatures': top_features,
                'timestamp': p[12] + 'Z' if not p[12].endswith('Z') else p[12],
                'userId': p[1]
            })

        return jsonify({'success': True, 'data': result}), 200

    except Exception as e:
        print(f"Enhanced predictions error: {e}")
        return jsonify({'success': False, 'error': 'Failed to get enhanced predictions'}), 500

@app.route('/api/prediction/feedback', methods=['POST'])
def submit_prediction_feedback():
    """Submit feedback for a prediction to calculate real-time accuracy"""
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        prediction_id = data.get('predictionId')
        actual_label = data.get('actualLabel')  # 'spam' or 'ham'

        if not prediction_id or not actual_label:
            return jsonify({'success': False, 'error': 'Prediction ID and actual label required'}), 400

        if actual_label not in ['spam', 'ham']:
            return jsonify({'success': False, 'error': 'Actual label must be spam or ham'}), 400

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Verify prediction belongs to user
        cursor.execute('SELECT id FROM predictions WHERE id = ? AND user_id = ?', (prediction_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Prediction not found'}), 404

        # Check if feedback already exists
        cursor.execute('SELECT id FROM prediction_feedback WHERE prediction_id = ?', (prediction_id,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'success': False, 'error': 'Feedback already submitted for this prediction'}), 409

        # Insert feedback
        feedback_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO prediction_feedback (id, prediction_id, user_id, actual_label)
            VALUES (?, ?, ?, ?)
        ''', (feedback_id, prediction_id, user_id, actual_label))

        conn.commit()
        conn.close()

        # Update real-time accuracy in model performance
        real_time_accuracy = ml_model.calculate_real_time_accuracy()
        if real_time_accuracy is not None:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE model_performance
                SET real_time_accuracy = ?, last_updated = ?
                WHERE model_name = ? AND model_version = ?
            ''', (real_time_accuracy, datetime.now().isoformat(),
                  ml_model.model_name, ml_model.model_version))
            conn.commit()
            conn.close()

        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully',
            'realTimeAccuracy': real_time_accuracy
        }), 200

    except Exception as e:
        print(f"Feedback submission error: {e}")
        return jsonify({'success': False, 'error': 'Failed to submit feedback'}), 500

@app.route('/api/model/accuracy', methods=['GET'])
def get_model_accuracy():
    """Get detailed model accuracy information"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM model_performance
            WHERE model_name = ? AND model_version = ?
        ''', (ml_model.model_name, ml_model.model_version))

        model_perf = cursor.fetchone()
        conn.close()

        if model_perf:
            accuracy_info = {
                'modelName': model_perf[1],
                'modelVersion': model_perf[2],
                'trainingAccuracy': model_perf[3],
                'validationAccuracy': model_perf[4],
                'realTimeAccuracy': model_perf[5],
                'precision': model_perf[6],
                'recall': model_perf[7],
                'f1Score': model_perf[8],
                'totalPredictions': model_perf[9],
                'correctPredictions': model_perf[10],
                'totalFeedback': model_perf[11],
                'lastUpdated': model_perf[12]
            }
        else:
            accuracy_info = {
                'modelName': ml_model.model_name,
                'modelVersion': ml_model.model_version,
                'trainingAccuracy': ml_model.training_accuracy,
                'validationAccuracy': ml_model.validation_accuracy,
                'realTimeAccuracy': None,
                'precision': None,
                'recall': None,
                'f1Score': None,
                'totalPredictions': 0,
                'correctPredictions': 0,
                'totalFeedback': 0,
                'lastUpdated': datetime.now().isoformat()
            }

        return jsonify({'success': True, 'data': accuracy_info}), 200

    except Exception as e:
        print(f"Model accuracy error: {e}")
        return jsonify({'success': False, 'error': 'Failed to get model accuracy'}), 500

@app.route('/api/model/insights', methods=['GET'])
def get_model_insights():
    """Get AI-powered insights about model performance"""
    try:
        user_id = get_user_from_token(request.headers.get('Authorization', ''))
        if not user_id:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Get model performance data
        cursor.execute('''
            SELECT * FROM model_performance
            WHERE model_name = ? AND model_version = ?
        ''', (ml_model.model_name, ml_model.model_version))
        model_perf = cursor.fetchone()

        # Get user's prediction data
        cursor.execute('''
            SELECT prediction, confidence, processing_time_ms, timestamp
            FROM predictions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 100
        ''', (user_id,))
        predictions = cursor.fetchall()

        # Get feedback data
        cursor.execute('''
            SELECT COUNT(*) as total_feedback,
                   SUM(CASE WHEN p.prediction = f.actual_label THEN 1 ELSE 0 END) as correct_feedback
            FROM prediction_feedback f
            JOIN predictions p ON f.prediction_id = p.id
            WHERE p.user_id = ?
        ''', (user_id,))
        feedback_data = cursor.fetchone()

        conn.close()

        insights = []

        # Performance stability analysis
        if model_perf:
            training_acc = model_perf[3] or 0
            validation_acc = model_perf[4] or 0
            realtime_acc = model_perf[5]

            # Overfitting check
            if training_acc > 0 and validation_acc > 0:
                overfitting = training_acc - validation_acc
                if overfitting > 0.05:
                    insights.append({
                        'type': 'warning',
                        'category': 'model_stability',
                        'title': 'Potential Overfitting Detected',
                        'message': f'Training accuracy ({training_acc:.1%}) significantly exceeds validation accuracy ({validation_acc:.1%}). Model may not generalize well.',
                        'recommendation': 'Consider regularization techniques or more diverse training data.',
                        'severity': 'medium'
                    })
                elif overfitting < 0.02:
                    insights.append({
                        'type': 'success',
                        'category': 'model_stability',
                        'title': 'Well-Balanced Model',
                        'message': 'Training and validation accuracies are well-aligned, indicating good generalization.',
                        'recommendation': 'Model appears stable and ready for production use.',
                        'severity': 'low'
                    })

            # Data drift analysis
            if realtime_acc and validation_acc:
                drift = validation_acc - realtime_acc
                if drift > 0.05:
                    insights.append({
                        'type': 'warning',
                        'category': 'data_drift',
                        'title': 'Data Drift Detected',
                        'message': f'Real-world performance ({realtime_acc:.1%}) is significantly lower than expected ({validation_acc:.1%}).',
                        'recommendation': 'Consider retraining the model with more recent data or investigating data quality issues.',
                        'severity': 'high'
                    })
                elif drift < -0.02:
                    insights.append({
                        'type': 'success',
                        'category': 'data_drift',
                        'title': 'Excellent Real-World Performance',
                        'message': f'Model performs better in practice ({realtime_acc:.1%}) than in testing ({validation_acc:.1%})!',
                        'recommendation': 'Great job! Your model is performing exceptionally well on real data.',
                        'severity': 'low'
                    })

        # Confidence analysis
        if predictions:
            confidences = [p[1] for p in predictions if p[1] is not None]
            if confidences:
                avg_confidence = sum(confidences) / len(confidences)
                low_confidence_count = len([c for c in confidences if c < 0.7])
                low_confidence_rate = low_confidence_count / len(confidences)

                if avg_confidence < 0.7:
                    insights.append({
                        'type': 'warning',
                        'category': 'confidence',
                        'title': 'Low Model Confidence',
                        'message': f'Average prediction confidence is {avg_confidence:.1%}, which may indicate model uncertainty.',
                        'recommendation': 'Consider collecting more training data or feature engineering to improve model confidence.',
                        'severity': 'medium'
                    })
                elif low_confidence_rate > 0.3:
                    insights.append({
                        'type': 'info',
                        'category': 'confidence',
                        'title': 'Mixed Confidence Levels',
                        'message': f'{low_confidence_rate:.1%} of predictions have low confidence (<70%).',
                        'recommendation': 'Review low-confidence predictions to identify patterns or edge cases.',
                        'severity': 'low'
                    })
                else:
                    insights.append({
                        'type': 'success',
                        'category': 'confidence',
                        'title': 'High Model Confidence',
                        'message': f'Model shows strong confidence with {avg_confidence:.1%} average confidence.',
                        'recommendation': 'Excellent! Your model is making confident predictions.',
                        'severity': 'low'
                    })

        # Performance trends
        if len(predictions) >= 20:
            recent_predictions = predictions[:10]
            older_predictions = predictions[10:20]

            recent_avg_conf = sum(p[1] for p in recent_predictions if p[1]) / len([p for p in recent_predictions if p[1]])
            older_avg_conf = sum(p[1] for p in older_predictions if p[1]) / len([p for p in older_predictions if p[1]])

            conf_trend = recent_avg_conf - older_avg_conf

            if conf_trend > 0.05:
                insights.append({
                    'type': 'success',
                    'category': 'trends',
                    'title': 'Improving Confidence Trend',
                    'message': f'Model confidence has improved by {conf_trend:.1%} in recent predictions.',
                    'recommendation': 'Great trend! Continue monitoring to ensure sustained improvement.',
                    'severity': 'low'
                })
            elif conf_trend < -0.05:
                insights.append({
                    'type': 'warning',
                    'category': 'trends',
                    'title': 'Declining Confidence Trend',
                    'message': f'Model confidence has decreased by {abs(conf_trend):.1%} in recent predictions.',
                    'recommendation': 'Investigate recent data quality or consider model refresh.',
                    'severity': 'medium'
                })

        # Feedback analysis
        if feedback_data and feedback_data[0] > 0:
            total_feedback = feedback_data[0]
            correct_feedback = feedback_data[1]
            feedback_accuracy = correct_feedback / total_feedback

            if total_feedback >= 10:
                if feedback_accuracy >= 0.9:
                    insights.append({
                        'type': 'success',
                        'category': 'feedback',
                        'title': 'Excellent User Feedback',
                        'message': f'Users confirm {feedback_accuracy:.1%} accuracy based on {total_feedback} feedbacks.',
                        'recommendation': 'Outstanding performance! Users are very satisfied with predictions.',
                        'severity': 'low'
                    })
                elif feedback_accuracy < 0.8:
                    insights.append({
                        'type': 'warning',
                        'category': 'feedback',
                        'title': 'User Feedback Concerns',
                        'message': f'Only {feedback_accuracy:.1%} of user feedback confirms correct predictions.',
                        'recommendation': 'Investigate prediction quality and consider model improvements.',
                        'severity': 'high'
                    })

        return jsonify({
            'success': True,
            'data': {
                'insights': insights,
                'summary': {
                    'total_insights': len(insights),
                    'warnings': len([i for i in insights if i['type'] == 'warning']),
                    'successes': len([i for i in insights if i['type'] == 'success']),
                    'recommendations': len([i for i in insights if i.get('recommendation')])
                }
            }
        }), 200

    except Exception as e:
        print(f"Model insights error: {e}")
        return jsonify({'success': False, 'error': 'Failed to get model insights'}), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced SMS Guard Backend...")
    if init_db():
        print("✅ Enhanced backend ready!")
        print(f"🤖 ML Model: {ml_model.model_name} v{ml_model.model_version}")
        print("🔑 Demo credentials: demo / demo123")
        print("📊 API running on: http://localhost:5000")
        print("=" * 50)
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize database")
