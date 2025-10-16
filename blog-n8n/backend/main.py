from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
from functions.verify_user import verify_user_credentials
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

# Carregar variáveis de ambiente
load_dotenv()

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

# Rotas da API
app.add_url_rule("/api/create_blog", "create_blog", create_blog, methods=["POST"])
app.add_url_rule("/api/posts", "posts", posts, methods=["GET"])
app.add_url_rule("/api/update_post", "update_post", update_post, methods=["PUT"])
app.add_url_rule("/api/delete_post", "delete_post", delete_post, methods=["DELETE"])
app.add_url_rule("/health", "health", health, methods=["GET"])
app.add_url_rule("/api/login", "login", login, methods=["POST"])
app.add_url_rule("/api/register", "register", register, methods=["POST"])

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
        
    app.run(debug=True, port=3003, host="0.0.0.0")
