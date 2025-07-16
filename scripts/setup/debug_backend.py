#!/usr/bin/env python3
"""
Debug backend startup issues
"""

import sys
import os

print("🔍 Backend Debug Information")
print("=" * 50)

# Check Python version
print(f"Python version: {sys.version}")

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Check if backend directory exists
backend_path = os.path.join(os.getcwd(), 'backend')
print(f"Backend directory exists: {os.path.exists(backend_path)}")

if os.path.exists(backend_path):
    print(f"Backend contents: {os.listdir(backend_path)}")

# Try to import Flask
try:
    import flask
    print(f"✅ Flask available: {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask not available: {e}")

# Try to import other dependencies
dependencies = ['flask_sqlalchemy', 'flask_cors', 'flask_jwt_extended', 'werkzeug']

for dep in dependencies:
    try:
        __import__(dep)
        print(f"✅ {dep} available")
    except ImportError:
        print(f"❌ {dep} not available")

# Try to run the backend app
print("\n🚀 Attempting to start backend...")
try:
    sys.path.append('backend')
    from app import create_app
    
    app = create_app()
    print("✅ App created successfully")
    
    # Test a simple route
    with app.test_client() as client:
        response = client.get('/api/health')
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.get_json()}")
        
except Exception as e:
    print(f"❌ Error creating app: {e}")
    import traceback
    traceback.print_exc()

print("\n💡 If you see errors above, try:")
print("   pip install -r backend/requirements.txt")
