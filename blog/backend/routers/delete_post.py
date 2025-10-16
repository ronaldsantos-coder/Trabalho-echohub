from flask import request, jsonify
import logging
from functions.post_delete import post_delete



def delete_post():
    try:
        data = request.get_json()
        logging.debug(f"Delete post attempt with data: {data}")
        
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
            
        post_id = data.get("id")

        if not post_id:
            return jsonify({"detail": "Please provide an id"}), 400

        success = post_delete(post_id)
        if success:
            logging.debug(f"Post deleted successfully: ID {post_id}")
            return jsonify({
                "message": "Post deleted successfully",
                "post_id": post_id,
                "success": True
            }), 200
        return jsonify({
            "detail": f"Error deleting post: ID {post_id}", 
            "success": False
        }), 500
    except Exception as e:
        logging.error(f"Error deleting post: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}", 
            "success": False
        }), 500