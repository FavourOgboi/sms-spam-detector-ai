"""
SMS Guard Flask Backend Application

This is the main Flask application file that initializes the app,
configures the database, and registers all the API routes.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

# Initialize extensions
jwt = JWTManager()

def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
    
    # Database configuration
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///smsguard.db')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # File upload configuration
    app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads/profile_images')
    app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 5242880))  # 5MB
    
    # Import and initialize database
    from models import db
    db.init_app(app)
    jwt.init_app(app)
    
    # CORS configuration
    cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')
    CORS(app, origins=cors_origins, supports_credentials=True)
    
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import models to ensure they are registered
    from models import User, Prediction

    # Register blueprints
    from routes.auth import auth_bp
    from routes.predictions import predictions_bp
    from routes.users import users_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(predictions_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/user')
    
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
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
