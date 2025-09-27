# 🚀 Quick Start Guide - Forgot Password with Secure Tokens

## ✅ What's Been Fixed
- **Secure tokens** using `itsdangerous` library
- **No token storage** - tokens are self-contained and cryptographically signed
- **1-hour expiry** built into the token
- **Better error handling** and debugging
- **Development mode** shows reset links when email isn't configured

## 🎯 How to Test

### Step 1: Start Backend
```bash
cd backend
python app.py
```

**Look for these messages:**
```
✅ Environment variables loaded from .env file
📧 Email configured: your_email@gmail.com (or Email not configured message)
Model loaded successfully...
Database initialized
Current users in database: 2
* Running on http://127.0.0.1:5000
```

### Step 2: Start Frontend
**In a new terminal:**
```bash
npm run dev:frontend-only
```

**Note the port** (e.g., `http://localhost:5179`)

### Step 3: Test the Application
1. Go to your frontend URL
2. Register a new account or login with existing credentials
3. Test the SMS spam detection functionality
4. Explore the dashboard and features

### Step 4: Expected Results

**Successful Login:**
- You should be redirected to the dashboard
- All features should be accessible
- SMS prediction should work correctly

**In Browser Console:**
```
🔗 Reset link (development): http://localhost:5173/reset-password?token=...
```

### Step 5: Test Password Reset
1. Copy the reset link from console
2. Open it in a new tab
3. Enter a new password
4. Submit - should redirect to login
5. Try logging in with the new password

## 🔧 If You Get "Endpoint not found"

### Check Backend Status
1. Make sure backend terminal shows "Running on http://127.0.0.1:5000"
2. Test health endpoint: `http://localhost:5000/api/health`
3. Should return: `{"success": true, "message": "SMS Guard API is running"}`

### Check CORS
- Backend is configured to allow all origins in development
- Should see: "🌐 CORS configured to allow all origins with full headers and methods"

### Check Routes
The forgot password endpoint should be: `POST /api/auth/forgot-password`

## 🎉 What Should Work Now

- ✅ **Secure token generation** with `itsdangerous`
- ✅ **No "Endpoint not found" errors** 
- ✅ **Development mode** shows reset links
- ✅ **Token verification** works properly
- ✅ **Password reset** completes successfully
- ✅ **Clean error handling** with helpful messages

## 🐛 Troubleshooting

**"Endpoint not found":**
- Backend not running or crashed
- Check backend terminal for errors

**"Network error":**
- Frontend can't reach backend
- Check if backend is on port 5000

**"No user with that email":**
- Email doesn't exist in database
- Use existing test emails

**Token errors:**
- Token expired (1 hour limit)
- Generate new reset link

## 📝 Next Steps

Once this works:
1. ✅ Forgot password is fully functional
2. ✅ Secure token system implemented
3. ✅ Ready for production use
4. ✅ Can configure real email later

**Try the steps above and let me know what happens!** 🎯
