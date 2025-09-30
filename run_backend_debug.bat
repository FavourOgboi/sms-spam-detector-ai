@echo off
echo ========================================
echo SMS Guard Backend Debug
echo ========================================
echo.

echo Checking Python...
python --version
echo.

echo Checking Flask...
python -c "import flask; print('Flask installed:', flask.__version__)"
echo.

echo Checking SendGrid...
python -c "try: import sendgrid; print('SendGrid: INSTALLED'); except: print('SendGrid: NOT INSTALLED')"
echo.

echo Changing to backend directory...
cd backend
echo Current directory: %CD%
echo.

echo Attempting to start Flask app...
python app.py

pause

