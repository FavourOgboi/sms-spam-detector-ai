"""
User Management Routes for SMS Guard API

This module handles user profile, statistics, and account management endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import User, Prediction, UserStats, db
import os
import uuid

users_bp = Blueprint('users', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """
    Get user statistics
    Expected: GET /api/user/stats
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": UserStats, "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        # Calculate user statistics
        stats = UserStats.calculate_stats(current_user_id)
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        print(f"Stats error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch user statistics'
        }), 500

@users_bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_user_predictions():
    """
    Get user's prediction history
    Expected: GET /api/user/predictions
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": PredictionResult[], "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        # Get user's predictions with pagination support
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        predictions = Prediction.query.filter_by(user_id=current_user_id)\
            .order_by(Prediction.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in predictions.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': predictions.total,
                'pages': predictions.pages
            }
        }), 200
        
    except Exception as e:
        print(f"Predictions fetch error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch predictions'
        }), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile
    Expected: PUT /api/user/profile
    Headers: Authorization: Bearer <token>
    Content-Type: multipart/form-data or application/json
    Returns: { "success": boolean, "data": User, "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Update allowed fields
        if 'username' in data:
            username = data['username'].strip()
            if len(username) < 3:
                return jsonify({
                    'success': False,
                    'error': 'Username must be at least 3 characters long'
                }), 400
            
            # Check if username is already taken
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({
                    'success': False,
                    'error': 'Username already taken'
                }), 409
            
            user.username = username
        
        if 'email' in data:
            email = data['email'].strip().lower()
            # Basic email validation
            if '@' not in email or '.' not in email:
                return jsonify({
                    'success': False,
                    'error': 'Invalid email format'
                }), 400
            
            # Check if email is already taken
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({
                    'success': False,
                    'error': 'Email already registered'
                }), 409
            
            user.email = email
        
        if 'bio' in data:
            bio = data['bio'].strip()
            if len(bio) > 500:
                return jsonify({
                    'success': False,
                    'error': 'Bio must be less than 500 characters'
                }), 400
            user.bio = bio
        
        if 'theme' in data:
            theme = data['theme']
            if theme in ['light', 'dark']:
                user.theme = theme
        
        # Handle profile image upload
        if 'profileImage' in request.files:
            file = request.files['profileImage']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                
                # Save file
                from flask import current_app
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Update user profile image
                user.profile_image = f'/uploads/profile_images/{filename}'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Profile update error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to update profile'
        }), 500

@users_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change user password
    Expected: PUT /api/user/change-password
    Headers: Authorization: Bearer <token>
    Body: { "currentPassword": "string", "newPassword": "string", "confirmNewPassword": "string" }
    Returns: { "success": boolean, "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'User not found or inactive'
            }), 401
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        current_password = data.get('currentPassword', '')
        new_password = data.get('newPassword', '')
        confirm_password = data.get('confirmNewPassword', '')
        
        # Validate current password
        if not user.check_password(current_password):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 400
        
        # Validate new password
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 6 characters long'
            }), 400
        
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'error': 'New passwords do not match'
            }), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Password change error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to change password'
        }), 500

@users_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    """
    Delete user account
    Expected: DELETE /api/user/delete
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "error"?: string }
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Delete user (cascade will delete predictions)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Account deletion error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to delete account'
        }), 500
