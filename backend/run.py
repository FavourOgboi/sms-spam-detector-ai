"""
SMS Guard Flask Backend - Main Entry Point

This script starts the Flask development server.
For production, use gunicorn or another WSGI server.
"""

import os
import sys

print("Starting backend...")

try:
    from dotenv import load_dotenv
    print("dotenv imported")
except ImportError:
    print("dotenv not found, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    from dotenv import load_dotenv

print("Loading environment...")
load_dotenv()

print("Importing app...")
from app import create_app

print("Creating Flask app...")
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("SMS Guard Flask Backend Starting...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("Register new users at: http://localhost:5173/register")
    print("API will be available at: http://localhost:5000/api")
    print("Frontend should connect from: http://localhost:5173")
    print("=" * 60)
    
    app.run(host=host, port=port, debug=debug_mode)
