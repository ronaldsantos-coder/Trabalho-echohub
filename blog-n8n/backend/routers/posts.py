from flask import request, jsonify
import logging
from functions.consult_post import consult_post


def posts():
    try:
        logging.debug("Fetching posts from n8n")
        posts_data = consult_post()
        if posts_data is not None:
            return jsonify({
                "message": "Posts retrieved successfully",
                "posts": posts_data,
                "count": len(posts_data),
                "success": True
            }), 200
        return jsonify({
            "detail": "Error retrieving posts",
            "success": False
        }), 500
    except Exception as e:
        logging.error(f"Error retrieving posts: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500
