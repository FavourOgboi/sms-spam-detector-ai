"""
AI Chatbot Service for SMS Spam Detector

This service provides conversational AI that can:
1. Chat naturally with users using their names
2. Understand context of SMS messages and situations
3. Integrate with spam detection model and LIME explanations
4. Provide personalized advice and recommendations
5. Use simple, easy-to-understand language
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import re

class ChatbotService:
    """
    AI Chatbot service that provides conversational assistance
    for SMS spam detection and user guidance
    """
    
    def __init__(self, spam_detector=None):
        """Initialize the chatbot service"""
        self.spam_detector = spam_detector
        self.conversation_memory = {}  # Store conversations by user_id
        self.max_memory_length = 10  # Keep last 10 messages for context
        
        # Common spam scenarios and advice
        self.spam_scenarios = {
            'account_expiring': {
                'keywords': ['account', 'expiring', 'expire', 'suspended', 'verify', 'confirm'],
                'advice': "This looks like a phishing scam! Real companies don't ask you to verify accounts through text messages. Never click suspicious links or give personal info."
            },
            'money_offers': {
                'keywords': ['free', 'money', 'cash', 'prize', 'winner', 'won', 'claim'],
                'advice': "This is likely a money scam! If it sounds too good to be true, it probably is. Legitimate prizes don't require you to pay fees or give personal information."
            },
            'urgent_banking': {
                'keywords': ['bank', 'urgent', 'compromised', 'fraud', 'security', 'alert'],
                'advice': "This could be a banking scam! Real banks will never ask for passwords or account details via text. Call your bank directly using the number on your card."
            },
            'tech_support': {
                'keywords': ['virus', 'infected', 'computer', 'microsoft', 'apple', 'support'],
                'advice': "This is probably a tech support scam! Real tech companies don't contact you about viruses through text messages. Don't click any links or call the numbers."
            },
            'delivery_issues': {
                'keywords': ['package', 'delivery', 'shipping', 'fedex', 'ups', 'dhl', 'postal'],
                'advice': "This might be a delivery scam! Check if you're actually expecting a package. Real delivery companies use their official apps and websites for tracking."
            }
        }
    
    def get_user_conversation(self, user_id: str) -> List[Dict]:
        """Get conversation history for a user"""
        return self.conversation_memory.get(user_id, [])
    
    def add_to_conversation(self, user_id: str, message: str, sender: str):
        """Add a message to conversation history"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            'message': message,
            'sender': sender,  # 'user' or 'bot'
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent messages for memory management
        if len(self.conversation_memory[user_id]) > self.max_memory_length:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-self.max_memory_length:]
    
    def analyze_message_context(self, message: str) -> Dict[str, Any]:
        """Analyze the context and scenario of a message"""
        message_lower = message.lower()
        
        # Check for spam scenarios
        detected_scenario = None
        scenario_confidence = 0
        
        for scenario_name, scenario_data in self.spam_scenarios.items():
            matches = sum(1 for keyword in scenario_data['keywords'] if keyword in message_lower)
            confidence = matches / len(scenario_data['keywords'])
            
            if confidence > scenario_confidence:
                scenario_confidence = confidence
                detected_scenario = scenario_name
        
        # Extract potential suspicious elements
        suspicious_elements = []
        
        # Check for URLs
        if re.search(r'http[s]?://|www\.|\.com|\.org|\.net|link|click', message_lower):
            suspicious_elements.append('contains_links')
        
        # Check for phone numbers
        if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\d{10}\b', message):
            suspicious_elements.append('contains_phone')
        
        # Check for urgency words
        urgency_words = ['urgent', 'immediate', 'now', 'asap', 'quickly', 'hurry']
        if any(word in message_lower for word in urgency_words):
            suspicious_elements.append('urgent_language')
        
        # Check for money/financial terms
        money_words = ['$', 'money', 'cash', 'pay', 'fee', 'cost', 'price', 'free']
        if any(word in message_lower for word in money_words):
            suspicious_elements.append('financial_content')
        
        return {
            'detected_scenario': detected_scenario,
            'scenario_confidence': scenario_confidence,
            'suspicious_elements': suspicious_elements,
            'message_length': len(message),
            'has_numbers': bool(re.search(r'\d', message)),
            'has_caps': bool(re.search(r'[A-Z]', message))
        }
    
    def generate_personalized_response(self, user_name: str, message: str, 
                                     spam_prediction: Dict = None, 
                                     explanation: Dict = None,
                                     conversation_history: List = None) -> str:
        """
        Generate a personalized response based on user context and message analysis
        """
        # Analyze message context
        context = self.analyze_message_context(message)
        
        # Start response with user's name
        response_parts = [f"Hi {user_name}! "]
        
        # If we have spam prediction, use it
        if spam_prediction:
            prediction = spam_prediction.get('prediction', '').lower()
            confidence = spam_prediction.get('confidence', 0) * 100
            
            if prediction == 'spam':
                response_parts.append(f"I analyzed your message and our AI thinks this is likely SPAM with {confidence:.0f}% confidence. ")
                
                # Add scenario-specific advice
                if context['detected_scenario']:
                    scenario_advice = self.spam_scenarios[context['detected_scenario']]['advice']
                    response_parts.append(f"{scenario_advice} ")
                
                # Add general safety advice
                response_parts.append("Here's what I recommend: ")
                safety_tips = []
                
                if 'contains_links' in context['suspicious_elements']:
                    safety_tips.append("Don't click any links in the message")
                
                if 'contains_phone' in context['suspicious_elements']:
                    safety_tips.append("Don't call any phone numbers mentioned")
                
                if 'financial_content' in context['suspicious_elements']:
                    safety_tips.append("Never give out your financial information")
                
                if 'urgent_language' in context['suspicious_elements']:
                    safety_tips.append("Take time to think - scammers use urgency to pressure you")
                
                if safety_tips:
                    response_parts.append("• " + " • ".join(safety_tips) + ". ")
                
                response_parts.append("When in doubt, delete the message and block the sender. Stay safe!")
                
            else:  # HAM/Legitimate
                response_parts.append(f"Good news! Our AI thinks this message looks legitimate with {confidence:.0f}% confidence. ")
                
                # Still provide context-aware advice
                if context['suspicious_elements']:
                    response_parts.append("However, I noticed a few things to keep in mind: ")
                    
                    if 'contains_links' in context['suspicious_elements']:
                        response_parts.append("Even though this seems legitimate, always be careful with links. Make sure they go to official websites. ")
                    
                    if 'financial_content' in context['suspicious_elements']:
                        response_parts.append("Since this involves money or payments, double-check it's from a trusted source. ")
                
                response_parts.append("Trust your instincts - if something feels off, it's okay to be cautious!")
        
        else:
            # No prediction available, provide general guidance
            response_parts.append("I'd be happy to help you understand this message better! ")
            
            if context['suspicious_elements']:
                response_parts.append("I notice this message has some elements that could be concerning: ")
                
                element_descriptions = {
                    'contains_links': "it contains links",
                    'contains_phone': "it has phone numbers",
                    'urgent_language': "it uses urgent language",
                    'financial_content': "it mentions money or payments"
                }
                
                descriptions = [element_descriptions.get(elem, elem) for elem in context['suspicious_elements']]
                response_parts.append(", ".join(descriptions) + ". ")
                
                response_parts.append("Would you like me to analyze this message with our spam detection system?")
        
        # Add explanation insights if available
        if explanation and explanation.get('success'):
            exp_data = explanation.get('explanation', {})
            features = exp_data.get('features', [])
            
            if features:
                response_parts.append(f"\n\nOur AI also found some key words that influenced the decision: ")
                
                spam_words = [f['feature'] for f in features if f['direction'] == 'spam'][:3]
                ham_words = [f['feature'] for f in features if f['direction'] == 'ham'][:3]
                
                if spam_words:
                    response_parts.append(f"Words that suggest spam: {', '.join(spam_words)}. ")
                
                if ham_words:
                    response_parts.append(f"Words that suggest it's legitimate: {', '.join(ham_words)}. ")
        
        # Add conversational elements based on history
        if conversation_history and len(conversation_history) > 1:
            response_parts.append(f"\n\nIs there anything else about this message or other messages you'd like to discuss, {user_name}?")
        else:
            response_parts.append(f"\n\nFeel free to ask me about any other suspicious messages, {user_name}!")
        
        return "".join(response_parts)
    
    def chat_with_user(self, user_id: str, user_name: str, message: str, 
                      analyze_with_model: bool = True) -> Dict[str, Any]:
        """
        Main chat function that handles user conversations
        """
        try:
            # Add user message to conversation history
            self.add_to_conversation(user_id, message, 'user')
            
            # Get conversation history
            conversation_history = self.get_user_conversation(user_id)
            
            # Initialize response data
            response_data = {
                'success': True,
                'user_message': message,
                'timestamp': datetime.now().isoformat(),
                'conversation_id': user_id
            }
            
            # Analyze with spam detection model if requested and available
            spam_prediction = None
            explanation = None
            
            if analyze_with_model and self.spam_detector:
                try:
                    spam_prediction = self.spam_detector.predict(message)
                    explanation = self.spam_detector.explain_prediction(message, num_features=5)
                except Exception as e:
                    print(f"Error analyzing message: {e}")
            
            # Generate personalized response
            bot_response = self.generate_personalized_response(
                user_name=user_name,
                message=message,
                spam_prediction=spam_prediction,
                explanation=explanation,
                conversation_history=conversation_history
            )
            
            # Add bot response to conversation history
            self.add_to_conversation(user_id, bot_response, 'bot')
            
            # Prepare response data
            response_data.update({
                'bot_response': bot_response,
                'spam_analysis': spam_prediction,
                'explanation': explanation,
                'conversation_length': len(conversation_history) + 1,
                'processing_time_ms': 50  # Placeholder for actual timing
            })
            
            return response_data
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Chat error: {str(e)}",
                'user_message': message,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_conversation_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of the user's conversation"""
        conversation = self.get_user_conversation(user_id)
        
        if not conversation:
            return {'has_conversation': False}
        
        user_messages = [msg for msg in conversation if msg['sender'] == 'user']
        bot_messages = [msg for msg in conversation if msg['sender'] == 'bot']
        
        return {
            'has_conversation': True,
            'total_messages': len(conversation),
            'user_messages': len(user_messages),
            'bot_messages': len(bot_messages),
            'conversation_start': conversation[0]['timestamp'] if conversation else None,
            'last_message': conversation[-1]['timestamp'] if conversation else None
        }

# Global chatbot instance
chatbot_service = None

def get_chatbot_service(spam_detector=None):
    """Get or create the global chatbot service instance"""
    global chatbot_service
    if chatbot_service is None:
        chatbot_service = ChatbotService(spam_detector)
    return chatbot_service
