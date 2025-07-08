# SMS Guard Flask Backend

A complete Flask backend for the SMS Guard spam detection application with JWT authentication, machine learning integration, and real-time analytics.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 🤖 **ML Spam Detection** - Real-time SMS spam classification
- 📊 **User Analytics** - Comprehensive statistics and dashboards
- 🗄️ **Database Management** - SQLAlchemy with PostgreSQL/SQLite support
- 📁 **File Upload** - Profile image management
- 🔒 **Security** - Input validation, CORS, and secure password handling

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository (if not already done)
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, change the SECRET_KEY and JWT_SECRET_KEY
```

### 3. Create ML Model

```bash
# Navigate to ml_notebooks directory
cd ../ml_notebooks

# Run the model creation script
python create_spam_model.py

# This will create the trained model files in backend/ml_model/models/
```

### 4. Initialize Database

```bash
# Go back to backend directory
cd ../backend

# Initialize the database (tables will be created automatically)
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 5. Run the Application

```bash
# Start the development server
python run.py

# Or use Flask's built-in command
flask run

# The API will be available at http://localhost:5000
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - User logout

### Predictions
- `POST /api/predict` - Predict SMS spam/ham
- `GET /api/model/info` - Get ML model information

### User Management
- `GET /api/user/stats` - Get user statistics
- `GET /api/user/predictions` - Get user's prediction history
- `PUT /api/user/profile` - Update user profile
- `PUT /api/user/change-password` - Change password
- `DELETE /api/user/delete` - Delete account

### Health Check
- `GET /api/health` - API health status

## Project Structure

```
backend/
├── app.py                 # Flask app factory
├── run.py                 # Application entry point
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── routes/               # API route blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── predictions.py   # Prediction routes
│   └── users.py         # User management routes
├── ml_model/            # Machine learning components
│   ├── __init__.py
│   ├── spam_detector.py # ML model wrapper
│   └── models/          # Trained model files
│       ├── spam_model.pkl
│       ├── vectorizer.pkl
│       └── model_metadata.json
└── uploads/             # File upload directory
    └── profile_images/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Flask secret key | dev-secret-key |
| `JWT_SECRET_KEY` | JWT signing key | jwt-secret-key |
| `DATABASE_URL` | Database connection string | sqlite:///smsguard.db |
| `UPLOAD_FOLDER` | File upload directory | uploads/profile_images |
| `MAX_CONTENT_LENGTH` | Max file upload size | 5242880 (5MB) |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:5173 |

## Database Configuration

### SQLite (Development)
```bash
DATABASE_URL=sqlite:///smsguard.db
```

### PostgreSQL (Production)
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/smsguard
```

## Machine Learning Model

The spam detection model uses:
- **Algorithm**: Naive Bayes or Logistic Regression (best performing)
- **Features**: TF-IDF vectorization with unigrams and bigrams
- **Preprocessing**: Text cleaning, lowercasing, special character removal
- **Performance**: >90% accuracy on test data

### Model Training

1. Run the training script:
   ```bash
   cd ml_notebooks
   python create_spam_model.py
   ```

2. The script will:
   - Create a sample dataset
   - Train multiple models
   - Select the best performing model
   - Save model files to `backend/ml_model/models/`

### Model Files
- `spam_model.pkl` - Trained classifier
- `vectorizer.pkl` - TF-IDF vectorizer
- `model_metadata.json` - Model information and metrics

## Testing

### Manual Testing
```bash
# Test the health endpoint
curl http://localhost:5000/api/health

# Test user registration
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Test spam prediction (with JWT token)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"message":"FREE! Win money now!"}'
```

### Unit Tests
```bash
# Run tests (when implemented)
pytest tests/
```

## Production Deployment

### Using Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Environment Setup for Production
```bash
# Set production environment
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export JWT_SECRET_KEY=your-production-jwt-key
export DATABASE_URL=postgresql://user:pass@host:port/db
export CORS_ORIGINS=https://yourdomain.com
```

## Security Considerations

- Change default secret keys in production
- Use HTTPS in production
- Set up proper CORS origins
- Use environment variables for sensitive data
- Implement rate limiting for production
- Regular security updates

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated
2. **Database Errors**: Check DATABASE_URL and permissions
3. **Model Not Found**: Run the model training script first
4. **CORS Errors**: Check CORS_ORIGINS environment variable
5. **File Upload Errors**: Check UPLOAD_FOLDER permissions

### Logs
Check console output for detailed error messages and debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
