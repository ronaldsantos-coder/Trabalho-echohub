from flask import request, jsonify
import logging
from functions.verify_user import verify_user_credentials
from auth_supabase import authenticate_user_supabase

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

        # Tentar autenticação com Supabase primeiro
        logging.info(f"Tentando autenticação Supabase para: {username}")
        supabase_result = authenticate_user_supabase(username, password)
        logging.info(f"Resultado Supabase: {supabase_result}")
        
        if supabase_result["success"]:
            logging.debug(f"Supabase login successful for user: {username}")
            return jsonify({
                "message": "Login successful",
                "username": username,
                "user": supabase_result["user"],
                "token": supabase_result.get("token"),
                "success": True
            }), 200
        
        # Fallback para autenticação local se Supabase falhar
        elif verify_user_credentials(username, password):
            logging.debug(f"Local login successful for user: {username}")
            return jsonify({
                "message": "Login successful", 
                "username": username,
                "success": True
            }), 200
        else:
            logging.debug(f"Login failed for user: {username}")
            return jsonify({
                "detail": supabase_result.get("error", "Invalid username or password"), 
                "success": False
            }), 401
            
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}", 
            "success": False
        }), 500