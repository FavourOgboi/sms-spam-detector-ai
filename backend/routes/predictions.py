"""
Prediction Routes for SMS Guard API

This module handles SMS spam prediction endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Prediction, db
from ml_model.spam_detector import spam_detector
import time

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict_spam():
    """
    SMS Spam Prediction endpoint
    Expected: POST /api/predict
    Headers: Authorization: Bearer <token>
    Body: { "message": "string" }
    Returns: { "success": boolean, "data": PredictionResult, "error"?: string }
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
        
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        if len(message) > 1000:
            return jsonify({
                'success': False,
                'error': 'Message too long. Maximum 1000 characters allowed.'
            }), 400
        
        # Make prediction using the ML model
        start_time = time.time()
        prediction_result = spam_detector.predict(message)

        # Generate basic explanation (top 5 features for quick display)
        try:
            explanation_result = spam_detector.explain_prediction(message, num_features=5)
            basic_explanation = None

            if explanation_result.get('success') and explanation_result.get('explanation'):
                # Extract top features for basic display
                features = explanation_result['explanation'].get('features', [])
                basic_explanation = {
                    'method': explanation_result['explanation'].get('method', 'Unknown'),
                    'summary': explanation_result['explanation'].get('summary', ''),
                    'top_features': features[:5]  # Top 5 for basic display
                }
        except Exception as e:
            print(f"Basic explanation error: {e}")
            basic_explanation = None

        # Create prediction record
        prediction = Prediction(
            user_id=current_user_id,
            message=message,
            prediction=prediction_result['prediction'],
            confidence=prediction_result['confidence'],
            processing_time_ms=prediction_result.get('processing_time_ms'),
            model_version=prediction_result.get('model_version')
        )

        db.session.add(prediction)
        db.session.commit()

        # Prepare response data
        response_data = prediction.to_dict()

        # Add basic explanation if available
        if basic_explanation:
            response_data['explanation'] = basic_explanation

        return jsonify({
            'success': True,
            'data': response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Prediction failed. Please try again.'
        }), 500

@predictions_bp.route('/model/info', methods=['GET'])
@jwt_required()
def get_model_info():
    """
    Get ML model information
    Expected: GET /api/model/info
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": ModelInfo, "error"?: string }
    """
    try:
        model_info = spam_detector.get_model_info()
        
        return jsonify({
            'success': True,
            'data': model_info
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch model information'
        }), 500

@predictions_bp.route('/explain', methods=['POST'])
@jwt_required()
def explain_prediction():
    """
    Explain SMS spam prediction using LIME
    Expected: POST /api/explain
    Headers: Authorization: Bearer <token>
    Body: { "message": "string", "num_features"?: number }
    Returns: { "success": boolean, "data": ExplanationResult, "error"?: string }
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

        message = data.get('message', '').strip()
        num_features = data.get('num_features', 10)

        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400

        if len(message) > 1000:
            return jsonify({
                'success': False,
                'error': 'Message too long. Maximum 1000 characters allowed.'
            }), 400

        # Generate explanation using the ML model
        print(f"EXPLAIN: Generating explanation for message: {message[:50]}...")
        explanation_result = spam_detector.explain_prediction(message, num_features)
        print(f"EXPLAIN: Result success: {explanation_result.get('success', False)}")

        if explanation_result.get('success'):
            return jsonify({
                'success': True,
                'data': explanation_result
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': explanation_result.get('error', 'Failed to generate explanation')
            }), 500

    except Exception as e:
        print(f"EXPLANATION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Explanation failed: {str(e)}'
        }), 500
