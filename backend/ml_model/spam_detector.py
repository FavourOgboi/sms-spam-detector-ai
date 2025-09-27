"""
SMS Spam Detection Model

This module contains the SpamDetector class that handles loading
the trained model and making predictions on SMS messages.
"""

import joblib
import re
import os
import time
from typing import Dict, Tuple, List, Optional
import numpy as np
from functools import lru_cache

# NLTK imports for exact notebook preprocessing
try:
    import nltk
    import string
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer

    # Download required NLTK data if not present
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    NLTK_AVAILABLE = True
    ps = PorterStemmer()
except ImportError:
    NLTK_AVAILABLE = False
    ps = None

# Explainable AI imports (optional)
try:
    import lime
    import lime.lime_text
    LIME_AVAILABLE = True
except ImportError:
    LIME_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

class SpamDetector:
    """
    SMS Spam Detection using trained scikit-learn model
    
    This class loads a pre-trained model and vectorizer to classify
    SMS messages as spam or ham (legitimate).
    """
    
    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        """
        Initialize the spam detector with model and vectorizer paths
        
        Args:
            model_path: Path to the trained model file (.pkl)
            vectorizer_path: Path to the trained vectorizer file (.pkl)
        """
        self.model = None
        self.vectorizer = None
        self.model_version = "1.0.0"
        self._preprocessing_cache = {}  # Simple cache for preprocessing
        self._max_cache_size = 100  # Limit cache size to prevent memory issues

        # Use correct absolute paths for model and vectorizer
        if model_path is None:
            model_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\clf_model.pkl'
        if vectorizer_path is None:
            vectorizer_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\vectorizer.pkl'

        self.model_path = model_path
        self.vectorizer_path = vectorizer_path

        # Load model and vectorizer
        self.load_model()
    
    def load_model(self):
        """Load the trained model and vectorizer from disk"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                print(f"Model loaded successfully from {self.model_path}")
                print(f"Vectorizer loaded successfully from {self.vectorizer_path}")
            else:
                print("Warning: Model files not found. Using fallback prediction method.")
                print(f"Expected model at: {self.model_path}")
                print(f"Expected vectorizer at: {self.vectorizer_path}")
                self.model = None
                self.vectorizer = None
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model = None
            self.vectorizer = None
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess SMS text for prediction using EXACT same method as notebook

        This matches the transform_text function from the notebook:
        1. Convert to lowercase
        2. Tokenize with NLTK
        3. Keep only alphanumeric tokens
        4. Remove stopwords and punctuation
        5. Apply Porter stemming
        6. Join back to string

        Args:
            text: Raw SMS message text

        Returns:
            Preprocessed text string (same as notebook)
        """
        # Input validation - handle various input types
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        if not text.strip():
            return ""

        # Check cache first for speed improvement
        text_hash = hash(text)
        if text_hash in self._preprocessing_cache:
            return self._preprocessing_cache[text_hash]

        try:
            if NLTK_AVAILABLE:
                # EXACT preprocessing from notebook transform_text function
                text = text.lower()
                text = nltk.word_tokenize(text)

                # Keep only alphanumeric tokens
                y = []
                for i in text:
                    if i.isalnum():
                        y.append(i)

                text = y[:]
                y.clear()

                # Remove stopwords and punctuation
                for i in text:
                    if i not in stopwords.words('english') and i not in string.punctuation:
                        y.append(i)

                text = y[:]
                y.clear()

                # Apply Porter stemming
                for i in text:
                    y.append(ps.stem(i))

                # Join back to string
                processed_text = " ".join(y)
                # Cache the result for speed improvement (with size limit)
                if len(self._preprocessing_cache) >= self._max_cache_size:
                    # Remove oldest entry (simple FIFO)
                    oldest_key = next(iter(self._preprocessing_cache))
                    del self._preprocessing_cache[oldest_key]
                self._preprocessing_cache[text_hash] = processed_text
                return processed_text
            else:
                # Fallback preprocessing if NLTK not available
                print("Warning: NLTK not available, using basic preprocessing")
                text = text.lower()
                text = ' '.join(text.split())
                text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
                processed_text = ' '.join(text.split())
                # Cache the result
                self._preprocessing_cache[text_hash] = processed_text
                return processed_text
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            # Basic fallback preprocessing
            text = text.lower()
            text = ' '.join(text.split())
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            processed_text = ' '.join(text.split())
            # Cache the result
            self._preprocessing_cache[text_hash] = processed_text
            return processed_text
    
    def predict(self, message: str) -> Dict[str, any]:
        """
        Predict if an SMS message is spam or ham

        Args:
            message: SMS message text to classify

        Returns:
            Dictionary containing prediction, confidence, and processing time
        """
        start_time = time.time()

        try:
            # Input validation - handle various input types
            if message is None:
                message = ""
            elif not isinstance(message, str):
                message = str(message)  # Convert to string

            # Handle empty messages
            if not message.strip():
                return {
                    'prediction': 'ham',  # Empty messages are typically not spam
                    'confidence': 0.5,    # Low confidence for empty input
                    'processing_time_ms': int((time.time() - start_time) * 1000),
                    'model_version': self.model_version,
                    'note': 'Empty message classified as ham with low confidence'
                }

            # Preprocess the message
            processed_message = self.preprocess_text(message)
            
            if self.model is not None and self.vectorizer is not None:
                # Use trained model for prediction
                # FIXED: Convert to dense array to match training format
                features = self.vectorizer.transform([processed_message]).toarray()
                prediction = self.model.predict(features)[0]
                probabilities = self.model.predict_proba(features)[0]
                confidence = max(probabilities)

                result = {
                    'prediction': 'spam' if prediction == 1 else 'ham',
                    'confidence': float(confidence),
                    'processing_time_ms': int((time.time() - start_time) * 1000),
                    'model_version': self.model_version
                }
            else:
                # Models not loaded - provide informative error
                result = {
                    'prediction': 'error',
                    'confidence': 0.0,
                    'processing_time_ms': int((time.time() - start_time) * 1000),
                    'model_version': 'error',
                    'error': 'Trained models not loaded. Check model files exist and are accessible.',
                    'model_path': self.model_path,
                    'vectorizer_path': self.vectorizer_path
                }
            
            return result
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            # Return error information instead of crashing
            return {
                'prediction': 'error',
                'confidence': 0.0,
                'processing_time_ms': int((time.time() - start_time) * 1000),
                'model_version': 'error',
                'error': f'Prediction failed: {str(e)}',
                'message': message
            }
    
    def _fallback_prediction(self, message: str, start_time: float) -> Dict[str, any]:
        """
        Fallback prediction method using keyword-based detection
        
        Args:
            message: Preprocessed message text
            start_time: Start time for processing time calculation
            
        Returns:
            Dictionary containing prediction results
        """
        # Common spam keywords
        spam_keywords = [
            'free', 'winner', 'urgent', 'limited time', 'click now', 
            'congratulations', 'prize', 'claim', 'offer', 'deal',
            'money', 'cash', 'credit', 'loan', 'debt', 'guarantee',
            'call now', 'act now', 'dont miss', 'exclusive', 'bonus',
            'win', 'won', 'winning', 'lottery', 'jackpot', 'reward'
        ]
        
        message_lower = message.lower()
        spam_score = 0
        
        # Count spam keywords
        for keyword in spam_keywords:
            if keyword in message_lower:
                spam_score += 1
        
        # Simple scoring logic
        is_spam = spam_score >= 2 or (spam_score >= 1 and len(message) < 50)
        confidence = min(0.6 + (spam_score * 0.1), 0.95) if is_spam else max(0.4 - (spam_score * 0.1), 0.05)
        
        return {
            'prediction': 'spam' if is_spam else 'ham',
            'confidence': float(confidence),
            'processing_time_ms': int((time.time() - start_time) * 1000),
            'model_version': 'fallback_1.0.0'
        }
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about the loaded model

        Returns:
            Dictionary containing model information
        """
        return {
            'model_loaded': self.model is not None,
            'vectorizer_loaded': self.vectorizer is not None,
            'model_version': self.model_version,
            'model_path': self.model_path,
            'vectorizer_path': self.vectorizer_path,
            'lime_available': LIME_AVAILABLE,
            'shap_available': SHAP_AVAILABLE,
            'nltk_available': NLTK_AVAILABLE,
            'preprocessing': 'notebook_exact' if NLTK_AVAILABLE else 'basic_fallback'
        }

    def explain_prediction(self, message: str, num_features: int = 10) -> Dict[str, any]:
        """
        Generate explanation for a prediction using LIME or model-based feature importance

        Args:
            message: SMS message to explain
            num_features: Number of top features to include in explanation

        Returns:
            Dictionary containing explanation data
        """
        start_time = time.time()

        try:
            # Preprocess the message
            processed_message = self.preprocess_text(message)

            # Get prediction first
            prediction_result = self.predict(message)

            if self.model is not None and self.vectorizer is not None:
                # Try LIME first, then SHAP, then fallback to model-based explanation
                if LIME_AVAILABLE:
                    explanation_result = self._get_lime_explanation(message, num_features, prediction_result)
                elif SHAP_AVAILABLE:
                    explanation_result = self._get_shap_explanation(message, num_features, prediction_result)
                else:
                    explanation_result = self._get_model_explanation(processed_message, num_features, prediction_result)

                explanation_result['processing_time_ms'] = int((time.time() - start_time) * 1000)
                return explanation_result
            else:
                # Fallback to keyword analysis
                return {
                    'success': False,
                    'error': 'Model not loaded',
                    'fallback_explanation': self._get_keyword_explanation(processed_message),
                    'processing_time_ms': int((time.time() - start_time) * 1000)
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Explanation failed: {str(e)}',
                'fallback_explanation': self._get_keyword_explanation(processed_message),
                'processing_time_ms': int((time.time() - start_time) * 1000)
            }

    def _get_lime_explanation(self, message: str, num_features: int, prediction_result: Dict) -> Dict[str, any]:
        """
        Generate explanation using LIME (based on Databricks implementation)

        Args:
            message: Original message text
            num_features: Number of top features to return
            prediction_result: Result from prediction

        Returns:
            Dictionary containing LIME explanation
        """
        try:
            # Create LIME explainer with enhanced configuration
            explainer = lime.lime_text.LimeTextExplainer(
                class_names=['ham', 'spam'],
                feature_selection='auto',  # Auto feature selection like Databricks
                verbose=False,
                mode='classification'
            )

            # Define prediction function for LIME (Databricks style)
            def predict_proba_for_lime(texts):
                """
                Prediction function that LIME will use to test perturbations
                Enhanced version based on Databricks implementation

                Args:
                    texts: List of text strings to predict

                Returns:
                    2D numpy array of probabilities [n_samples, n_classes]
                """
                predictions = []
                for text in texts:
                    # Preprocess and vectorize (consistent with training)
                    processed_text = self.preprocess_text(text)
                    features = self.vectorizer.transform([processed_text]).toarray()

                    # Get probabilities
                    proba = self.model.predict_proba(features)[0]
                    predictions.append(proba)

                return np.array(predictions)

            # Generate LIME explanation with optimized parameters for speed
            explanation = explainer.explain_instance(
                message,  # Use original message, not preprocessed
                predict_proba_for_lime,
                num_features=min(num_features, 10),  # Limit features for performance
                labels=[0, 1],  # Explain both classes
                num_samples=500  # Reduced samples for faster processing
            )

            # Get prediction probabilities for detailed analysis
            prediction_proba = predict_proba_for_lime([message])[0]

            # Extract feature explanations with enhanced metadata
            feature_explanations = []
            for feature, importance in explanation.as_list():
                feature_explanations.append({
                    'feature': feature,
                    'importance': float(importance),
                    'direction': 'spam' if importance > 0 else 'ham',
                    'abs_importance': abs(float(importance)),
                    'contribution_type': 'positive' if importance > 0 else 'negative',
                    'strength': 'strong' if abs(importance) > 0.1 else 'moderate' if abs(importance) > 0.05 else 'weak'
                })

            # Sort by absolute importance
            feature_explanations.sort(key=lambda x: x['abs_importance'], reverse=True)

            # Calculate explanation quality metrics
            total_importance = sum(abs(f['importance']) for f in feature_explanations)
            explanation_coverage = len([f for f in feature_explanations if abs(f['importance']) > 0.01])

            return {
                'success': True,
                'message': message,
                'prediction': prediction_result['prediction'],
                'confidence': prediction_result['confidence'],
                'probabilities': {
                    'ham': float(prediction_proba[0]),
                    'spam': float(prediction_proba[1])
                },
                'explanation': {
                    'method': 'LIME (Local Interpretable Model-agnostic Explanations)',
                    'features': feature_explanations,
                    'summary': self._generate_lime_summary(feature_explanations, prediction_result['prediction']),
                    'lime_score': explanation.score if hasattr(explanation, 'score') else None,
                    'explanation_quality': {
                        'total_importance': float(total_importance),
                        'coverage': explanation_coverage,
                        'confidence_level': 'high' if total_importance > 0.5 else 'medium' if total_importance > 0.2 else 'low'
                    }
                }
            }

        except Exception as e:
            print(f"LIME explanation error: {e}")
            # Fallback to model-based explanation
            return self._get_model_explanation(self.preprocess_text(message), num_features, prediction_result)

    def _get_shap_explanation(self, message: str, num_features: int, prediction_result: Dict) -> Dict[str, any]:
        """
        Generate explanation using SHAP (based on Databricks implementation)

        Args:
            message: Original message text
            num_features: Number of top features to return
            prediction_result: Result from prediction

        Returns:
            Dictionary containing SHAP explanation
        """
        try:
            # Preprocess and vectorize the message
            processed_message = self.preprocess_text(message)
            message_vector = self.vectorizer.transform([processed_message]).toarray()

            # Create appropriate SHAP explainer based on model type (Databricks style)
            if hasattr(self.model, 'coef_'):
                # Linear models - use LinearExplainer
                shap_explainer = shap.LinearExplainer(
                    self.model,
                    message_vector,  # Use the current message as background
                    feature_perturbation="interventional"
                )
                explainer_type = "Linear"

            elif hasattr(self.model, 'feature_importances_'):
                # Tree-based models - use TreeExplainer
                shap_explainer = shap.TreeExplainer(self.model)
                explainer_type = "Tree"

            else:
                # Other models - use KernelExplainer (slower but universal)
                def model_predict(X):
                    return self.model.predict_proba(X)[:, 1]  # Return spam probability

                # Use a simple background (just the current message)
                background = message_vector
                shap_explainer = shap.KernelExplainer(model_predict, background)
                explainer_type = "Kernel"

            # Get SHAP values
            shap_values = shap_explainer.shap_values(message_vector)

            # Handle different SHAP value formats
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Spam class
            elif len(shap_values.shape) > 2:
                shap_values = shap_values[:, :, 1]  # Spam class

            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()

            # Extract feature contributions
            feature_explanations = []
            shap_values_flat = shap_values.flatten() if shap_values.ndim > 1 else shap_values

            for i, (feature_name, shap_value) in enumerate(zip(feature_names, shap_values_flat)):
                if abs(shap_value) > 0.001:  # Only include meaningful contributions
                    feature_explanations.append({
                        'feature': feature_name,
                        'importance': float(shap_value),
                        'direction': 'spam' if shap_value > 0 else 'ham',
                        'abs_importance': abs(float(shap_value)),
                        'contribution_type': 'positive' if shap_value > 0 else 'negative',
                        'strength': 'strong' if abs(shap_value) > 0.1 else 'moderate' if abs(shap_value) > 0.05 else 'weak'
                    })

            # Sort by absolute importance
            feature_explanations.sort(key=lambda x: x['abs_importance'], reverse=True)

            # Take top features
            top_features = feature_explanations[:num_features]

            # Calculate explanation quality metrics
            total_importance = sum(abs(f['importance']) for f in top_features)

            return {
                'success': True,
                'message': message,
                'prediction': prediction_result['prediction'],
                'confidence': prediction_result['confidence'],
                'explanation': {
                    'method': f'SHAP ({explainer_type} Explainer)',
                    'features': top_features,
                    'summary': self._generate_shap_summary(top_features, prediction_result['prediction'], explainer_type),
                    'explanation_quality': {
                        'total_importance': float(total_importance),
                        'explainer_type': explainer_type,
                        'confidence_level': 'high' if total_importance > 0.5 else 'medium' if total_importance > 0.2 else 'low'
                    }
                }
            }

        except Exception as e:
            print(f"SHAP explanation error: {e}")
            # Fallback to model-based explanation
            return self._get_model_explanation(self.preprocess_text(message), num_features, prediction_result)

    def _get_model_explanation(self, message: str, num_features: int, prediction_result: Dict) -> Dict[str, any]:
        """
        Generate explanation using the trained model's feature importance

        Args:
            message: Preprocessed message text
            num_features: Number of top features to return
            prediction_result: Result from prediction

        Returns:
            Dictionary containing model-based explanation
        """
        try:
            # Transform the message to get feature vector
            message_vector = self.vectorizer.transform([message]).toarray()

            # Get feature names from vectorizer
            feature_names = self.vectorizer.get_feature_names_out()

            # Get the feature weights for this specific message
            feature_weights = []

            if hasattr(self.model, 'coef_'):
                # For linear models (LogisticRegression, SVM, etc.)
                model_coef = self.model.coef_[0] if len(self.model.coef_.shape) > 1 else self.model.coef_

                # Get non-zero features in the message
                message_features = message_vector.toarray()[0]

                for i, (feature_name, feature_value) in enumerate(zip(feature_names, message_features)):
                    if feature_value > 0:  # Only consider features present in the message
                        importance = float(model_coef[i] * feature_value)
                        feature_weights.append({
                            'feature': feature_name,
                            'importance': importance,
                            'direction': 'spam' if importance > 0 else 'ham',
                            'frequency': float(feature_value)
                        })

                # Sort by absolute importance
                feature_weights.sort(key=lambda x: abs(x['importance']), reverse=True)

                # Take top features
                top_features = feature_weights[:num_features]

                return {
                    'success': True,
                    'message': message,
                    'prediction': prediction_result['prediction'],
                    'confidence': prediction_result['confidence'],
                    'explanation': {
                        'method': 'Model Feature Importance',
                        'features': top_features,
                        'summary': self._generate_model_summary(top_features, prediction_result['prediction'])
                    }
                }

            elif hasattr(self.model, 'feature_importances_'):
                # For tree-based models (RandomForest, etc.)
                importances = self.model.feature_importances_
                message_features = message_vector.toarray()[0]

                for i, (feature_name, feature_value) in enumerate(zip(feature_names, message_features)):
                    if feature_value > 0:
                        importance = float(importances[i] * feature_value)
                        feature_weights.append({
                            'feature': feature_name,
                            'importance': importance,
                            'direction': 'spam' if importance > 0.5 else 'ham',  # Threshold for tree models
                            'frequency': float(feature_value)
                        })

                feature_weights.sort(key=lambda x: abs(x['importance']), reverse=True)
                top_features = feature_weights[:num_features]

                return {
                    'success': True,
                    'message': message,
                    'prediction': prediction_result['prediction'],
                    'confidence': prediction_result['confidence'],
                    'explanation': {
                        'method': 'Tree Feature Importance',
                        'features': top_features,
                        'summary': self._generate_model_summary(top_features, prediction_result['prediction'])
                    }
                }
            else:
                # Model doesn't support feature importance, use enhanced keyword analysis
                return {
                    'success': True,
                    'message': message,
                    'prediction': prediction_result['prediction'],
                    'confidence': prediction_result['confidence'],
                    'explanation': self._get_enhanced_keyword_explanation(message, prediction_result)
                }

        except Exception as e:
            print(f"Model explanation error: {e}")
            return {
                'success': False,
                'error': f'Model explanation failed: {str(e)}',
                'fallback_explanation': self._get_keyword_explanation(message)
            }

    def _get_keyword_explanation(self, message: str) -> Dict[str, any]:
        """
        Fallback explanation using keyword analysis

        Args:
            message: Preprocessed message text

        Returns:
            Dictionary containing keyword-based explanation
        """
        spam_keywords = [
            'free', 'winner', 'urgent', 'limited time', 'click now',
            'congratulations', 'prize', 'claim', 'offer', 'deal',
            'money', 'cash', 'credit', 'loan', 'debt', 'guarantee',
            'call now', 'act now', 'dont miss', 'exclusive', 'bonus',
            'win', 'won', 'winning', 'lottery', 'jackpot', 'reward'
        ]

        message_lower = message.lower()
        found_keywords = []

        for keyword in spam_keywords:
            if keyword in message_lower:
                found_keywords.append({
                    'feature': keyword,
                    'importance': 0.5,  # Default importance
                    'direction': 'spam'
                })

        return {
            'method': 'Keyword Analysis',
            'features': found_keywords[:10],  # Top 10
            'summary': f"Found {len(found_keywords)} spam indicators" if found_keywords else "No obvious spam indicators found"
        }

    def _generate_model_summary(self, features: List[Dict], prediction: str) -> str:
        """
        Generate a human-readable summary based on your trained model's learned features

        Args:
            features: List of feature explanations from your trained model
            prediction: Predicted class (spam/ham)

        Returns:
            Human-readable explanation of what your model learned
        """
        if not features:
            return f"Your trained model classified this as {prediction.upper()} but no significant learned features were identified."

        # Separate spam and ham indicators
        spam_features = [f for f in features if f['direction'] == 'spam']
        ham_features = [f for f in features if f['direction'] == 'ham']

        top_features = features[:3]  # Top 3 most important features

        if prediction == 'spam':
            if spam_features:
                spam_words = [f['feature'] for f in spam_features[:3]]
                total_spam_signals = len(spam_features)
                return f"Our AI detected SPAM because words like '{', '.join(spam_words)}' are strong spam indicators based on patterns learned from thousands of messages. Found {total_spam_signals} spam signals total."
            else:
                return "Our AI classified this as SPAM based on learned patterns, though no individual words stood out as strong spam indicators."
        else:
            if ham_features:
                ham_words = [f['feature'] for f in ham_features[:3]]
                total_ham_signals = len(ham_features)
                return f"Our AI classified this as LEGITIMATE because words like '{', '.join(ham_words)}' indicate normal messages based on patterns learned from thousands of messages. Found {total_ham_signals} legitimate signals."
            else:
                return "Our AI classified this as LEGITIMATE based on learned communication patterns, indicating this message appears to be normal correspondence."

    def _get_enhanced_keyword_explanation(self, message: str, prediction_result: Dict) -> Dict[str, any]:
        """
        Enhanced keyword-based explanation with better analysis

        Args:
            message: Message text
            prediction_result: Prediction result

        Returns:
            Enhanced keyword explanation
        """
        spam_keywords = {
            'urgent': 0.8, 'free': 0.9, 'winner': 0.85, 'congratulations': 0.7,
            'prize': 0.75, 'claim': 0.6, 'offer': 0.65, 'deal': 0.6,
            'money': 0.8, 'cash': 0.8, 'credit': 0.7, 'loan': 0.7,
            'click': 0.6, 'now': 0.5, 'limited': 0.6, 'exclusive': 0.6,
            'win': 0.7, 'won': 0.75, 'winning': 0.7, 'lottery': 0.9,
            'guarantee': 0.7, 'bonus': 0.6, 'reward': 0.65
        }

        message_lower = message.lower()
        found_features = []

        for keyword, weight in spam_keywords.items():
            if keyword in message_lower:
                found_features.append({
                    'feature': keyword,
                    'importance': weight,
                    'direction': 'spam',
                    'frequency': message_lower.count(keyword)
                })

        # Sort by importance
        found_features.sort(key=lambda x: x['importance'], reverse=True)

        # Calculate explanation confidence
        total_spam_weight = sum(f['importance'] for f in found_features)
        explanation_confidence = min(total_spam_weight / 3.0, 1.0)  # Normalize

        summary = f"Found {len(found_features)} spam indicators with combined weight {total_spam_weight:.2f}"
        if prediction_result['prediction'] == 'spam':
            summary += f" - Strong spam signals detected"
        else:
            summary += f" - Insufficient spam signals for classification"

        return {
            'method': 'Enhanced Keyword Analysis',
            'features': found_features[:10],
            'summary': summary,
            'explanation_confidence': explanation_confidence
        }

    def _generate_lime_summary(self, features: List[Dict], prediction: str) -> str:
        """
        Generate a human-readable summary for LIME explanations

        Args:
            features: List of LIME feature explanations
            prediction: Predicted class (spam/ham)

        Returns:
            Human-readable LIME explanation summary
        """
        if not features:
            return f"LIME classified this as {prediction.upper()} but found no significant word contributions."

        # Get top contributing features for each direction
        spam_features = [f for f in features[:5] if f['direction'] == 'spam' and f['abs_importance'] > 0.01]
        ham_features = [f for f in features[:5] if f['direction'] == 'ham' and f['abs_importance'] > 0.01]

        if prediction == 'spam':
            if spam_features:
                top_spam = [f['feature'] for f in spam_features[:3]]
                summary = f"LIME identified this as SPAM primarily due to words: {', '.join(top_spam)}"
                if ham_features:
                    top_ham = [f['feature'] for f in ham_features[:2]]
                    summary += f". However, words like '{', '.join(top_ham)}' suggested it might be legitimate."
            else:
                summary = "LIME classified this as SPAM based on overall text patterns rather than specific words."
        else:
            if ham_features:
                top_ham = [f['feature'] for f in ham_features[:3]]
                summary = f"LIME identified this as LEGITIMATE due to normal words: {', '.join(top_ham)}"
                if spam_features:
                    top_spam = [f['feature'] for f in spam_features[:2]]
                    summary += f". Some words like '{', '.join(top_spam)}' had slight spam indicators."
            else:
                summary = "LIME classified this as LEGITIMATE based on overall text patterns."

        return summary

    def _generate_shap_summary(self, features: List[Dict], prediction: str, explainer_type: str) -> str:
        """
        Generate a human-readable summary for SHAP explanations

        Args:
            features: List of SHAP feature explanations
            prediction: Predicted class (spam/ham)
            explainer_type: Type of SHAP explainer used

        Returns:
            Human-readable SHAP explanation summary
        """
        if not features:
            return f"SHAP {explainer_type} explainer classified this as {prediction.upper()} but found no significant feature contributions."

        # Get top contributing features for each direction
        spam_features = [f for f in features[:5] if f['direction'] == 'spam' and f['abs_importance'] > 0.01]
        ham_features = [f for f in features[:5] if f['direction'] == 'ham' and f['abs_importance'] > 0.01]

        if prediction == 'spam':
            if spam_features:
                top_spam = [f['feature'] for f in spam_features[:3]]
                summary = f"SHAP {explainer_type} analysis identified this as SPAM due to features: {', '.join(top_spam)}"
                if ham_features:
                    top_ham = [f['feature'] for f in ham_features[:2]]
                    summary += f". However, features like '{', '.join(top_ham)}' provided some legitimacy signals."
            else:
                summary = f"SHAP {explainer_type} classified this as SPAM based on overall feature interactions rather than individual words."
        else:
            if ham_features:
                top_ham = [f['feature'] for f in ham_features[:3]]
                summary = f"SHAP {explainer_type} analysis identified this as LEGITIMATE due to features: {', '.join(top_ham)}"
                if spam_features:
                    top_spam = [f['feature'] for f in spam_features[:2]]
                    summary += f". Some features like '{', '.join(top_spam)}' showed minor spam characteristics."
            else:
                summary = f"SHAP {explainer_type} classified this as LEGITIMATE based on overall feature patterns."

        return summary

    def _generate_explanation_summary(self, features: List[Dict], prediction: str) -> str:
        """
        Generate a human-readable summary of the explanation (legacy method)

        Args:
            features: List of feature explanations
            prediction: Predicted class (spam/ham)

        Returns:
            Human-readable explanation summary
        """
        return self._generate_model_summary(features, prediction)

# Global instance for the Flask app
spam_detector = SpamDetector()
