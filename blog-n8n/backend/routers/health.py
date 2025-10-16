from flask import jsonify
import logging
from n8n_client import n8n_client


def health():
    try:
        # Testar conexão com n8n fazendo uma requisição simples
        response = n8n_client.get_posts()
        
        if response is not None:
            return jsonify({
                "status": "healthy",
                "n8n": "connected",
                "message": "API and n8n are running",
                "success": True
            })
        else:
            return jsonify({
                "status": "healthy",
                "n8n": "disconnected",
                "message": "API is running (n8n may be offline)",
                "success": True
            })
    except Exception as e:
        return jsonify({
            "status": "healthy",
            "n8n": "disconnected",
            "message": "API is running (n8n may be offline)",
            "error": str(e),
            "success": True
        })
