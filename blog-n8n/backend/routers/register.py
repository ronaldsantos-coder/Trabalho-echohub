from flask import request, jsonify
import logging
from n8n_client import n8n_client


def register():
    try:
        data = request.get_json()
        logging.debug(f"Register attempt with data: {data}")
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        if not username or not password:
            return jsonify({"detail": "Please provide username and password"}), 400
        
        # Criar usuário via n8n
        response = n8n_client.create_user(username, password, email)
        
        if response and response.get('success', False):
            logging.debug(f"User created successfully: {username}")
            return jsonify({
                "message": "User created successfully",
                "username": username,
                "success": True
            }), 201
        else:
            logging.debug(f"User creation failed: {username}")
            return jsonify({
                "detail": "Failed to create user",
                "success": False
            }), 400
    except Exception as e:
        logging.error(f"Register error: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500
