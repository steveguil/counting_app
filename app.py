"""
Simple Flask app for "The Counting Game".

Run with:
    python app.py

This app keeps a persistent counter in a SQLite database and exposes endpoints:
- GET /      -> serve the single page UI with current count
- POST /count -> increment the counter and return JSON with the new value
- POST /reset -> reset the counter to zero

This file is heavily commented for beginners.
"""
from flask import Flask, render_template, jsonify
from threading import Lock
import sqlite3
import os

# Create the Flask application object
app = Flask(__name__)

# Database configuration
DB_PATH = 'counting_game.db'

# A lock to avoid race conditions when accessing the database from multiple threads.
db_lock = Lock()


def init_db():
    """Initialize the SQLite database and create the counter table if it doesn't exist.

    The table has a single row with id=1 that stores the current counter value.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the counter table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counter (
            id INTEGER PRIMARY KEY,
            value INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Insert the initial counter row if it doesn't exist
    cursor.execute('SELECT COUNT(*) FROM counter WHERE id = 1')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO counter (id, value) VALUES (1, 0)')

    conn.commit()
    conn.close()


def get_counter():
    """Read the current counter value from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM counter WHERE id = 1')
    value = cursor.fetchone()[0]
    conn.close()
    return value


def increment_counter():
    """Increment the counter in the database and return the new value."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE counter SET value = value + 1 WHERE id = 1')
        cursor.execute('SELECT value FROM counter WHERE id = 1')
        new_value = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_value


def reset_counter():
    """Reset the counter to zero in the database and return the new value."""
    with db_lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE counter SET value = 0 WHERE id = 1')
        cursor.execute('SELECT value FROM counter WHERE id = 1')
        new_value = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return new_value


# Initialize the database when the app starts
init_db()


@app.route('/')
def index():
    """Serve the single-page UI.

    We pass the current counter value to the template so the page can show it
    when first loaded.
    """
    current_count = get_counter()
    return render_template('index.html', count=current_count)


@app.route('/count', methods=['POST'])
def increment_count():
    """Increment the database counter and return the new value as JSON.

    This endpoint is called from client-side JavaScript. We use a lock in
    increment_counter() to prevent race conditions if multiple requests
    arrive at the same time.
    """
    new_value = increment_counter()

    # Return the new value in JSON format. The client will use this to update
    # the displayed counter without a full page reload.
    return jsonify({'count': new_value})


@app.route('/reset', methods=['POST'])
def reset_count():
    """Reset the database counter to zero and return the new value.

    This endpoint is called when the user dismisses the '13' message in the
    UI. We use the lock in reset_counter() to prevent races with concurrent requests.
    """
    new_value = reset_counter()
    return jsonify({'count': new_value})


@app.route('/hello')
def hello_world():
    """A simple Hello World endpoint."""
    return "Hello World!"


if __name__ == '__main__':
    # Start the Flask development server on localhost:5001 so the user can
    # open http://localhost:5001 in their browser.
    # debug=False by default; during development you can set debug=True.
    app.run(host='127.0.0.1', port=5001)
