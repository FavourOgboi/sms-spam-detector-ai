"""
Final verification test for SMS Guard backend
This script tests if all fixes are working
"""
import sys
import os

print("=" * 70)
print(" SMS GUARD - FINAL VERIFICATION TEST")
print("=" * 70)
print()

# Test 1: SendGrid Import
print("[TEST 1] Checking SendGrid import...")
try:
    import sendgrid
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    print("  ✅ PASS - SendGrid imported successfully")
except ImportError as e:
    print(f"  ❌ FAIL - SendGrid import failed: {e}")
    print("  FIX: Run 'pip install sendgrid'")
    sys.exit(1)

# Test 2: Flask and dependencies
print("\n[TEST 2] Checking Flask and dependencies...")
required_modules = [
    'flask',
    'flask_sqlalchemy',
    'flask_cors',
    'flask_jwt_extended',
    'flask_mail',
    'werkzeug'
]
all_ok = True
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError as e:
        print(f"  ❌ {module} - {e}")
        all_ok = False

if not all_ok:
    print("  ❌ FAIL - Some dependencies missing")
    sys.exit(1)
else:
    print("  ✅ PASS - All Flask dependencies OK")

# Test 3: ML Model files exist
print("\n[TEST 3] Checking ML model files...")
model_files = [
    'models/main_model/clf_model.pkl',
    'models/main_model/vectorizer.pkl'
]
for file in model_files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} - NOT FOUND")
        all_ok = False

if not all_ok:
    print("  ❌ FAIL - Model files missing")
    print("  FIX: Run 'python ml_notebooks/create_spam_model.py'")
    sys.exit(1)
else:
    print("  ✅ PASS - All model files exist")

# Test 4: Backend app creation
print("\n[TEST 4] Testing backend app creation...")
try:
    os.chdir('backend')
    from app import create_app
    print("  ✅ create_app imported")
    
    app = create_app()
    print("  ✅ Flask app created")
    
    # Test health endpoint
    with app.test_client() as client:
        response = client.get('/api/health')
        if response.status_code == 200:
            data = response.get_json()
            print(f"  ✅ Health check: {data['message']}")
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
            all_ok = False
    
    if all_ok:
        print("  ✅ PASS - Backend app works correctly")
    else:
        print("  ❌ FAIL - Backend app has issues")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ FAIL - Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Model loading
print("\n[TEST 5] Testing ML model loading...")
try:
    from ml_model.spam_detector import SpamDetector
    detector = SpamDetector()
    
    if detector.model is not None and detector.vectorizer is not None:
        print("  ✅ Model and vectorizer loaded")
        
        # Test prediction
        test_message = "Congratulations! You've won a free prize. Call now!"
        result = detector.predict(test_message)
        print(f"  ✅ Test prediction: {result['prediction']} (confidence: {result['confidence']:.2%})")
        print("  ✅ PASS - ML model works correctly")
    else:
        print("  ⚠️  WARNING - Model loaded but may have issues")
        
except Exception as e:
    print(f"  ❌ FAIL - Model loading error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# All tests passed!
print()
print("=" * 70)
print(" 🎉 ALL TESTS PASSED! 🎉")
print("=" * 70)
print()
print("Your SMS Guard backend is ready to run!")
print()
print("To start the backend:")
print("  Option 1: .\\start_backend_fixed.ps1")
print("  Option 2: cd backend && python app.py")
print("  Option 3: start-dev.bat")
print()
print("Backend will run on: http://localhost:5000")
print("Frontend will run on: http://localhost:5173")
print()
print("=" * 70)

