"""
Authentication Routes for SMS Guard API

This module handles all authentication-related endpoints including
login, register, logout, and user verification.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, db
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    return True, ""

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 50:
        return False, "Username must be less than 50 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, ""

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Expected: POST /api/auth/login
    Body: { "usernameOrEmail": "string", "password": "string" }
    Returns: { "success": boolean, "data": { "token": string, "user": User }, "error"?: string }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        username_or_email = data.get('usernameOrEmail', '').strip()
        password = data.get('password', '')
        
        if not username_or_email or not password:
            return jsonify({
                'success': False,
                'error': 'Username/email and password are required'
            }), 400
        
        # Find user by username or email
        user = None
        if '@' in username_or_email:
            user = User.query.filter_by(email=username_or_email.lower()).first()
            print(f"DEBUG: Searching by email: {username_or_email.lower()}")
        else:
            user = User.query.filter_by(username=username_or_email).first()
            print(f"DEBUG: Searching by username: {username_or_email}")

        print(f"DEBUG: User found: {user is not None}")
        if user:
            print(f"DEBUG: User details - ID: {user.id}, Username: {user.username}, Email: {user.email}")
            password_check = user.check_password(password)
            print(f"DEBUG: Password check result: {password_check}")

        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
        
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Account is deactivated'
            }), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'token': access_token,
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    Expected: POST /api/auth/register
    Body: { "username": "string", "email": "string", "password": "string" }
    Returns: { "success": boolean, "data": { "token": string, "user": User }, "error"?: string }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not username or not email or not password:
            return jsonify({
                'success': False,
                'error': 'Username, email, and password are required'
            }), 400
        
        # Validate username
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Validate email
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # Validate password
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'token': access_token,
                'user': user.to_dict()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    Expected: GET /api/auth/me
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": User, "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch user information'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout endpoint
    Expected: POST /api/auth/logout
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean }
    """
    # In a more sophisticated implementation, you might want to blacklist the token
    # For now, we'll just return success as the frontend will remove the token
    return jsonify({
        'success': True,
        'message': 'Successfully logged out'
    }), 200
