"""
SMS Guard Flask Backend - Main Entry Point

This script starts the Flask development server.
For production, use gunicorn or another WSGI server.
"""

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print("=" * 50)
    print("SMS Guard Flask Backend Starting...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=debug_mode)
