"""
Simple Flask app for "The Counting Game".

Run with:
    python app.py

This app keeps an in-memory counter (a Python variable) and exposes two endpoints:
- GET /      -> serve the single page UI with current count
- POST /count -> increment the counter and return JSON with the new value

This file is heavily commented for beginners.
"""
from flask import Flask, render_template, jsonify
from threading import Lock

# Create the Flask application object
app = Flask(__name__)

# A global in-memory counter. This satisfies requirement #4 (in-memory for now).
# In a production system you'd store this in a database.
counter = {
    "value": 0
}

# A lock to avoid race conditions if the dev server runs with threads.
counter_lock = Lock()


@app.route('/')
def index():
    """Serve the single-page UI.

    We pass the current counter value to the template so the page can show it
    when first loaded.
    """
    # Read the counter value (no lock needed for read in this simple app,
    # but we could use the lock for consistency)
    return render_template('index.html', count=counter['value'])


@app.route('/count', methods=['POST'])
def increment_count():
    """Increment the in-memory counter and return the new value as JSON.

    This endpoint is called from client-side JavaScript. We use a lock to
    prevent a race condition if multiple requests arrive at the same time.
    """
    with counter_lock:
        counter['value'] += 1
        new_value = counter['value']

    # Return the new value in JSON format. The client will use this to update
    # the displayed counter without a full page reload.
    return jsonify({'count': new_value})


@app.route('/reset', methods=['POST'])
def reset_count():
    """Reset the in-memory counter to zero and return the new value.

    This endpoint is called when the user dismisses the '13' message in the
    UI. We also use the lock here to prevent races with concurrent requests.
    """
    with counter_lock:
        counter['value'] = 0
        new_value = counter['value']
    return jsonify({'count': new_value})


@app.route('/hello')
def hello_world():
    """A simple Hello World endpoint."""
    return "Hello World!"


if __name__ == '__main__':
    # Start the Flask development server on localhost:5000 so the user can
    # open http://localhost:5000 in their browser.
    # debug=False by default; during development you can set debug=True.
    app.run(host='127.0.0.1', port=5000)
