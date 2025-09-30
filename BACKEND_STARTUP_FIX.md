# 🔧 SMS Guard Backend Startup Diagnostic & Fix Guide

## Problem Identified
The backend Flask application is not starting properly on port 5000. Based on deep analysis, here are the potential issues and solutions:

## 🔍 Root Causes Found

### 1. **Missing SendGrid Package** ⚠️
The `backend/routes/auth.py` file imports `sendgrid` but it's not in `requirements.txt`:
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
```

### 2. **Flask Version Mismatch** ⚠️
- Requirements.txt specifies: `Flask==2.3.3`
- System has installed: `Flask==3.0.3`
- This may cause compatibility issues

### 3. **Hardcoded Model Paths** ⚠️
In `backend/ml_model/spam_detector.py` (lines 78-80):
```python
model_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\clf_model.pkl'
vectorizer_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\vectorizer.pkl'
```

## ✅ SOLUTIONS

### Solution 1: Install Missing SendGrid Package
```bash
pip install sendgrid
```

### Solution 2: Update Requirements.txt
Add sendgrid to `backend/requirements.txt`:
```
sendgrid==6.11.0
```

### Solution 3: Fix Flask Version (Optional)
Either upgrade requirements or downgrade Flask:
```bash
# Option A: Upgrade requirements.txt to Flask 3.0.3
# Option B: Downgrade Flask
pip install Flask==2.3.3 --force-reinstall
```

### Solution 4: Fix Model Paths
The model paths should be relative, not absolute. This will be fixed in the code.

## 🚀 Quick Start Steps

### Step 1: Install Missing Dependencies
Open PowerShell or Command Prompt in the project directory:
```powershell
cd c:\Users\USER\Documents\GitHub\sms-spam-detector-ai
pip install sendgrid
```

### Step 2: Run the Debug Script
Double-click on `run_backend_debug.bat` or run:
```cmd
run_backend_debug.bat
```

This will:
- Check Python version
- Check Flask installation
- Check SendGrid installation
- Start the backend server
- Show any error messages

### Step 3: Start Backend Manually
If the batch file works, you can also start manually:
```cmd
cd backend
python app.py
```

The backend should start on: **http://localhost:5000**

### Step 4: Start Frontend
In a separate terminal:
```cmd
npm run dev:frontend-only
```

The frontend should start on: **http://localhost:5173**

## 🧪 Testing the Backend

Once the backend starts, test it:

### Test 1: Health Check
Open browser to: http://localhost:5000/api/health

Expected response:
```json
{
  "success": true,
  "message": "SMS Guard API is running",
  "version": "1.0.0"
}
```

### Test 2: Check Console Output
You should see:
```
✅ Environment variables loaded from .env file
📧 SendGrid configured: API key found
🌐 CORS configured to allow all origins
Database initialized
Current users in database: X
Ready for new user registrations
 * Running on http://0.0.0.0:5000
```

## 🐛 Common Issues & Fixes

### Issue 1: "ModuleNotFoundError: No module named 'sendgrid'"
**Fix:** Run `pip install sendgrid`

### Issue 2: "Address already in use" (Port 5000)
**Fix:** Kill the process using port 5000:
```powershell
# Find process on port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue 3: Database errors
**Fix:** Delete and recreate database:
```cmd
cd backend
del instance\smsguard.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database recreated')"
```

### Issue 4: NLTK data missing
**Fix:** Download NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 📋 Complete Dependency List

Make sure all these are installed:
```bash
pip install flask flask-sqlalchemy flask-cors flask-jwt-extended flask-mail
pip install werkzeug python-dotenv sendgrid
pip install scikit-learn numpy pandas joblib
pip install nltk lime shap
pip install pillow
```

## 🔄 Alternative: Fresh Install

If nothing works, try a fresh install:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# On Windows:
venv\Scripts\activate

# 3. Install all dependencies
cd backend
pip install -r requirements.txt
pip install sendgrid

# 4. Run the app
python app.py
```

## 📞 Next Steps

1. **Run `run_backend_debug.bat`** - This will show you exactly what's wrong
2. **Install sendgrid** - `pip install sendgrid`
3. **Check the console output** - Look for error messages
4. **Test the health endpoint** - http://localhost:5000/api/health
5. **Start the frontend** - `npm run dev:frontend-only`

## 🎯 Expected Behavior

When working correctly:
- Backend runs on http://localhost:5000
- Frontend runs on http://localhost:5173
- Health check returns success
- You can register/login users
- SMS spam detection works

## 📝 Files Created for Debugging

1. `run_backend_debug.bat` - Interactive debug script
2. `check_imports.py` - Check all Python imports
3. `direct_test.py` - Direct backend test
4. `BACKEND_STARTUP_FIX.md` - This guide

---

**Need more help?** Check the error messages in the console when running `run_backend_debug.bat` and share them for further assistance.

