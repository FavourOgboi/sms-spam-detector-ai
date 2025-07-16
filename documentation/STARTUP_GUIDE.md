# 🚀 SMS Guard - Startup Guide

## Quick Start

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 2. Start Frontend

```bash
# In a new terminal, from project root
npm install
npm run dev
```

### 3. Login

- Open: http://localhost:5173
- **Demo User:** `demo` / `demo123`
- Or register a new user

## Project Structure

```
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask app factory
│   ├── run.py              # Backend startup script
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── predictions.py  # Spam prediction endpoints
│   │   └── users.py        # User management endpoints
│   ├── ml_model/           # Machine learning components
│   └── requirements.txt    # Python dependencies
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── pages/              # Page components
│   ├── services/           # API services
│   └── contexts/           # React contexts
└── package.json            # Node.js dependencies
```

## Features

✅ **Authentication System**

- JWT-based authentication
- Demo user auto-creation
- User registration
- Password hashing with Werkzeug

✅ **SMS Spam Detection**

- Machine learning predictions
- Confidence scores
- Prediction history storage

✅ **User Dashboard**

- Statistics and analytics
- Recent predictions
- User profile management

✅ **Database**

- SQLAlchemy ORM
- SQLite for development
- PostgreSQL support for production

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/user/stats` - User statistics
- `POST /api/predict` - SMS spam prediction

## Troubleshooting

### Backend won't start

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend won't start

```bash
npm install
npm run dev
```

### Can't login

- Register a new account at `/register` first
- Check backend console for any error messages
- Verify backend is running on port 5000

### Database issues

- Delete `backend/instance/smsguard.db` to reset
- Restart backend to recreate clean database

## Development

### Backend Development

```bash
cd backend
pip install -r requirements.txt
export FLASK_ENV=development
python run.py
```

### Frontend Development

```bash
npm run dev
```

### Testing

```bash
# Test backend authentication
cd backend
python test_auth_fix.py
```

## Production Deployment

### Backend

```bash
cd backend
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend

```bash
npm run build
# Serve the dist/ folder with your web server
```

## Environment Variables

Create `.env` file in backend folder:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///smsguard.db
FLASK_ENV=development
```

**Your SMS Guard application is now properly structured and ready to use! 🎉**
