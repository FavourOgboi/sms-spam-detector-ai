@echo off
echo Starting SMS Spam Detector Development Environment...
echo.

echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd backend && echo Starting backend... && python app.py && echo Backend stopped. Press any key to close. && pause"

echo [2/2] Waiting 3 seconds then starting Frontend...
timeout /t 3 /nobreak > nul

start "Frontend Server" cmd /k "echo Starting frontend... && npm run dev:frontend-only && echo Frontend stopped. Press any key to close. && pause"

echo.
echo ✅ Both servers should be starting now!
echo 🔥 Backend: http://localhost:5000/api/health
echo ⚡ Frontend: http://localhost:5173
echo.
echo 🧪 To test forgot password:
echo    1. Go to http://localhost:5173/login
echo    2. Click "Forgot your password?"
echo    3. Enter your test user email
echo    4. Check console for reset link (development mode)
echo.
echo Press any key to exit this script (servers will keep running)...
pause > nul
