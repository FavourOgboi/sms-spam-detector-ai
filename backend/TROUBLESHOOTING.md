# SMS Guard Authentication Troubleshooting

## Common Authentication Issues and Solutions

### Issue: "Invalid credentials" after successful registration

This is a common issue that can have several causes. Follow these steps to diagnose and fix:

## Quick Fix Steps

### Step 1: Run the Authentication Fix Script
```bash
cd backend
python fix_auth.py
```

This script will:
- Recreate the database tables
- Create test users with known passwords
- Verify the authentication flow

### Step 2: Test with Known Credentials
After running the fix script, try logging in with:
- **Username:** `demo`
- **Password:** `demo123`

OR

- **Username:** `testuser`
- **Password:** `password123`

### Step 3: Debug Existing Issues
If you still have problems, run the debug script:
```bash
cd backend
python debug_auth.py
```

This will help you:
- Check database connection
- List all users
- Test password hashing
- Verify specific user credentials
- Reset passwords if needed

## Common Causes and Solutions

### 1. Database Not Initialized Properly
**Symptoms:** Registration works but login fails immediately

**Solution:**
```bash
cd backend
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.drop_all(); db.create_all(); print('Database reset complete')"
```

### 2. Password Hashing Issues
**Symptoms:** Password verification always fails

**Check:** Run this test in Python:
```python
from werkzeug.security import generate_password_hash, check_password_hash

password = "your_password"
hash_val = generate_password_hash(password)
print(f"Hash: {hash_val}")
print(f"Verification: {check_password_hash(hash_val, password)}")
```

### 3. Case Sensitivity Issues
**Symptoms:** Login works sometimes but not others

**Solution:** The backend now converts emails to lowercase automatically. Make sure you're using the exact username (case-sensitive) or email (case-insensitive).

### 4. Database File Permissions
**Symptoms:** Database errors or "table doesn't exist"

**Solution:**
```bash
# Check if database file exists and is writable
ls -la backend/smsguard.db

# If it doesn't exist or has permission issues:
rm -f backend/smsguard.db  # Remove old database
cd backend
python fix_auth.py  # Recreate with proper permissions
```

### 5. Frontend-Backend Communication Issues
**Symptoms:** Network errors or CORS issues

**Check:**
1. Backend is running on `http://localhost:5000`
2. Frontend is configured to use the correct API URL
3. CORS is properly configured in `.env`:
   ```
   CORS_ORIGINS=http://localhost:5173
   ```

## Manual Testing

### Test Registration via curl:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser2","email":"test2@example.com","password":"password123"}'
```

### Test Login via curl:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"usernameOrEmail":"testuser2","password":"password123"}'
```

### Test with the API Test Script:
```bash
cd backend
python test_api.py
```

## Debug Mode

To see detailed debug information, add these debug prints to your login attempts:

1. Check the backend console output when you try to log in
2. Look for DEBUG messages showing:
   - What username/email is being searched
   - Whether the user was found
   - Password verification results

## Environment Check

Make sure your `.env` file has the correct settings:
```bash
# Check your .env file
cat backend/.env

# Should contain:
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///smsguard.db
```

## Database Inspection

To manually inspect your database:
```bash
cd backend
python -c "
from app import create_app, db
from models import User
app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'User: {user.username}, Email: {user.email}, Active: {user.is_active}')
"
```

## Reset Everything

If nothing else works, completely reset:
```bash
cd backend
rm -f smsguard.db  # Remove database
rm -f *.db         # Remove any other db files
python fix_auth.py # Recreate everything
```

## Still Having Issues?

If you're still having problems:

1. **Check the backend console** for error messages
2. **Check browser developer tools** for network errors
3. **Run the debug script** and share the output
4. **Verify your environment** matches the requirements

## Contact Information

If none of these solutions work, please provide:
1. The exact error message
2. Output from `python debug_auth.py`
3. Your `.env` file contents (without sensitive keys)
4. Backend console output when attempting login
