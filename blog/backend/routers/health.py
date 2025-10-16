from flask import jsonify
import logging
from database.database import create_connection_db

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