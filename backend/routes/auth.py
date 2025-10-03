"""
Authentication Routes for SMS Guard API

This module handles all authentication-related endpoints including
login, register, logout, and user verification.
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
from models import User, PasswordResetToken, db
import re
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

auth_bp = Blueprint('auth', __name__)



def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Simple password validation"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

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

        if not user:
            return jsonify({
                'success': False,
                'error': 'Account does not exist. Please check your username/email or register for a new account.'
            }), 401

        if not user.check_password(password):
            return jsonify({
                'success': False,
                'error': 'Incorrect password. Please try again.'
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
    """Simple user registration that actually works"""
    print("=== REGISTRATION REQUEST ===")

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        print(f"Registration attempt: {username}, {email}")

        # Basic validation
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'All fields are required'}), 400

        if len(username) < 3:
            return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400

        if '@' not in email:
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400

        if len(password) < 8:
            return jsonify({'success': False, 'error': 'Password must be at least 8 characters'}), 400

        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 409

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        print(f"✅ User created: {user.id}")

        # Create token
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
        print(f"❌ Registration error: {e}")
        return jsonify({'success': False, 'error': 'Registration failed'}), 500

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

# --- Password Reset System ---
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Request password reset - generates token and sends email
    Expected: POST /api/auth/forgot-password
    Body: { "email": "string" }
    Returns: { "success": boolean, "message": string }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        email = data.get('email', '').strip().lower()

        if not email:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400

        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # Always return success message for security (don't reveal if email exists)
        success_message = "If that email exists in our system, a password reset link has been sent."

        if not user:
            return jsonify({
                'success': True,
                'message': success_message
            }), 200

        # Generate reset token
        reset_token = PasswordResetToken.create_for_user(user, hours_valid=1)

        # Create reset link
        reset_link = f"http://localhost:5173/reset-password?token={reset_token.token}"

        # Send email with multiple fallback options
        email_sent = False
        email_method = ""

        # Method 1: Try SendGrid first (Primary)
        try:
            sendgrid_api_key = os.environ.get('SENDGRID_API_KEY') or current_app.config.get('SENDGRID_API_KEY')
            print(f"🔍 SendGrid API Key found: {'Yes' if sendgrid_api_key else 'No'}")
            if sendgrid_api_key:
                print("📧 Attempting to send email via SendGrid...")
                email_sent = send_email_sendgrid(user.email, reset_link, sendgrid_api_key)
                if email_sent:
                    email_method = "SendGrid"
                    print(f"✅ SendGrid email sent successfully!")
            else:
                print("⚠️ No SendGrid API key found, skipping SendGrid")
        except Exception as sg_err:
            print(f"⚠️ SendGrid error: {sg_err}")

        # Method 2: Try Flask-Mail as fallback
        if not email_sent:
            try:
                print("📧 Attempting to send email via Flask-Mail...")
                if current_app.config.get('MAIL_USERNAME') and current_app.config.get('MAIL_PASSWORD'):
                    mail = current_app.extensions.get('mail')
                    if mail:
                        email_sent = send_email_flask_mail(user.email, reset_link, mail)
                        if email_sent:
                            email_method = "Flask-Mail"
            except Exception as mail_err:
                print(f"⚠️ Flask-Mail error: {mail_err}")

        # Method 3: Development mode fallback
        if not email_sent:
            print("📧 Using development mode - showing reset link in response")
            return jsonify({
                "success": True,
                "message": "Password reset link generated (Email service unavailable)",
                "resetLink": reset_link,
                "debug": True
            }), 200

        # Email sent successfully
        print(f"✅ Password reset email sent via {email_method} to {email}")
        return jsonify({
            "success": True,
            "message": success_message
        }), 200

    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process request'
        }), 500


def send_email_sendgrid(email, reset_link, api_key):
    """Send password reset email using SendGrid"""
    try:
        sg = SendGridAPIClient(api_key)

        # Create email content
        subject = "Reset Your SMS Guard Password"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 SMS Guard</h1>
                    <h2>Password Reset Request</h2>
                </div>
                <div class="content">
                    <p>Hello,</p>
                    <p>We received a request to reset your SMS Guard password. Click the button below to create a new password:</p>
                    <p style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset My Password</a>
                    </p>
                    <p><strong>This link will expire in 1 hour</strong> for your security.</p>
                    <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.</p>
                    <div class="footer">
                        <p>Best regards,<br>SMS Guard Team</p>
                        <p><em>Protecting you from spam, one message at a time.</em></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        SMS Guard - Password Reset Request

        Hello,

        We received a request to reset your SMS Guard password.

        Click this link to reset your password: {reset_link}

        This link will expire in 1 hour for your security.

        If you didn't request this password reset, please ignore this email.

        Best regards,
        SMS Guard Team
        """

        message = Mail(
            from_email='noreply@smsguard.com',  # You can customize this
            to_emails=email,
            subject=subject,
            html_content=html_content,
            plain_text_content=text_content
        )

        response = sg.send(message)
        print(f"📧 SendGrid response: {response.status_code}")
        return response.status_code == 202  # SendGrid returns 202 for success

    except Exception as e:
        print(f"❌ SendGrid error: {e}")
        return False


def send_email_flask_mail(email, reset_link, mail):
    """Send password reset email using Flask-Mail"""
    try:
        subject = "Reset Your SMS Guard Password"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center;">
                <h1>🔐 SMS Guard</h1>
                <h2>Password Reset Request</h2>
            </div>
            <div style="background: #f9f9f9; padding: 30px;">
                <p>Hello,</p>
                <p>We received a request to reset your SMS Guard password. Click the link below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" style="display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">Reset My Password</a>
                </p>
                <p><strong>This link will expire in 1 hour</strong> for your security.</p>
                <p>If you didn't request this password reset, please ignore this email.</p>
                <p style="text-align: center; margin-top: 20px; color: #666;">
                    Best regards,<br>SMS Guard Team
                </p>
            </div>
        </div>
        """

        text_body = f"""
        SMS Guard - Password Reset Request

        Hello,

        We received a request to reset your SMS Guard password.

        Click this link to reset your password: {reset_link}

        This link will expire in 1 hour for your security.

        If you didn't request this password reset, please ignore this email.

        Best regards,
        SMS Guard Team
        """

        msg = Message(
            subject=subject,
            recipients=[email],
            body=text_body,
            html=html_body
        )
        mail.send(msg)
        return True

    except Exception as e:
        print(f"❌ Flask-Mail error: {e}")
        return False




    except Exception as e:
        print(f"❌ Forgot password error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to process request'
        }), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password using token
    Expected: POST /api/auth/reset-password
    Body: { "token": "string", "password": "string" }
    Returns: { "success": boolean, "message": string }
    """
    try:
        print("🔄 Reset password request received")
        data = request.get_json()
        print(f"📥 Request data: {data}")

        if not data:
            print("❌ No data provided")
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400

        token = data.get('token', '').strip()
        new_password = data.get('password', '')
        user_id = data.get('user_id', '').strip()  # Optional for backward compatibility

        print(f"🎫 Token: {token[:20] if token else 'None'}...")
        print(f"🔑 Password provided: {'Yes' if new_password else 'No'}")
        print(f"👤 User ID provided: {'Yes' if user_id else 'No'}")

        if not token:
            print("❌ Token missing")
            return jsonify({
                'success': False,
                'error': 'Reset token is required'
            }), 400

        if not new_password:
            print("❌ Password missing")
            return jsonify({
                'success': False,
                'error': 'New password is required'
            }), 400

        # Validate password strength
        print("🔍 Validating password strength...")
        valid_pw, pw_msg = validate_password(new_password)
        if not valid_pw:
            print(f"❌ Password validation failed: {pw_msg}")
            return jsonify({
                'success': False,
                'error': pw_msg
            }), 400

        # Find and validate token
        print("🔍 Looking up reset token...")
        reset_token = PasswordResetToken.query.filter_by(token=token).first()

        if not reset_token:
            print("❌ Reset token not found in database")
            return jsonify({
                'success': False,
                'error': 'Invalid reset token'
            }), 400

        print(f"✅ Token found: ID={reset_token.id}, User ID={reset_token.user_id}")
        print(f"🕐 Token expiry: {reset_token.expiry}")
        print(f"🔒 Token used: {reset_token.used}")

        if not reset_token.is_valid():
            print("❌ Token is not valid (expired or used)")
            return jsonify({
                'success': False,
                'error': 'Reset token has expired or been used'
            }), 400

        # Get user and update password
        user = User.query.get(reset_token.user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        # Update password
        user.set_password(new_password)

        # Mark token as used
        reset_token.mark_as_used()

        print(f"✅ Password reset successful for user: {user.email}")
        return jsonify({
            'success': True,
            'message': 'Password has been reset successfully'
        }), 200

    except Exception as e:
        print(f"❌ Reset password error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to reset password'
        }), 500
