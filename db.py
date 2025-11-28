import sqlite3
from datetime import datetime
import os

DB_PATH = 'chatlogs.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_session_id ON chat_logs(session_id)
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def log_interaction(session_id, user_message, bot_response):
    """Log a chat interaction to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO chat_logs (session_id, user_message, bot_response)
        VALUES (?, ?, ?)
    ''', (session_id, user_message, bot_response))
    
    conn.commit()
    conn.close()

def get_chat_history(session_id, limit=10):
    """Get chat history for a session"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_message, bot_response, timestamp
        FROM chat_logs
        WHERE session_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (session_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    history = []
    for row in reversed(rows):
        history.append({
            'user': row['user_message'],
            'bot': row['bot_response'],
            'timestamp': row['timestamp']
        })
    
    return history

def get_all_logs():
    """Get all chat logs (for admin purposes)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, session_id, user_message, bot_response, timestamp
        FROM chat_logs
        ORDER BY timestamp DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def clear_session_history(session_id):
    """Clear chat history for a specific session"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM chat_logs WHERE session_id = ?
    ''', (session_id,))
    
    conn.commit()
    conn.close()
