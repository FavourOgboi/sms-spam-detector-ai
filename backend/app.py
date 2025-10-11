"""
SMS Guard Flask Backend Application

This is the main Flask application file that initializes the app,
configures the database, and registers all the API routes.
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
import os
from datetime import timedelta

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")


jwt = JWTManager()
mail = Mail()

def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__)
    
    # My Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set. Please configure your PostgreSQL connection.")
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads/profile_images')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 5242880))    # 5MB

    # Email configuration - SendGrid (Primary)
    app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')

    # Email configuration - Flask-Mail (Fallback)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME'))

    # Print email configuration status
    if app.config['SENDGRID_API_KEY']:
        print(f"📧 SendGrid configured: API key found")
    elif app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
        print(f"📧 Gmail configured: {app.config['MAIL_USERNAME']}")
    else:
        print("⚠️  No email service configured - using development mode")
    
    # Create upload folder if it doesn't exist
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Created upload folder: {upload_folder}")
    
    
    from backend.models import db
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    
    # --- CORS FIX: Allow all origins for development (simpler approach) ---
    CORS(app,
         origins="*",
         supports_credentials=False,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    print("🌐 CORS configured to allow all origins with full headers and methods")
    # -----------------------------------------------------------------------------------------------------------------
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import models to ensure they are registered
    from backend.models import User, Prediction, PasswordResetToken

    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.predictions import predictions_bp
    from backend.routes.users import users_bp
    from backend.routes.chatbot import chatbot_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predictions_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/user')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({
            'success': False,
            'error': 'File too large. Maximum size is 5MB.'
        }), 413
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'success': True,
            'message': 'SMS Guard API is running',
            'version': '1.0.0'
        })

    # Forgot password page (Flask-only solution)
    @app.route('/forgot-password')
    def forgot_password_page():
        """Serve the forgot password HTML page"""
        return send_from_directory('templates', 'forgot_password.html')

    # Simple login page redirect
    @app.route('/login')
    def login_redirect():
        """Redirect to React frontend login or show simple message"""
        return '''
        <html>
        <head><title>SMS Guard - Login</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🔐 SMS Guard</h1>
            <p>Please use the React frontend at <a href="http://localhost:5179">http://localhost:5179</a></p>
            <p>SMS Spam Detection Application</p>
        </body>
        </html>
        '''

    # Serve uploaded profile images on both /uploads/profile_images and /api/uploads/profile_images
    @app.route('/uploads/profile_images/<filename>')
    @app.route('/api/uploads/profile_images/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database initialized")

        # Check existing users
        from backend.models import User
        users = User.query.all()
        print(f"Current users in database: {len(users)}")
        for user in users:
            print(f"  - {user.username} ({user.email})")

        print("Ready for new user registrations")

    return app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

# Expose app instance for gunicorn (no --factory)
app = create_app()
