# 🔧 Login Fix Guide

## Quick Fix Steps

### 1. **Start Backend Manually**
```bash
cd backend
python run.py
```

You should see:
```
============================================================
SMS Guard Flask Backend Starting...
Environment: development
Debug Mode: True
Host: 0.0.0.0
Port: 5000
Demo credentials: demo / demo123
API will be available at: http://localhost:5000/api
Frontend should connect from: http://localhost:5173
============================================================
```

### 2. **Test Demo Login**
Open another terminal and run:
```bash
python test_demo_login.py
```

### 3. **Start Frontend**
In another terminal:
```bash
npm run dev:frontend-only
```

### 4. **Test Login in Browser**
1. Go to `http://localhost:5173`
2. Use demo credentials:
   - Username: `demo`
   - Password: `demo123`

## If Backend Won't Start

### Install Dependencies:
```bash
pip install -r backend/requirements.txt
```

### Or use the quick start:
```bash
python quick_start.py
```

## Common Issues

### 1. **Port 5000 in use**
- Kill any process using port 5000
- Or change port in `backend/run.py`

### 2. **Python dependencies missing**
```bash
pip install flask flask-sqlalchemy flask-cors flask-jwt-extended werkzeug
```

### 3. **Database issues**
- Delete `backend/smsguard.db` and restart
- Backend will recreate it with demo user

## Test Everything Works

1. Backend health: `http://localhost:5000/api/health`
2. Demo login works in browser
3. Can access dashboard after login

## If Still Not Working

Check browser console (F12) for errors and let me know what you see.
