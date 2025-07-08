"""
Database Models for SMS Guard Application

This file contains all the SQLAlchemy models for the application,
including User and Prediction models with proper relationships and constraints.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    theme = db.Column(db.String(10), default='light')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profileImage': self.profile_image,
            'bio': self.bio,
            'memberSince': self.member_since.strftime('%Y-%m-%d'),
            'isAuthenticated': True,
            'theme': self.theme
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Prediction(db.Model):
    """Prediction model for storing SMS spam detection results"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)  # 'spam' or 'ham'
    confidence = db.Column(db.Float, nullable=False)  # 0.0 to 1.0
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    model_version = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add constraints
    __table_args__ = (
        db.CheckConstraint('prediction IN ("spam", "ham")', name='check_prediction_values'),
        db.CheckConstraint('confidence >= 0 AND confidence <= 1', name='check_confidence_range'),
    )
    
    def to_dict(self):
        """Convert prediction object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'message': self.message,
            'prediction': self.prediction,
            'confidence': round(self.confidence, 4),
            'timestamp': self.timestamp.isoformat() + 'Z',
            'userId': self.user_id
        }
    
    def __repr__(self):
        return f'<Prediction {self.id}: {self.prediction}>'

class UserStats:
    """Helper class for calculating user statistics"""
    
    @staticmethod
    def calculate_stats(user_id):
        """Calculate comprehensive statistics for a user"""
        predictions = Prediction.query.filter_by(user_id=user_id).all()
        
        total_messages = len(predictions)
        spam_count = len([p for p in predictions if p.prediction == 'spam'])
        ham_count = len([p for p in predictions if p.prediction == 'ham'])
        
        spam_rate = spam_count / total_messages if total_messages > 0 else 0
        avg_confidence = sum(p.confidence for p in predictions) / total_messages if total_messages > 0 else 0
        
        # Get recent predictions (last 10)
        recent_predictions = Prediction.query.filter_by(user_id=user_id)\
            .order_by(Prediction.timestamp.desc())\
            .limit(10)\
            .all()
        
        return {
            'totalMessages': total_messages,
            'spamCount': spam_count,
            'hamCount': ham_count,
            'accuracy': 0.95,  # This would be calculated based on model performance
            'spamRate': round(spam_rate, 4),
            'avgConfidence': round(avg_confidence, 4),
            'recentPredictions': [p.to_dict() for p in recent_predictions]
        }
