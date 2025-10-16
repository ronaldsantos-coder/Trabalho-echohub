from flask import request, jsonify
import logging
from functions.create_post_db import create_post_db

def create_blog():
    try:
        data = request.get_json()
        logging.debug(f"Create blog attempt with data: {data}")
        
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
            
        name = data.get("name")
        title = data.get("title")
        description = data.get("description")

        if not all([name, title, description]):
            return jsonify({"detail": "Please provide name, title, and description"}), 400

        success = create_post_db(name, title, description)
        if success:
            logging.debug(f"Post created successfully: {title}")
            return jsonify({
                "message": "Post created successfully", 
                "post": title,
                "success": True
            }), 201
        return jsonify({
            "detail": f"Error creating post: {title}", 
            "success": False
        }), 500
        
    except Exception as e:
        logging.error(f"Error creating post: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}", 
            "success": False
        }), 500