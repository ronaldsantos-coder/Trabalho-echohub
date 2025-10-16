from flask import request, jsonify
import logging
from auth_supabase import create_user_supabase

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

        # Criar usuário no Supabase
        result = create_user_supabase(username, password, email)
        
        if result["success"]:
            logging.debug(f"User created successfully: {username}")
            return jsonify({
                "message": "User created successfully",
                "user": result["user"],
                "success": True
            }), 201
        else:
            logging.debug(f"User creation failed: {username}")
            return jsonify({
                "detail": result.get("error", "Failed to create user"),
                "success": False
            }), 400
            
    except Exception as e:
        logging.error(f"Register error: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500
