"""
SMS Spam Detection Model

This module contains the SpamDetector class that handles loading
the trained model and making predictions on SMS messages.
"""

import joblib
import re
import os
import time
from typing import Dict, Tuple
import numpy as np

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
        
        # Default paths
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'spam_model.pkl')
        if vectorizer_path is None:
            vectorizer_path = os.path.join(os.path.dirname(__file__), 'models', 'vectorizer.pkl')
        
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
        Preprocess SMS text for prediction
        
        Args:
            text: Raw SMS message text
            
        Returns:
            Preprocessed text string
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra spaces created by regex
        text = ' '.join(text.split())
        
        return text
    
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
            # Preprocess the message
            processed_message = self.preprocess_text(message)
            
            if self.model is not None and self.vectorizer is not None:
                # Use trained model for prediction
                features = self.vectorizer.transform([processed_message])
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
                # Fallback prediction method using keyword detection
                result = self._fallback_prediction(processed_message, start_time)
            
            return result
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            # Return fallback prediction on error
            return self._fallback_prediction(message, start_time)
    
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
            'vectorizer_path': self.vectorizer_path
        }

# Global instance for the Flask app
spam_detector = SpamDetector()
