import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# FAQ Knowledge Base
FAQ_DATABASE = {
    'greeting': {
        'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
        'responses': [
            'Hello! How can I help you today?',
            'Hi there! What can I assist you with?',
            'Hey! Welcome to our support. How may I help you?'
        ]
    },
    'goodbye': {
        'patterns': ['bye', 'goodbye', 'see you', 'later', 'exit', 'quit'],
        'responses': [
            'Goodbye! Have a great day!',
            'See you later! Feel free to come back anytime.',
            'Bye! Thanks for chatting with us.'
        ]
    },
    'thanks': {
        'patterns': ['thank', 'thanks', 'appreciate', 'helpful'],
        'responses': [
            "You're welcome! Is there anything else I can help with?",
            'Happy to help! Let me know if you have more questions.',
            'Glad I could assist! Anything else you need?'
        ]
    },
    'hours': {
        'patterns': ['hours', 'open', 'close', 'timing', 'schedule', 'when'],
        'responses': [
            'Our support is available 24/7! You can reach us anytime.',
            'We are here round the clock to assist you.',
            'Our team is available 24 hours a day, 7 days a week.'
        ]
    },
    'contact': {
        'patterns': ['contact', 'email', 'phone', 'call', 'reach'],
        'responses': [
            'You can reach us at support@example.com or call 1-800-SUPPORT.',
            'Feel free to email us at support@example.com.',
            'Contact us via email: support@example.com or phone: 1-800-SUPPORT'
        ]
    },
    'pricing': {
        'patterns': ['price', 'cost', 'pricing', 'pay', 'fee', 'charge'],
        'responses': [
            'Our pricing varies based on the plan. Visit our pricing page for details.',
            'We offer flexible pricing plans. Would you like me to explain them?',
            'Pricing depends on your needs. Our basic plan starts at $9.99/month.'
        ]
    },
    'help': {
        'patterns': ['help', 'support', 'assist', 'problem', 'issue'],
        'responses': [
            'I am here to help! Please describe your issue.',
            'Sure, I can assist you. What seems to be the problem?',
            'Let me help you with that. Can you provide more details?'
        ]
    },
    'default': {
        'patterns': [],
        'responses': [
            "I'm not sure I understand. Could you please rephrase that?",
            'Interesting question! Let me connect you with a human agent for better assistance.',
            "I don't have information on that. Can I help you with something else?"
        ]
    }
}

def preprocess_text(text):
    """Preprocess the input text"""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if t not in stop_words]
    return tokens

def find_best_intent(user_message):
    """Find the best matching intent for the user message"""
    tokens = preprocess_text(user_message)
    
    best_intent = 'default'
    best_score = 0
    
    for intent, data in FAQ_DATABASE.items():
        if intent == 'default':
            continue
        
        score = 0
        for pattern in data['patterns']:
            pattern_tokens = preprocess_text(pattern)
            # Check for matching tokens
            for token in tokens:
                if token in pattern_tokens or any(token in p for p in data['patterns']):
                    score += 1
        
        if score > best_score:
            best_score = score
            best_intent = intent
    
    return best_intent if best_score > 0 else 'default'

def get_bot_response(user_message, history=None):
    """Generate a response based on user message and chat history"""
    
    # Find the best matching intent
    intent = find_best_intent(user_message)
    
    # Get a random response for the intent
    responses = FAQ_DATABASE[intent]['responses']
    response = random.choice(responses)
    
    # Add context awareness based on history
    if history and len(history) > 0:
        last_interaction = history[-1]
        # If user is following up, acknowledge it
        if any(word in user_message.lower() for word in ['more', 'detail', 'explain', 'elaborate']):
            response = "Building on our previous conversation: " + response
    
    return response
