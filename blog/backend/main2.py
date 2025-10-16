from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql.cursors
from dotenv import load_dotenv
import logging
import os
from typing import Optional

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT')) if os.getenv('DB_PORT') else 3306
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database connection function
def create_connection_db():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None

# Database operations
def consult_post():
    connection = create_connection_db()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM posts"
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error retrieving posts: {e}")
        return None
    finally:
        connection.close()

def create_post_db(name: str, title: str, description: str) -> bool:
    connection = create_connection_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO posts (name, title, description) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, title, description))
            return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error inserting post: {e}")
        return False
    finally:
        connection.close()

def post_delete(title: str) -> bool:
    connection = create_connection_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM posts WHERE title = %s"
            cursor.execute(sql, (title,))
            return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error deleting post: {e}")
        return False
    finally:
        connection.close()

def update_post_db(old_title: str, name: str, title: str, description: str) -> bool:
    connection = create_connection_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE posts SET name = %s, title = %s, description = %s WHERE title = %s"
            cursor.execute(sql, (name, title, description, old_title))
            return cursor.rowcount > 0
    except Exception as e:
        logging.error(f"Error updating post: {e}")
        return False
    finally:
        connection.close()

def verify_user_credentials(username: str, password: str) -> bool:
    connection = create_connection_db()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username, password FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            return result is not None
    except Exception as e:
        logging.error(f"Error verifying credentials: {e}")
        return False
    finally:
        connection.close()

# API endpoints
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

def delete_post():
    try:
        data = request.get_json()
        logging.debug(f"Delete post attempt with data: {data}")
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
        title = data.get("title")
        if not title:
            return jsonify({"detail": "Please provide a title"}), 400
        success = post_delete(title)
        if success:
            logging.debug(f"Post deleted successfully: {title}")
            return jsonify({
                "message": "Post deleted successfully",
                "post": title,
                "success": True
            }), 200
        return jsonify({
            "detail": f"Error deleting post: {title}",
            "success": False
        }), 500
    except Exception as e:
        logging.error(f"Error deleting post: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500

def health():
    try:
        connection = create_connection_db()
        if connection:
            connection.close()
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "message": "API and database are running",
                "success": True
            })
        else:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "message": "API is running but database connection failed",
                "success": False
            }), 503
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "message": "Health check failed",
            "success": False
        }), 503

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
        if verify_user_credentials(username, password):
            logging.debug(f"Login successful for user: {username}")
            return jsonify({
                "message": "Login successful",
                "username": username,
                "success": True
            }), 200
        else:
            logging.debug(f"Login failed for user: {username}")
            return jsonify({
                "detail": "Invalid username or password",
                "success": False
            }), 401
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500

def posts():
    try:
        logging.debug("Fetching posts")
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

def update_post():
    try:
        data = request.get_json()
        logging.debug(f"Update post attempt with data: {data}")
        if not data:
            return jsonify({"detail": "No JSON data provided"}), 400
        old_title = data.get("old_title")
        name = data.get("name")
        title = data.get("title")
        description = data.get("description")
        if not all([old_title, name, title, description]):
            return jsonify({"detail": "Please provide old_title, name, title, and description"}), 400
        success = update_post_db(old_title, name, title, description)
        if success:
            logging.debug(f"Post updated successfully: {title}")
            return jsonify({
                "message": "Post updated successfully",
                "post": title,
                "description": description,
                "success": True
            }), 200
        return jsonify({
            "detail": f"Error updating post: {title}",
            "success": False
        }), 500
    except Exception as e:
        logging.error(f"Error updating post: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500

# Flask app setup
app = Flask(__name__, static_folder="../frontend/dist", static_url_path="")
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True
    }
})

# Route definitions
app.add_url_rule("/api/create_blog", "create_blog", create_blog, methods=["POST"])
app.add_url_rule("/api/posts", "posts", posts, methods=["GET"])
app.add_url_rule("/api/update_post", "update_post", update_post, methods=["PUT"])
app.add_url_rule("/api/delete_post", "delete_post", delete_post, methods=["DELETE"])
app.add_url_rule("/health", "health", health, methods=["GET"])
app.add_url_rule("/api/login", "login", login, methods=["POST"])

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

# Main execution
if __name__ == "__main__":
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/dist")
    if not os.path.exists(frontend_path):
        print(f"⚠️  Frontend build not found at: {frontend_path}")
        print("Please build the frontend first with: npm run build")
        print("Starting API only mode...")
    necessary_dirs = ["static/css", "static/js", "static/images"]
    for dir_path in necessary_dirs:
        os.makedirs(dir_path, exist_ok=True)
    app.run(debug=True, port=3000, host="0.0.0.0")