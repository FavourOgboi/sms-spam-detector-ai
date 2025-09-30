#!/usr/bin/env powershell
# SMS Guard Backend Startup Script with Fixes

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SMS Guard Backend - Fixed Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python not found!" -ForegroundColor Red
    exit 1
}

# Step 2: Check Flask
Write-Host "[2/5] Checking Flask..." -ForegroundColor Yellow
try {
    $flaskCheck = python -c "import flask; print(f'Flask {flask.__version__}')" 2>&1
    Write-Host "  ✅ $flaskCheck" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Flask not installed!" -ForegroundColor Red
    Write-Host "  Run: pip install flask" -ForegroundColor Yellow
    exit 1
}

# Step 3: Install SendGrid if missing
Write-Host "[3/5] Checking SendGrid..." -ForegroundColor Yellow
$sendgridCheck = python -c "try: import sendgrid; print('installed')" 2>&1
if ($sendgridCheck -like "*installed*") {
    Write-Host "  ✅ SendGrid already installed" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  SendGrid not found. Installing..." -ForegroundColor Yellow
    pip install sendgrid
    Write-Host "  ✅ SendGrid installed" -ForegroundColor Green
}

# Step 4: Check if port 5000 is available
Write-Host "[4/5] Checking port 5000..." -ForegroundColor Yellow
$portCheck = netstat -ano | Select-String ":5000"
if ($portCheck) {
    Write-Host "  ⚠️  Port 5000 is already in use!" -ForegroundColor Yellow
    Write-Host "  Processes using port 5000:" -ForegroundColor Yellow
    Write-Host $portCheck -ForegroundColor Gray
    Write-Host ""
    $response = Read-Host "  Kill processes on port 5000? (y/n)"
    if ($response -eq 'y') {
        $portCheck | ForEach-Object {
            $pid = $_.ToString().Split()[-1]
            Write-Host "  Killing process $pid..." -ForegroundColor Yellow
            taskkill /PID $pid /F 2>&1 | Out-Null
        }
        Write-Host "  ✅ Port 5000 cleared" -ForegroundColor Green
    }
} else {
    Write-Host "  ✅ Port 5000 is available" -ForegroundColor Green
}

# Step 5: Start the backend
Write-Host "[5/5] Starting Flask backend..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Backend will run on: http://localhost:5000" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location backend
python app.py

