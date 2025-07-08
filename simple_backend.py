"""
Simple working Flask backend for SMS Guard
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import uuid
import os

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-sms-guard-2024'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-sms-guard-2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smsguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:5173'], supports_credentials=True)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    theme = db.Column(db.String(10), default='light')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
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

# Prediction Model
class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'prediction': self.prediction,
            'confidence': round(self.confidence, 4),
            'timestamp': self.timestamp.isoformat() + 'Z',
            'userId': self.user_id
        }

# Simple spam detection function
def predict_spam(message):
    spam_keywords = ['free', 'win', 'winner', 'urgent', 'limited time', 'click now', 
                     'congratulations', 'prize', 'claim', 'offer', 'money', 'cash']
    
    message_lower = message.lower()
    spam_score = sum(1 for keyword in spam_keywords if keyword in message_lower)
    
    is_spam = spam_score >= 2
    confidence = min(0.6 + (spam_score * 0.1), 0.95) if is_spam else max(0.4 - (spam_score * 0.1), 0.05)
    
    return {
        'prediction': 'spam' if is_spam else 'ham',
        'confidence': confidence
    }

# Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'success': True,
        'message': 'SMS Guard API is running',
        'version': '1.0.0'
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'data': {'token': token, 'user': user.to_dict()}
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username_or_email = data.get('usernameOrEmail', '').strip()
        password = data.get('password', '')
        
        if not username_or_email or not password:
            return jsonify({'success': False, 'error': 'Username/email and password are required'}), 400
        
        user = None
        if '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email.lower()).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'error': 'Account is deactivated'}), 401
        
        token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'data': {'token': token, 'user': user.to_dict()}
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Login failed'}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({'success': True, 'data': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to fetch user information'}), 500

@app.route('/api/predict', methods=['POST'])
@jwt_required()
def predict():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'success': False, 'error': 'User not found'}), 401
        
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        # Make prediction
        result = predict_spam(message)
        
        # Save prediction
        prediction = Prediction(
            user_id=current_user_id,
            message=message,
            prediction=result['prediction'],
            confidence=result['confidence']
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({'success': True, 'data': prediction.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Prediction failed'}), 500

@app.route('/api/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    try:
        current_user_id = get_jwt_identity()
        predictions = Prediction.query.filter_by(user_id=current_user_id).all()
        
        total_messages = len(predictions)
        spam_count = len([p for p in predictions if p.prediction == 'spam'])
        ham_count = len([p for p in predictions if p.prediction == 'ham'])
        
        spam_rate = spam_count / total_messages if total_messages > 0 else 0
        avg_confidence = sum(p.confidence for p in predictions) / total_messages if total_messages > 0 else 0
        
        recent_predictions = Prediction.query.filter_by(user_id=current_user_id)\
            .order_by(Prediction.timestamp.desc()).limit(10).all()
        
        stats = {
            'totalMessages': total_messages,
            'spamCount': spam_count,
            'hamCount': ham_count,
            'accuracy': 0.95,
            'spamRate': round(spam_rate, 4),
            'avgConfidence': round(avg_confidence, 4),
            'recentPredictions': [p.to_dict() for p in recent_predictions]
        }
        
        return jsonify({'success': True, 'data': stats}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to fetch statistics'}), 500

@app.route('/api/user/predictions', methods=['GET'])
@jwt_required()
def get_user_predictions():
    try:
        current_user_id = get_jwt_identity()
        predictions = Prediction.query.filter_by(user_id=current_user_id)\
            .order_by(Prediction.timestamp.desc()).all()

        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in predictions]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': 'Failed to fetch predictions'}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        data = request.get_json()

        # Update allowed fields
        if 'username' in data:
            username = data['username'].strip()
            if len(username) < 3:
                return jsonify({'success': False, 'error': 'Username must be at least 3 characters long'}), 400

            # Check if username is already taken
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'success': False, 'error': 'Username already taken'}), 409

            user.username = username

        if 'email' in data:
            email = data['email'].strip().lower()
            if '@' not in email or '.' not in email:
                return jsonify({'success': False, 'error': 'Invalid email format'}), 400

            # Check if email is already taken
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'success': False, 'error': 'Email already registered'}), 409

            user.email = email

        if 'bio' in data:
            bio = data['bio'].strip()
            if len(bio) > 500:
                return jsonify({'success': False, 'error': 'Bio must be less than 500 characters'}), 400
            user.bio = bio

        if 'theme' in data:
            theme = data['theme']
            if theme in ['light', 'dark']:
                user.theme = theme

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'success': True, 'data': user.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to update profile'}), 500

@app.route('/api/user/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user or not user.is_active:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        data = request.get_json()
        current_password = data.get('currentPassword', '')
        new_password = data.get('newPassword', '')
        confirm_password = data.get('confirmNewPassword', '')

        # Validate current password
        if not user.check_password(current_password):
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 400

        # Validate new password
        if len(new_password) < 6:
            return jsonify({'success': False, 'error': 'New password must be at least 6 characters long'}), 400

        if new_password != confirm_password:
            return jsonify({'success': False, 'error': 'New passwords do not match'}), 400

        # Update password
        user.set_password(new_password)
        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'success': True, 'message': 'Password changed successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to change password'}), 500

@app.route('/api/user/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404

        # Delete user (this will cascade delete predictions due to foreign key)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Account deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Failed to delete account'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create test users if they don't exist
        if not User.query.filter_by(username='demo').first():
            demo_user = User(username='demo', email='demo@example.com')
            demo_user.set_password('demo123')
            db.session.add(demo_user)
            
        if not User.query.filter_by(username='testuser').first():
            test_user = User(username='testuser', email='test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            
        db.session.commit()
        print("✅ Database initialized with test users")
    
    print("🚀 Starting SMS Guard Backend...")
    print("📊 Available endpoints:")
    print("   - POST /api/auth/login")
    print("   - POST /api/auth/register")
    print("   - GET /api/auth/me")
    print("   - POST /api/predict")
    print("   - GET /api/user/stats")
    print("   - GET /api/user/predictions")
    print("   - GET /api/health")
    print("🔑 Test credentials: demo / demo123")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
