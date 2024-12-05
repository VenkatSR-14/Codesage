# app.py
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    # Example response
    users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Doe"}]
    app.logger.info("Fetched user list")
    return jsonify(users), 200

# Global Error Handler
@app.errorhandler(Exception)
def handle_exception(e):
    # If the exception is an HTTPException, use its details
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({"error": e.description}).data
        response.content_type = "application/json"
        return response
    # Otherwise, it's an internal server error
    app.logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
