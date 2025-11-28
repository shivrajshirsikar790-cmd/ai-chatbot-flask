from flask import Flask, render_template, request, jsonify, session
import uuid
from model import get_bot_response
from db import init_db, log_interaction, get_chat_history

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Initialize database
init_db()

@app.route('/')
def home():
    # Create session ID for new users
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    session_id = session.get('session_id', str(uuid.uuid4()))
    
    # Get chat history for context
    history = get_chat_history(session_id, limit=5)
    
    # Get bot response
    bot_response = get_bot_response(user_message, history)
    
    # Log the interaction
    log_interaction(session_id, user_message, bot_response)
    
    return jsonify({'reply': bot_response})

@app.route('/history', methods=['GET'])
def history():
    session_id = session.get('session_id', '')
    if not session_id:
        return jsonify({'history': []})
    
    history = get_chat_history(session_id, limit=50)
    return jsonify({'history': history})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
