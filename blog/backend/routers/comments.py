from flask import request, jsonify
import logging
import os
from functions.add_comment import add_comment
from functions.list_comments import list_comments
from functions.delete_comment import delete_comment as delete_comment_fn
from functions.storage import upload_comment_attachment


def post_comment(post_id: int):
    try:
        attachment_url = None

        if request.content_type and request.content_type.startswith('multipart/form-data'):
            content = request.form.get('content')
            author = request.form.get('author')
            file = request.files.get('file')
            if file and file.filename:
                # Save locally under backend/static/uploads and return public path /uploads/... 
                attachment_url = upload_comment_attachment(file, post_id)
                # If we got a relative path, turn into absolute URL
                if attachment_url and attachment_url.startswith('/'):
                    base = request.host_url.rstrip('/')
                    attachment_url = f"{base}{attachment_url}"
                if not attachment_url:
                    logging.error("Upload de anexo falhou: URL pública não gerada")
                    return jsonify({
                        "detail": "Falha ao enviar o anexo. Verifique o bucket 'comments' e as permissões de leitura.",
                        "success": False
                    }), 500
        else:
            data = request.get_json() or {}
            content = data.get("content")
            author = data.get("author")
        
        # If no author provided, use default
        if not author:
            author = "Usuário"

        if not content or not str(content).strip():
            return jsonify({"detail": "Comment content is required"}), 400

        saved = add_comment(post_id=post_id, content=str(content).strip(), author=author, attachment_url=attachment_url)
        if saved is None:
            return jsonify({"detail": "Failed to save comment"}), 500

        # saved already includes attachment_url when present

        return jsonify({
            "message": "Comment created",
            "comment": saved,
            "success": True
        }), 201
    except Exception as e:
        logging.error(f"Error creating comment: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500


def get_comments(post_id: int):
    try:
        comments = list_comments(post_id)
        return jsonify({
            "message": "Comments retrieved",
            "comments": comments,
            "count": len(comments),
            "success": True
        }), 200
    except Exception as e:
        logging.error(f"Error retrieving comments: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500


def delete_comment(post_id: int, comment_id: int):
    try:
        uploads_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads'))
        ok = delete_comment_fn(post_id, comment_id, uploads_root)
        if ok:
            return jsonify({"message": "Comment deleted", "success": True}), 200
        return jsonify({"detail": "Failed to delete comment", "success": False}), 500
    except Exception as e:
        logging.error(f"Error deleting comment: {e}")
        return jsonify({
            "detail": f"Server error: {str(e)}",
            "success": False
        }), 500


