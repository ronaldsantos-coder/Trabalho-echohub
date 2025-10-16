from flask import request, jsonify
import logging
from functions.verify_user import verify_user_credentials


def login():
    try:
        data = request.get_json()
        logging.debug(f"Login attempt with data: {data}")
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return jsonify({"detail": "Please provide username and password"}), 400
        if verify_user_credentials(username, password):
            logging.debug(f"Login successful for user: {username}")
            return jsonify({
                "message": "Login successful",
                "username": username,
                "success": True
            }), 200
        else:
            logging.debug(f"Login failed for user: {username}")
            return jsonify({
                "detail": "Invalid username or password",
                "success": False
            }), 401
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500
