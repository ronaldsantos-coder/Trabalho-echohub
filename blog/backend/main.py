from curses import echo
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from typing import Optional
from dotenv import load_dotenv
# Removed MySQL database import - using Supabase only 
from functions.verify_user import verify_user_credentials
from auth_supabase import authenticate_user_supabase
from functions.create_post_db import create_post_db
from functions.consult_post import consult_post
from functions.update_post import update_post_db
from functions.post_delete import post_delete
from routers.create_blog import create_blog
from routers.posts import posts
from routers.update_post import update_post
from routers.delete_post import delete_post
from routers.health import health
from routers.login import login
from routers.register import register
from routers.comments import post_comment, get_comments, delete_comment
from routers.profile import upload_profile_photo_route, get_profile_photo
from flask import send_from_directory
import os


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True
    }
})

logging.basicConfig(level=logging.DEBUG)


app.add_url_rule("/api/create_blog", "create_blog", create_blog, methods=["POST"])
app.add_url_rule("/api/posts", "posts", posts, methods=["GET"])
app.add_url_rule("/api/update_post", "update_post", update_post, methods=["PUT"])
app.add_url_rule("/api/delete_post", "delete_post", delete_post, methods=["DELETE"])
app.add_url_rule("/health", "health", health, methods=["GET"])
app.add_url_rule("/api/login", "login", login, methods=["POST"])
app.add_url_rule("/api/register", "register", register, methods=["POST"])
app.add_url_rule("/api/posts/<int:post_id>/comments", "post_comment", post_comment, methods=["POST"])
app.add_url_rule("/api/posts/<int:post_id>/comments", "get_comments", get_comments, methods=["GET"])
app.add_url_rule("/api/posts/<int:post_id>/comments/<int:comment_id>", "delete_comment", delete_comment, methods=["DELETE"])
app.add_url_rule("/api/profile/photo", "upload_profile_photo", upload_profile_photo_route, methods=["POST"])
app.add_url_rule("/api/profile/photo/<email>", "get_profile_photo", get_profile_photo, methods=["GET"])

# Local uploads serving
UPLOADS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'uploads'))
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")




if __name__ == "__main__":
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
    
    if not os.path.exists(frontend_path):
        print(f"⚠️  Frontend build not found at: {frontend_path}")
        print("Please build the frontend first with: npm run build")
        print("Starting API only mode...")
        
    necessary_dirs = ["static/css", "static/js", "static/images"]
    for dir_path in necessary_dirs:
        os.makedirs(dir_path, exist_ok=True)
        
    app.run(debug=True, port=3002, host="0.0.0.0")