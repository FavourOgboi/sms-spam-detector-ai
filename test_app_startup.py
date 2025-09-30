"""
Test script to debug app startup issues
"""
import sys
import os

print("=" * 60)
print("SMS Guard App Startup Diagnostic")
print("=" * 60)

# Check Python version
print(f"\n1. Python Version: {sys.version}")

# Check if we're in the right directory
print(f"\n2. Current Directory: {os.getcwd()}")
print(f"   Backend exists: {os.path.exists('backend')}")
print(f"   Backend/app.py exists: {os.path.exists('backend/app.py')}")

# Try importing Flask
print("\n3. Testing Flask import...")
try:
    import flask
    print(f"   ✅ Flask {flask.__version__} imported successfully")
except ImportError as e:
    print(f"   ❌ Flask import failed: {e}")
    sys.exit(1)

# Try importing other dependencies
print("\n4. Testing other dependencies...")
dependencies = [
    'flask_sqlalchemy',
    'flask_cors',
    'flask_jwt_extended',
    'flask_mail',
    'werkzeug',
    'dotenv'
]

for dep in dependencies:
    try:
        __import__(dep)
        print(f"   ✅ {dep} imported successfully")
    except ImportError as e:
        print(f"   ❌ {dep} import failed: {e}")

# Change to backend directory
print("\n5. Changing to backend directory...")
os.chdir('backend')
print(f"   Current directory: {os.getcwd()}")

# Try importing models
print("\n6. Testing models import...")
try:
    from models import db, User, Prediction
    print("   ✅ Models imported successfully")
except Exception as e:
    print(f"   ❌ Models import failed: {e}")
    import traceback
    traceback.print_exc()

# Try creating the app
print("\n7. Testing app creation...")
try:
    from app import create_app
    print("   ✅ create_app imported successfully")
    
    app = create_app()
    print("   ✅ App created successfully")
    
    # Test the app
    with app.test_client() as client:
        response = client.get('/api/health')
        print(f"   ✅ Health check status: {response.status_code}")
        print(f"   ✅ Health check response: {response.get_json()}")
    
    print("\n8. Starting the Flask server...")
    print("   Backend will run on: http://localhost:5000")
    print("   Press Ctrl+C to stop")
    print("=" * 60)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"   ❌ App creation/startup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

