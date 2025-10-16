from flask import request, jsonify
import logging
from functions.update_post import update_post_db


def update_post():
    try:
        data = request.get_json()
        logging.debug(f"Update post attempt with data: {data}")
        
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
            
        post_id = data.get("id")
        name = data.get("name")
        title = data.get("title")
        description = data.get("description")

        if not all([post_id, name, title, description]):
            return jsonify({"detail": "Please provide id, name, title, and description"}), 400

        success = update_post_db(post_id, name, title, description)
        if success:
            logging.debug(f"Post updated successfully: {title}")
            return jsonify({
                "message": "Post updated successfully",
                "post_id": post_id,
                "title": title,
                "description": description,
                "success": True
            }), 200
        return jsonify({
            "detail": f"Error updating post: ID {post_id}", 
            "success": False
        }), 500
    except Exception as e:
        logging.error(f"Error updating post: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}", 
            "success": False
        }), 500
