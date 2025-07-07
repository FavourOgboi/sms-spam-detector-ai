# Backend Development Guide for SMS Guard

## 🎯 Overview for Gemini AI

This document provides comprehensive guidance for implementing the Flask backend for SMS Guard. The frontend is fully functional with mock data and expects specific API endpoints and data formats.

## 📋 Project Context

**Frontend Technology:** React + TypeScript + Tailwind CSS  
**Expected Backend:** Flask + Python  
**Database:** PostgreSQL (recommended) or SQLite  
**Authentication:** JWT tokens  
**ML Framework:** scikit-learn, TensorFlow, or PyTorch  

## 🗂️ Frontend File Structure Reference

```
src/
├── components/
│   ├── layout/
│   │   ├── Layout.tsx          # Main layout wrapper
│   │   └── Navigation.tsx      # Sidebar navigation with user info
│   ├── ui/
│   │   ├── GuardAnimation.tsx  # Animated guard for predictions
│   │   ├── LoadingSpinner.tsx  # Loading states
│   │   └── Modal.tsx           # Modal dialogs
│   └── ProtectedRoute.tsx      # Route protection
├── contexts/
│   ├── AuthContext.tsx         # Authentication state
│   └── ThemeContext.tsx        # Theme management
├── pages/
│   ├── Dashboard.tsx           # Analytics dashboard
│   ├── Predict.tsx             # Message prediction
│   ├── History.tsx             # Message history
│   ├── Profile.tsx             # User profile
│   ├── Login.tsx               # Authentication
│   └── Register.tsx            # User registration
├── services/
│   └── api.ts                  # API integration layer
└── types/
    └── index.ts                # TypeScript definitions
```

## 🔗 API Integration Points

### Current API Configuration
```typescript
// src/services/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';
```

### Authentication Flow
1. Frontend sends credentials to `/api/auth/login`
2. Backend returns JWT token + user data
3. Frontend stores token in localStorage
4. All requests include `Authorization: Bearer <token>` header

## 📊 Required Data Models

### User Model
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    member_since: datetime = datetime.now()
    theme: str = 'light'
    is_active: bool = True
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
```

### Prediction Model
```python
@dataclass
class PredictionResult:
    id: str
    user_id: str
    message: str
    prediction: str  # 'spam' or 'ham'
    confidence: float  # 0.0 to 1.0
    timestamp: datetime = datetime.now()
    processing_time_ms: Optional[int] = None
    model_version: Optional[str] = None
```

### User Statistics Model
```python
@dataclass
class UserStats:
    total_messages: int
    spam_count: int
    ham_count: int
    accuracy: float  # Model accuracy
    spam_rate: float  # User's spam rate
    avg_confidence: float  # Average confidence
    recent_predictions: list  # Last 10 predictions
```

## 🌐 Required API Endpoints

### Authentication Endpoints

#### POST /api/auth/login
```python
# Request
{
    "usernameOrEmail": "string",
    "password": "string"
}

# Response
{
    "success": true,
    "data": {
        "token": "jwt_token_here",
        "user": {
            "id": "user_id",
            "username": "username",
            "email": "email@example.com",
            "profileImage": "url_or_null",
            "bio": "user_bio",
            "memberSince": "2024-01-15",
            "isAuthenticated": true,
            "theme": "light"
        }
    }
}
```

#### POST /api/auth/register
```python
# Request
{
    "username": "string",
    "email": "string",
    "password": "string"
}

# Response - Same as login
```

#### GET /api/auth/me
```python
# Headers: Authorization: Bearer <token>
# Response
{
    "success": true,
    "data": {
        "id": "user_id",
        "username": "username",
        "email": "email@example.com",
        "profileImage": "url_or_null",
        "bio": "user_bio",
        "memberSince": "2024-01-15",
        "isAuthenticated": true,
        "theme": "light"
    }
}
```

### Prediction Endpoints

#### POST /api/predict
```python
# Headers: Authorization: Bearer <token>
# Request
{
    "message": "Your SMS message text here"
}

# Response
{
    "success": true,
    "data": {
        "id": "prediction_id",
        "message": "Your SMS message text here",
        "prediction": "spam",  # or "ham"
        "confidence": 0.85,
        "timestamp": "2024-01-15T10:30:00Z",
        "userId": "user_id"
    }
}
```

### User Data Endpoints

#### GET /api/user/stats
```python
# Headers: Authorization: Bearer <token>
# Response
{
    "success": true,
    "data": {
        "totalMessages": 150,
        "spamCount": 45,
        "hamCount": 105,
        "accuracy": 0.973,
        "spamRate": 0.30,
        "avgConfidence": 0.87,
        "recentPredictions": [
            {
                "id": "pred_id",
                "message": "message text",
                "prediction": "spam",
                "confidence": 0.92,
                "timestamp": "2024-01-15T10:30:00Z",
                "userId": "user_id"
            }
            // ... up to 10 recent predictions
        ]
    }
}
```

#### GET /api/user/predictions
```python
# Headers: Authorization: Bearer <token>
# Response
{
    "success": true,
    "data": [
        {
            "id": "pred_id",
            "message": "message text",
            "prediction": "spam",
            "confidence": 0.92,
            "timestamp": "2024-01-15T10:30:00Z",
            "userId": "user_id"
        }
        // ... all user predictions
    ]
}
```

#### PUT /api/user/profile
```python
# Headers: Authorization: Bearer <token>
# Content-Type: multipart/form-data
# Form data: username, email, bio, profileImage (file)

# Response
{
    "success": true,
    "data": {
        "id": "user_id",
        "username": "updated_username",
        "email": "updated_email",
        "profileImage": "new_image_url",
        "bio": "updated_bio",
        "memberSince": "2024-01-15",
        "isAuthenticated": true,
        "theme": "light"
    }
}
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_image VARCHAR(500),
    bio TEXT,
    member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    theme VARCHAR(10) DEFAULT 'light',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Predictions Table
```sql
CREATE TABLE predictions (
    id VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    prediction VARCHAR(10) NOT NULL CHECK (prediction IN ('spam', 'ham')),
    confidence DECIMAL(5,4) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_predictions_timestamp ON predictions(timestamp);
CREATE INDEX idx_predictions_prediction ON predictions(prediction);
```

## 🤖 Machine Learning Requirements

### Model Specifications
- **Input:** Raw SMS text
- **Output:** Classification ('spam' or 'ham') + confidence score
- **Performance:** >95% accuracy, <50ms processing time
- **Features:** TF-IDF, N-grams, keyword detection

### Training Data
- Use SMS Spam Collection dataset
- Implement preprocessing pipeline
- Include model versioning

### Example Implementation
```python
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re

class SpamDetector:
    def __init__(self):
        self.model = joblib.load('spam_model.pkl')
        self.vectorizer = joblib.load('vectorizer.pkl')
    
    def preprocess_text(self, text):
        # Remove special characters, lowercase, etc.
        text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
        return text
    
    def predict(self, message):
        processed = self.preprocess_text(message)
        features = self.vectorizer.transform([processed])
        prediction = self.model.predict(features)[0]
        confidence = max(self.model.predict_proba(features)[0])
        
        return {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'confidence': float(confidence)
        }
```

## 🔒 Security Requirements

### Authentication
```python
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
```

### Input Validation
```python
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class PredictionForm(FlaskForm):
    message = TextAreaField('message', validators=[
        DataRequired(),
        Length(min=1, max=500)
    ])

class UserRegistrationForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=3, max=100)
    ])
    email = StringField('email', validators=[
        DataRequired(),
        Email()
    ])
```

## 📁 File Upload Handling

### Profile Image Upload
```python
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/profile_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/user/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    if 'profileImage' in request.files:
        file = request.files['profileImage']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            # Update user profile_image in database
```

## 🌐 CORS Configuration

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173'])  # Development
# CORS(app, origins=['https://your-domain.com'])  # Production
```

## 📝 Environment Variables

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost/smsguard
# or for SQLite: sqlite:///smsguard.db

# File Upload
UPLOAD_FOLDER=uploads/
MAX_CONTENT_LENGTH=5242880  # 5MB

# CORS
CORS_ORIGINS=http://localhost:5173

# ML Model
MODEL_PATH=models/spam_detector.pkl
VECTORIZER_PATH=models/vectorizer.pkl
```

## 🧪 Testing Strategy

### Unit Tests
```python
import unittest
from app import app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def test_user_registration(self):
        response = self.app.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
```

## 🚀 Deployment Checklist

- [ ] Set up production database
- [ ] Configure environment variables
- [ ] Set up file storage (AWS S3, etc.)
- [ ] Configure CORS for production domain
- [ ] Set up logging and monitoring
- [ ] Train and deploy ML model
- [ ] Set up SSL certificates
- [ ] Configure rate limiting
- [ ] Set up backup strategy

## 📞 Frontend Integration Notes

### Key Files to Reference
- `src/services/api.ts` - All API calls and expected responses
- `src/types/index.ts` - TypeScript interfaces to match
- `src/contexts/AuthContext.tsx` - Authentication flow
- `src/pages/` - All page components that use the API

### Mock Data Replacement
The frontend currently uses mock data in `api.ts`. Replace each function marked with `// TODO: Connect to Flask` with actual HTTP requests to your Flask endpoints.

### Error Handling
The frontend expects errors in this format:
```json
{
    "success": false,
    "error": "Error message string"
}
```

This guide provides everything needed to implement a Flask backend that seamlessly integrates with the existing React frontend.