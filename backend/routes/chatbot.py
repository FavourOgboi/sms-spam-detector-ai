"""
Chatbot API Routes

Provides endpoints for AI chatbot conversations, integrating with
spam detection model and providing personalized user assistance.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import os

# Add the parent directory to the path to import chatbot service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_chatbot.chatbot_service import get_chatbot_service
from ml_model.spam_detector import spam_detector
from models import User

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat_with_ai():
    """
    Chat with AI assistant about SMS messages
    Expected: POST /api/chatbot/chat
    Headers: Authorization: Bearer <token>
    Body: {
        "message": "User's message or SMS content",
        "analyze_message": true/false (optional, default: true)
    }
    """
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get request data
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
                'error': 'Message cannot be empty'
            }), 400
        
        analyze_message = data.get('analyze_message', True)
        
        # Get chatbot service with spam detector
        chatbot = get_chatbot_service(spam_detector)
        
        # Chat with the AI
        response = chatbot.chat_with_user(
            user_id=str(current_user_id),
            user_name=user.username,  # Use username as display name
            message=message,
            analyze_with_model=analyze_message
        )
        
        if response['success']:
            return jsonify({
                'success': True,
                'data': {
                    'bot_response': response['bot_response'],
                    'user_message': response['user_message'],
                    'timestamp': response['timestamp'],
                    'spam_analysis': response.get('spam_analysis'),
                    'explanation': response.get('explanation'),
                    'conversation_length': response.get('conversation_length', 1),
                    'processing_time_ms': response.get('processing_time_ms', 0)
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': response.get('error', 'Chat failed')
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Chat error: {str(e)}'
        }), 500

@chatbot_bp.route('/conversation', methods=['GET'])
@jwt_required()
def get_conversation_history():
    """
    Get conversation history for current user
    Expected: GET /api/chatbot/conversation
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get chatbot service
        chatbot = get_chatbot_service()
        
        # Get conversation history
        conversation = chatbot.get_user_conversation(str(current_user_id))
        summary = chatbot.get_conversation_summary(str(current_user_id))
        
        return jsonify({
            'success': True,
            'data': {
                'conversation': conversation,
                'summary': summary,
                'user_name': user.username
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get conversation: {str(e)}'
        }), 500

@chatbot_bp.route('/clear', methods=['POST'])
@jwt_required()
def clear_conversation():
    """
    Clear conversation history for current user
    Expected: POST /api/chatbot/clear
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get chatbot service
        chatbot = get_chatbot_service()
        
        # Clear conversation
        if str(current_user_id) in chatbot.conversation_memory:
            del chatbot.conversation_memory[str(current_user_id)]
        
        return jsonify({
            'success': True,
            'message': f'Conversation cleared for {user.username}'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to clear conversation: {str(e)}'
        }), 500

@chatbot_bp.route('/quick-analyze', methods=['POST'])
@jwt_required()
def quick_analyze_message():
    """
    Quick analysis of a message with AI advice (without full conversation)
    Expected: POST /api/chatbot/quick-analyze
    Headers: Authorization: Bearer <token>
    Body: {
        "message": "SMS message to analyze"
    }
    """
    try:
        # Get current user
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get request data
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
                'error': 'Message cannot be empty'
            }), 400
        
        # Get chatbot service
        chatbot = get_chatbot_service(spam_detector)
        
        # Analyze message context
        context = chatbot.analyze_message_context(message)
        
        # Get spam prediction
        spam_prediction = None
        explanation = None
        
        try:
            spam_prediction = spam_detector.predict(message)
            explanation = spam_detector.explain_prediction(message, num_features=3)
        except Exception as e:
            print(f"Error in spam analysis: {e}")
        
        # Generate quick advice
        advice = chatbot.generate_personalized_response(
            user_name=user.username,
            message=message,
            spam_prediction=spam_prediction,
            explanation=explanation,
            conversation_history=[]
        )
        
        return jsonify({
            'success': True,
            'data': {
                'message': message,
                'advice': advice,
                'context_analysis': context,
                'spam_prediction': spam_prediction,
                'explanation': explanation,
                'user_name': user.username
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@chatbot_bp.route('/scenarios', methods=['GET'])
@jwt_required()
def get_spam_scenarios():
    """
    Get information about common spam scenarios
    Expected: GET /api/chatbot/scenarios
    Headers: Authorization: Bearer <token>
    """
    try:
        # Get chatbot service
        chatbot = get_chatbot_service()
        
        # Format scenarios for frontend
        scenarios = {}
        for scenario_name, scenario_data in chatbot.spam_scenarios.items():
            scenarios[scenario_name] = {
                'name': scenario_name.replace('_', ' ').title(),
                'keywords': scenario_data['keywords'],
                'advice': scenario_data['advice']
            }
        
        return jsonify({
            'success': True,
            'data': {
                'scenarios': scenarios,
                'total_scenarios': len(scenarios)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get scenarios: {str(e)}'
        }), 500
