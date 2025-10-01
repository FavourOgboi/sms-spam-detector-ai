"""
Prediction Routes for SMS Guard API

This module handles SMS spam prediction endpoints.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Prediction, db
from ml_model.spam_detector_multi import predict_consensus, get_best_accuracy, explain_consensus_prediction
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

        consensus = consensus_result["consensus"]
        model_results = consensus_result["model_results"]
        # If model_results is a list, convert to object with model names as keys
        if isinstance(model_results, list):
            model_results = {f"Model_{i+1}": res for i, res in enumerate(model_results)}
        majority_prediction = consensus.get("majority_vote", "unknown").lower()
        consensus_confidence = consensus.get("confidence", 0.0)
        # Convert percentage to probability for DB constraint
        db_confidence = consensus_confidence / 100.0

        # Create prediction record (store majority vote and confidence)
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

        # Prepare response data
        response_data = prediction.to_dict()
        response_data["consensus"] = consensus
        response_data["model_results"] = model_results

        # Add top-level prediction and confidence for frontend compatibility
        response_data = {
            "consensus": consensus,
            "model_results": model_results,
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
        from ml_model.spam_detector_multi import get_all_metrics
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
