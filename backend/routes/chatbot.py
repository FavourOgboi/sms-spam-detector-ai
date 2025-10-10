"""
Simple keyword-based chatbot for SMS spam detection help
"""

from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from backend.config import Config
try:
    from backend.models import User
except ImportError:
    from models import User

chatbot_bp = Blueprint('chatbot', __name__)

# Simple keyword-based responses
CHATBOT_RESPONSES = {
    # Greetings
    'greetings': {
        'keywords': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
        'responses': [
            "Hello! I'm your SMS Guard assistant. I can help you understand spam messages and how to stay safe. What would you like to know?",
            "Hi there! I'm here to help you with spam detection. Ask me anything about identifying spam messages!",
            "Hey! I can help you understand spam patterns and protect yourself from scams. How can I assist you?"
        ]
    },
    
    # What is spam
    'what_is_spam': {
        'keywords': ['what is spam', 'define spam', 'spam meaning', 'what spam'],
        'responses': [
            "Spam messages are unwanted or unsolicited messages, often sent in bulk. They can be advertisements, scams, phishing attempts, or malicious content trying to steal your information or money."
        ]
    },
    
    # How to identify spam
    'identify_spam': {
        'keywords': ['how to identify', 'how to detect', 'how to spot', 'recognize spam', 'tell if spam', 'identify spam'],
        'responses': [
            "Here are key signs of spam:\n• Urgent language (ACT NOW, LIMITED TIME)\n• Requests for personal info (passwords, bank details)\n• Too good to be true offers (FREE MONEY, WIN PRIZES)\n• Unknown senders\n• Suspicious links\n• Poor grammar or spelling\n• Threats or pressure tactics"
        ]
    },
    
    # Urgent/pressure tactics
    'urgent': {
        'keywords': ['urgent', 'act now', 'limited time', 'expires', 'hurry', 'immediately', 'right now'],
        'responses': [
            "⚠️ SPAM ALERT: Messages with urgent language like 'ACT NOW' or 'LIMITED TIME' are classic spam tactics. Scammers create false urgency to make you act without thinking. Legitimate companies rarely pressure you this way."
        ]
    },
    
    # Free offers
    'free_offers': {
        'keywords': ['free', 'win', 'prize', 'winner', 'congratulations', 'won', 'claim'],
        'responses': [
            "⚠️ SPAM ALERT: Messages offering free prizes, money, or claiming you've won something are usually scams. If you didn't enter a contest, you didn't win. These messages try to steal your personal information or money."
        ]
    },
    
    # Money/financial
    'money': {
        'keywords': ['money', 'cash', 'bank', 'account', 'credit card', 'payment', 'transfer', 'loan'],
        'responses': [
            "⚠️ SPAM ALERT: Messages about money, bank accounts, or payments from unknown sources are often scams. Never share financial information via text. Banks will never ask for passwords or PINs through SMS."
        ]
    },
    
    # Links and clicking
    'links': {
        'keywords': ['click here', 'link', 'visit', 'website', 'url', 'http'],
        'responses': [
            "⚠️ SPAM ALERT: Be very careful with links in text messages! Spam messages often contain malicious links that can:\n• Steal your information\n• Install malware\n• Lead to fake websites\n\nNever click links from unknown senders. If it's supposedly from a company you know, go directly to their official website instead."
        ]
    },
    
    # Personal information
    'personal_info': {
        'keywords': ['password', 'pin', 'social security', 'verify', 'confirm', 'update', 'account details'],
        'responses': [
            "⚠️ SPAM ALERT: NEVER share personal information via text message! Legitimate companies will NEVER ask for:\n• Passwords or PINs\n• Social Security numbers\n• Bank account details\n• Credit card numbers\n\nThis is a phishing attempt. Delete the message immediately."
        ]
    },
    
    # What to do
    'what_to_do': {
        'keywords': ['what should i do', 'what to do', 'received spam', 'got spam', 'help'],
        'responses': [
            "If you receive a spam message:\n1. DON'T click any links\n2. DON'T reply\n3. DON'T share personal info\n4. DELETE the message\n5. BLOCK the sender\n6. REPORT to your carrier (forward to 7726/SPAM)\n7. Use our SMS Guard tool to analyze suspicious messages!"
        ]
    },
    
    # How the detector works
    'how_it_works': {
        'keywords': ['how does it work', 'how it works', 'how detector', 'how does this work'],
        'responses': [
            "Our SMS Guard uses machine learning trained on thousands of real spam and legitimate messages. It analyzes:\n• Word patterns\n• Suspicious phrases\n• Common spam tactics\n• Message structure\n\nJust paste any message into the detector, and it will tell you if it's likely spam with a confidence score!"
        ]
    },
    
    # Safety tips
    'safety': {
        'keywords': ['stay safe', 'protect', 'security', 'safe', 'tips'],
        'responses': [
            "🛡️ SMS Safety Tips:\n• Never share passwords via text\n• Don't click unknown links\n• Verify sender identity\n• Use two-factor authentication\n• Keep your phone updated\n• Trust your instincts - if it feels wrong, it probably is\n• Use SMS Guard to check suspicious messages!"
        ]
    },
    
    # Thanks
    'thanks': {
        'keywords': ['thank', 'thanks', 'appreciate'],
        'responses': [
            "You're welcome! Stay safe out there! 🛡️",
            "Happy to help! Remember, when in doubt, use SMS Guard to check any suspicious message!",
            "Glad I could help! Feel free to ask if you have more questions about spam detection."
        ]
    },
    
    # Default/fallback
    'default': {
        'keywords': [],
        'responses': [
            "I can help you with:\n• Identifying spam messages\n• Understanding spam tactics\n• Staying safe from scams\n• Using the SMS Guard detector\n\nTry asking: 'How do I identify spam?' or 'What should I do if I receive spam?'"
        ]
    }
}

def token_required(f):
    """Decorator to require valid JWT token, or return a helpful fallback if invalid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                token = None
        
        if not token:
            # Fallback: helpful response for missing token
            if request.path.endswith('/chat'):
                return jsonify({
                    'success': True,
                    'data': {
                        'response': (
                            "You are not logged in, but I can still help! "
                            "Here are some tips for handling suspicious messages:\n\n"
                            "• Never click links from unknown senders\n"
                            "• Don't share personal info via text\n"
                            "• Block and delete suspicious messages\n"
                            "• Report spam to your carrier (7726)\n\n"
                            "If you want a more personalized analysis, please log in."
                        ),
                        'user': 'guest'
                    }
                }), 200
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                # Fallback: helpful response for invalid user
                if request.path.endswith('/chat'):
                    return jsonify({
                        'success': True,
                        'data': {
                            'response': (
                                "I couldn't verify your account, but here are some general tips:\n\n"
                                "• Never click links from unknown senders\n"
                                "• Don't share personal info via text\n"
                                "• Block and delete suspicious messages\n"
                                "• Report spam to your carrier (7726)\n\n"
                                "For a full experience, please log in."
                            ),
                            'user': 'guest'
                        }
                    }), 200
                return jsonify({'success': False, 'error': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            if request.path.endswith('/chat'):
                return jsonify({
                    'success': True,
                    'data': {
                        'response': (
                            "Your session has expired, but I can still help! "
                            "Here are some tips for handling suspicious messages:\n\n"
                            "• Never click links from unknown senders\n"
                            "• Don't share personal info via text\n"
                            "• Block and delete suspicious messages\n"
                            "• Report spam to your carrier (7726)\n\n"
                            "Please log in again for personalized analysis."
                        ),
                        'user': 'guest'
                    }
                }), 200
            return jsonify({'success': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            if request.path.endswith('/chat'):
                return jsonify({
                    'success': True,
                    'data': {
                        'response': (
                            "Your login token is invalid, but I can still help! "
                            "Here are some tips for handling suspicious messages:\n\n"
                            "• Never click links from unknown senders\n"
                            "• Don't share personal info via text\n"
                            "• Block and delete suspicious messages\n"
                            "• Report spam to your carrier (7726)\n\n"
                            "Please log in again for personalized analysis."
                        ),
                        'user': 'guest'
                    }
                }), 200
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def get_chatbot_response(message):
    """Get response based on keywords in message"""
    import random
    
    message_lower = message.lower().strip()
    
    # Check each category for keyword matches
    for category, data in CHATBOT_RESPONSES.items():
        if category == 'default':
            continue
            
        for keyword in data['keywords']:
            if keyword in message_lower:
                # Return a random response from this category
                return random.choice(data['responses'])
    
    # No match found, return default
    return random.choice(CHATBOT_RESPONSES['default']['responses'])

import requests

def gemini_chatbot_response(user_message, context_message, context_prediction):
    """
    Gemini-powered AI chatbot logic with rules:
    - Always reference the last prediction and message
    - Be unbiased, provide safety tips, and follow guidance rules
    """
    # Gemini API key (for demo, hardcoded; in production, use env variable)
    GEMINI_API_KEY = "AIzaSyD9N-O5Xu64sK7uA7K70f8ZMxvP-iBDtmU"
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    # Compose prompt with rules
    prompt = (
        "You are an SMS spam detection assistant. "
        "Always start by referencing the user's last analyzed message and the model's prediction. "
        "Be unbiased: if the model is uncertain or the message is ambiguous, ask clarifying questions. "
        "Always provide safety tips and guidance, and never encourage risky behavior. "
        "If the user asks about spam, scams, or safety, give clear, actionable advice. "
        "If the user asks something unrelated, politely redirect to SMS safety. "
        "Here is the last analyzed message:\n"
        f"\"{context_message or ''}\"\n"
        f"Prediction: {context_prediction.get('prediction', 'N/A').upper() if context_prediction else 'N/A'} "
        f"(Confidence: {context_prediction.get('confidence', 0)*100:.1f}%)\n\n"
        f"User: {user_message}\n"
        "Your response:"
    )

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    params = {"key": GEMINI_API_KEY}

    try:
        resp = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        # Extract the generated text
        answer = (
            result.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )
        if not answer:
            answer = "Sorry, I couldn't generate a response at this time. Please try again."
        return answer
    except Exception as e:
        print(f"Gemini API error: {e}")
        return (
            "Sorry, I couldn't reach the AI assistant right now. "
            "Please try again later or ask about SMS safety and spam detection."
        )

def hybrid_chatbot_response(user_message, context_message, context_prediction):
    # Use Gemini if API key is present, else fallback to rules
    return gemini_chatbot_response(user_message, context_message, context_prediction)

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Gemini chatbot endpoint (no JWT required for Gemini-only mode)
    Expected: POST /api/chatbot/chat
    Body: { "message": "string", "contextMessage": "string", "contextPrediction": { ... } }
    Returns: { "success": boolean, "data": { "response": string } }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        message = data.get('message', '').strip()
        context_message = data.get('contextMessage', '').strip()
        context_prediction = data.get('contextPrediction', None)
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Always use Gemini for the response
        response = hybrid_chatbot_response(message, context_message, context_prediction)
        
        return jsonify({
            'success': True,
            'data': {
                'response': response,
                'user': 'guest'
            }
        }), 200
        
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your message'
        }), 500

@chatbot_bp.route('/suggestions', methods=['GET'])
@token_required
def get_suggestions(current_user):
    """
    Get suggested questions
    Returns: { "success": boolean, "data": { "suggestions": [string] } }
    """
    suggestions = [
        "How do I identify spam messages?",
        "What should I do if I receive spam?",
        "How does the spam detector work?",
        "What are common spam tactics?",
        "How can I stay safe from scams?"
    ]
    
    return jsonify({
        'success': True,
        'data': {
            'suggestions': suggestions
        }
    }), 200
