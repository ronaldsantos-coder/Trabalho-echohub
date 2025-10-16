from flask import request, jsonify
import logging
import os
from functions.storage import upload_profile_photo
from config_supabase import get_supabase_client


def upload_profile_photo_route():
    try:
        if not request.content_type or not request.content_type.startswith('multipart/form-data'):
            return jsonify({"detail": "Content-Type must be multipart/form-data"}), 400

        file = request.files.get('photo')
        email = request.form.get('email')

        if not file or not file.filename:
            return jsonify({"detail": "Photo file is required"}), 400

        if not email:
            return jsonify({"detail": "Email is required"}), 400

        # Upload photo
        uploads_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads'))
        photo_url = upload_profile_photo(file, email, uploads_root)
        
        if not photo_url:
            return jsonify({"detail": "Failed to upload profile photo"}), 500

        # Convert to absolute URL
        if photo_url.startswith('/'):
            base = request.host_url.rstrip('/')
            photo_url = f"{base}{photo_url}"

        # Update user profile in Supabase
        supabase = get_supabase_client()
        response = supabase.table('users').update({
            'profile_photo_url': photo_url
        }).eq('email', email).execute()

        if not response.data:
            logging.error("Failed to update user profile photo in database")
            return jsonify({"detail": "Failed to update profile"}), 500

        return jsonify({
            "message": "Profile photo uploaded successfully",
            "profile_photo_url": photo_url,
            "success": True
        }), 200

    except Exception as e:
        logging.error(f"Error uploading profile photo: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500


def get_profile_photo(email: str):
    try:
        supabase = get_supabase_client()
        response = supabase.table('users').select('profile_photo_url').eq('email', email).single().execute()
        
        if response.data:
            return jsonify({
                "profile_photo_url": response.data.get('profile_photo_url'),
                "success": True
            }), 200
        else:
            return jsonify({
                "profile_photo_url": None,
                "success": True
            }), 200

    except Exception as e:
        logging.error(f"Error getting profile photo: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500
