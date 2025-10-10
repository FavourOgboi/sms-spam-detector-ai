"""
Prediction Routes for SMS Guard API

This module handles SMS spam prediction endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
try:
    from backend.models import User, Prediction, db
except ImportError:
    from models import User, Prediction, db
from backend.ml_model.spam_detector_multi import predict_consensus, get_best_accuracy, explain_consensus_prediction, predict_weighted_consensus
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
        
        # Make consensus prediction using all models
        consensus_result = predict_consensus(message)
        weighted_result = predict_weighted_consensus(message, metric='f1')

        consensus = consensus_result["consensus"]
        model_results = consensus_result["model_results"]
        
        # If model_results is a list, convert to object with model names as keys
        if isinstance(model_results, list):
            model_results = {f"Model_{i+1}": res for i, res in enumerate(model_results)}
            
        majority_prediction = consensus.get("majority_vote", "unknown").lower()
        consensus_confidence = consensus.get("confidence", 0.0)
        db_confidence = consensus_confidence / 100.0

        # Create prediction record
        prediction = Prediction(
            user_id=current_user_id,
            message=message,
            prediction=majority_prediction,
            confidence=db_confidence,
            processing_time_ms=None,
            model_version="N/A"
        )
        db.session.add(prediction)
        db.session.commit()

        # Determine confidence level and suggestion
        weighted_conf = None
        if weighted_result['weighted_spam_prob'] is not None:
            if weighted_result['weighted_majority'] == 'spam':
                weighted_conf = weighted_result['weighted_spam_prob']
            elif weighted_result['weighted_majority'] == 'ham':
                weighted_conf = 1 - weighted_result['weighted_spam_prob']

        confidence_level = 'N/A'
        suggestion = "The models could not agree. Please review the message carefully."
        if weighted_conf is not None:
            if weighted_conf >= 0.8:
                confidence_level = 'HIGH ⚠️'
            elif weighted_conf >= 0.6:
                confidence_level = 'MEDIUM ℹ️'
            else:
                confidence_level = 'LOW ?'

            if weighted_result['weighted_majority'] == 'spam':
                if weighted_conf >= 0.8:
                    suggestion = "This message is likely SPAM. Be cautious and verify the sender before taking any action."
                elif weighted_conf >= 0.6:
                    suggestion = "This message might be SPAM. Be cautious and verify the sender before taking any action."
                else:
                    suggestion = "There is some suspicion this is SPAM. Use caution and double-check the message source."
            elif weighted_result['weighted_majority'] == 'ham':
                if weighted_conf >= 0.8:
                    suggestion = "This message is likely safe (not spam)."
                elif weighted_conf >= 0.6:
                    suggestion = "This message appears safe, but always be cautious with unknown senders."
                else:
                    suggestion = "The message is probably safe, but confidence is low. Use your judgment."

        # Prepare response data
        response_data = {
            "message": message,
            "consensus": consensus,
            "weighted_result": weighted_result,
            "model_results": model_results,
            "confidence_level": confidence_level,
            "suggestion": suggestion,
            "prediction": consensus.get("majority_vote", "unknown"),
            "confidence": consensus.get("confidence", 0.0)
        }
        
        return jsonify({
            "success": True,
            "data": response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Prediction failed. Please try again.'
        }), 500

@predictions_bp.route('/model/accuracy', methods=['GET'])
@jwt_required()
def get_model_accuracy():
    """
    Get best model accuracy for dashboard
    Expected: GET /api/model/accuracy
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": { "accuracy": float }, "error"?: string }
    """
    try:
        accuracy = get_best_accuracy()
        return jsonify({
            'success': True,
            'data': { 'accuracy': accuracy }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch model accuracy'
        }), 500

@predictions_bp.route('/model/metrics', methods=['GET'])
@jwt_required()
def get_model_metrics():
    """
    Get per-model accuracy and metrics
    Expected: GET /api/model/metrics
    Headers: Authorization: Bearer <token>
    Returns: { "success": boolean, "data": { [modelName]: { accuracy, ... } }, "error"?: string }
    """
    try:
        from backend.ml_model.spam_detector_multi import get_all_metrics
        metrics = get_all_metrics()
        return jsonify({
            'success': True,
            'data': metrics
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch model metrics'
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

        # Generate explanation using the consensus model
        print(f"EXPLAIN: Generating explanation for message: {message[:50]}...")
        explanation_result = explain_consensus_prediction(message, num_features)
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
