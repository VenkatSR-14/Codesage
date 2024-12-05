# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Home route returning a simple JSON response."""
    return jsonify({"message": "Welcome to the production-ready Flask app!"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check route to verify the service status."""
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    # Run the app in production-ready mode
    app.run(host='0.0.0.0', port=5000)
