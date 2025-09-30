# 🤖 SMS Guard - Simple Chatbot

## Overview

A **simple, keyword-based chatbot** that helps users understand spam messages and stay safe. No complex AI models or machine learning - just reliable keyword matching!

## ✨ Features

- **Fast & Reliable**: Instant responses using keyword matching
- **Educational**: Teaches users about spam detection
- **Safety Tips**: Provides actionable advice
- **User-Friendly**: Clean, modern chat interface
- **Contextual**: Recognizes spam-related keywords in user messages

## 🎯 What It Does

The chatbot helps users with:

1. **Identifying Spam**
   - Recognizes urgent language (ACT NOW, LIMITED TIME)
   - Detects free offers and prize scams
   - Identifies phishing attempts

2. **Safety Guidance**
   - What to do if you receive spam
   - How to protect personal information
   - Best practices for SMS security

3. **System Information**
   - How the spam detector works
   - Understanding confidence scores
   - Using the SMS Guard tool

## 🔧 How It Works

### Backend (`backend/routes/chatbot.py`)

- **Keyword Matching**: Scans user messages for specific keywords
- **Category-Based Responses**: Organized responses by topic
- **Multiple Responses**: Random selection for variety
- **JWT Authentication**: Secure, user-specific sessions

### Frontend (`src/pages/Chat.tsx`)

- **Real-Time Chat**: Instant message display
- **Suggested Questions**: Quick-start prompts
- **Clean UI**: Modern, gradient design
- **Message History**: Scrollable conversation view

## 📝 Example Interactions

### User: "Hello!"
**Bot:** "Hi there! I'm here to help you with spam detection. Ask me anything about identifying spam messages!"

### User: "How do I identify spam?"
**Bot:** "Here are key signs of spam:
• Urgent language (ACT NOW, LIMITED TIME)
• Requests for personal info (passwords, bank details)
• Too good to be true offers (FREE MONEY, WIN PRIZES)
• Unknown senders
• Suspicious links
• Poor grammar or spelling
• Threats or pressure tactics"

### User: "I got a message saying I won a prize"
**Bot:** "⚠️ SPAM ALERT: Messages offering free prizes, money, or claiming you've won something are usually scams. If you didn't enter a contest, you didn't win. These messages try to steal your personal information or money."

### User: "Someone is asking for my password"
**Bot:** "⚠️ SPAM ALERT: NEVER share personal information via text message! Legitimate companies will NEVER ask for:
• Passwords or PINs
• Social Security numbers
• Bank account details
• Credit card numbers

This is a phishing attempt. Delete the message immediately."

## 🚀 Getting Started

### 1. Start the System

```powershell
.\start_and_test.ps1
```

This will:
- Start the backend (Flask)
- Start the frontend (React)
- Test the chatbot
- Show you how to use it

### 2. Access the Chatbot

1. Open: http://localhost:5174
2. Login: demo@example.com / demo123
3. Click: **"AI Chat"** in the navigation
4. Start chatting!

### 3. Try These Questions

- "How do I identify spam?"
- "What should I do if I receive spam?"
- "How does the spam detector work?"
- "I got a message about winning money"
- "Someone wants my password"

## 🔑 Keyword Categories

The chatbot recognizes these keyword categories:

1. **Greetings**: hello, hi, hey
2. **Spam Identification**: how to identify, how to detect, recognize spam
3. **Urgent Language**: urgent, act now, limited time, expires
4. **Free Offers**: free, win, prize, winner, congratulations
5. **Money/Financial**: money, cash, bank, account, credit card
6. **Links**: click here, link, visit, website
7. **Personal Info**: password, pin, social security, verify
8. **What To Do**: what should i do, received spam, help
9. **How It Works**: how does it work, how detector
10. **Safety**: stay safe, protect, security, tips
11. **Thanks**: thank, thanks, appreciate

## 📁 File Structure

```
backend/
  routes/
    chatbot.py          # Chatbot API endpoint

src/
  pages/
    Chat.tsx            # Chat interface
  services/
    chatbotService.ts   # API communication

test_chatbot.py         # Test script
start_and_test.ps1      # Startup script
```

## 🔒 Security

- **JWT Authentication**: All requests require valid token
- **User-Specific**: Each user has their own chat session
- **No Data Storage**: Messages are not saved (privacy-first)
- **Rate Limiting**: Built into Flask backend

## 🎨 UI Features

- **Gradient Design**: Modern blue-to-purple gradient
- **Message Bubbles**: User (right) vs Bot (left)
- **Timestamps**: Each message shows time
- **Suggestions**: Quick-start questions
- **Loading States**: Spinner while bot responds
- **Responsive**: Works on all screen sizes

## 🧪 Testing

### Manual Test
```bash
python test_chatbot.py
```

### What It Tests
- User login/registration
- Chatbot responses to various messages
- Suggestion endpoint
- Token authentication

## 💡 Why Keyword-Based?

1. **Reliability**: No model loading, no dependencies
2. **Speed**: Instant responses
3. **Predictability**: Consistent behavior
4. **Maintainability**: Easy to add new keywords
5. **No Training**: Works immediately
6. **Low Resource**: Minimal CPU/memory usage

## 🔄 Adding New Responses

Edit `backend/routes/chatbot.py`:

```python
CHATBOT_RESPONSES = {
    'your_category': {
        'keywords': ['keyword1', 'keyword2', 'phrase'],
        'responses': [
            "Response 1",
            "Response 2"
        ]
    }
}
```

## 🐛 Troubleshooting

### Chatbot not responding?
- Check backend is running: http://localhost:5000/api/health
- Check browser console for errors
- Verify you're logged in

### "Token is missing" error?
- Log out and log back in
- Clear browser localStorage
- Check token in browser DevTools

### Backend error?
- Check `backend/app.py` has chatbot blueprint registered
- Verify `routes/chatbot.py` exists
- Check Python console for errors

## 📊 API Endpoints

### POST `/api/chatbot/chat`
Send a message to the chatbot

**Request:**
```json
{
  "message": "How do I identify spam?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "Here are key signs of spam...",
    "user": "demo"
  }
}
```

### GET `/api/chatbot/suggestions`
Get suggested questions

**Response:**
```json
{
  "success": true,
  "data": {
    "suggestions": [
      "How do I identify spam messages?",
      "What should I do if I receive spam?",
      ...
    ]
  }
}
```

## 🎉 Success!

You now have a working, simple chatbot that:
- ✅ Responds instantly
- ✅ Provides helpful information
- ✅ Educates users about spam
- ✅ Requires no complex setup
- ✅ Works reliably every time

Enjoy your SMS Guard chatbot! 🛡️

