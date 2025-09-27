@echo off
echo Starting SMS Spam Detector Backend...
echo.

cd backend
echo Current directory: %CD%
echo.

echo Activating conda environment...
call conda activate base

echo.
echo Starting Flask application...
python app.py

pause
