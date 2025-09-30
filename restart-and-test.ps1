# Restart and Test Password Reset System
Write-Host "🔄 Restarting Password Reset System" -ForegroundColor Cyan

# Kill any existing processes
Write-Host "🛑 Stopping existing processes..." -ForegroundColor Yellow
Get-Process -Name "python" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name "node" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

# Create database tables
Write-Host "🗄️ Creating database tables..." -ForegroundColor Yellow
python -c "
import sys, os
sys.path.append('backend')
from app import create_app
from models import db, User, PasswordResetToken

app = create_app()
with app.app_context():
    db.create_all()
    print('✅ Database tables created')
    
    # Check tables
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f'📊 Tables: {tables}')
    
    if 'password_reset_tokens' in tables:
        print('✅ PasswordResetToken table exists')
    else:
        print('❌ PasswordResetToken table missing')
"

# Start backend
Write-Host "🚀 Starting backend..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "backend/app.py" -WindowStyle Minimized

Start-Sleep -Seconds 5

# Test backend health
Write-Host "🏥 Testing backend health..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET -TimeoutSec 5
    if ($healthResponse.StatusCode -eq 200) {
        Write-Host "✅ Backend is running!" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend not responding" -ForegroundColor Red
    exit 1
}

# Test forgot password
Write-Host "📧 Testing forgot password..." -ForegroundColor Yellow
$forgotData = @{
    email = "ogboifavourifeanyichukwu@gmail.com"
} | ConvertTo-Json

try {
    $forgotResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/forgot-password" -Method POST -Body $forgotData -ContentType "application/json" -TimeoutSec 10
    
    if ($forgotResponse.StatusCode -eq 200) {
        $responseData = $forgotResponse.Content | ConvertFrom-Json
        Write-Host "✅ Forgot password successful!" -ForegroundColor Green
        
        if ($responseData.resetLink) {
            Write-Host "🔗 Reset Link: $($responseData.resetLink)" -ForegroundColor Cyan
            
            # Extract token
            if ($responseData.resetLink -match "token=([^&]+)") {
                $token = $matches[1]
                Write-Host "🎫 Token: $($token.Substring(0, [Math]::Min(20, $token.Length)))..." -ForegroundColor Gray
                
                # Test reset password immediately
                Write-Host "🔑 Testing password reset..." -ForegroundColor Yellow
                $resetData = @{
                    token = $token
                    password = "NewTestPassword123!"
                } | ConvertTo-Json
                
                try {
                    $resetResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/reset-password" -Method POST -Body $resetData -ContentType "application/json" -TimeoutSec 10
                    
                    if ($resetResponse.StatusCode -eq 200) {
                        Write-Host "✅ Password reset successful!" -ForegroundColor Green
                        $resetResponseData = $resetResponse.Content | ConvertFrom-Json
                        Write-Host "📥 Response: $($resetResponse.Content)" -ForegroundColor Gray
                    } else {
                        Write-Host "❌ Password reset failed with status $($resetResponse.StatusCode)" -ForegroundColor Red
                        Write-Host "📥 Response: $($resetResponse.Content)" -ForegroundColor Gray
                    }
                } catch {
                    Write-Host "❌ Password reset error: $($_.Exception.Message)" -ForegroundColor Red
                    if ($_.Exception.Response) {
                        $errorResponse = $_.Exception.Response.GetResponseStream()
                        $reader = New-Object System.IO.StreamReader($errorResponse)
                        $errorContent = $reader.ReadToEnd()
                        Write-Host "📥 Error Response: $errorContent" -ForegroundColor Red
                    }
                }
            }
        }
    }
} catch {
    Write-Host "❌ Forgot password error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 Test Complete!" -ForegroundColor Cyan
Write-Host "💡 If successful, you can now test in browser at:" -ForegroundColor Yellow
Write-Host "   http://localhost:5173/forgot-password" -ForegroundColor Cyan
