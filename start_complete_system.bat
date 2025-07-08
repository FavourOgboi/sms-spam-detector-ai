@echo off
echo ================================================
echo SMS Guard Complete System Startup
echo ================================================

echo.
echo 1. Starting Flask Backend...
echo ================================================
start "SMS Guard Backend" cmd /k "python simple_backend.py"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo 2. Testing Backend Connection...
echo ================================================
python test_full_integration.py

echo.
echo 3. Backend is ready! Now start your React frontend:
echo ================================================
echo    npm run dev
echo.
echo 4. Then open your browser and go to:
echo    http://localhost:5173
echo.
echo 5. Login with:
echo    Username: demo
echo    Password: demo123
echo.
echo ================================================
echo System startup complete!
echo ================================================
pause
