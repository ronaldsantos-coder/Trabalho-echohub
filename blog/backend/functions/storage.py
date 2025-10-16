import logging
import uuid
import os
from werkzeug.utils import secure_filename
from typing import Optional


def ensure_uploads_dir(base_path: str) -> None:
    try:
        os.makedirs(base_path, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create uploads directory: {e}")


def upload_comment_attachment(file_storage, post_id: int, uploads_dir: str = None, public_base: str = None) -> Optional[str]:
    try:
        # Defaults
        base_dir = uploads_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads'))
        public_prefix = public_base or '/uploads'

        ensure_uploads_dir(base_dir)

        # per-post folder
        safe_name = secure_filename(file_storage.filename or f"file-{uuid.uuid4()}")
        rel_path = os.path.join('posts', str(post_id))
        abs_post_dir = os.path.join(base_dir, rel_path)
        os.makedirs(abs_post_dir, exist_ok=True)

        final_filename = f"{uuid.uuid4()}-{safe_name}"
        abs_path = os.path.join(abs_post_dir, final_filename)
        file_storage.save(abs_path)

        # Build public URL path (served by Flask static rule)
        public_url = f"{public_prefix}/posts/{post_id}/{final_filename}"
        return public_url
    except Exception as e:
        logging.error(f"Error saving local attachment: {e}")
        return None


def upload_profile_photo(file_storage, user_id: str, uploads_dir: str = None, public_base: str = None) -> Optional[str]:
    try:
        # Defaults
        base_dir = uploads_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads'))
        public_prefix = public_base or '/uploads'

        ensure_uploads_dir(base_dir)

        # profile photos folder
        safe_name = secure_filename(file_storage.filename or f"profile-{uuid.uuid4()}")
        rel_path = os.path.join('profiles', user_id)
        abs_profile_dir = os.path.join(base_dir, rel_path)
        os.makedirs(abs_profile_dir, exist_ok=True)

        # Get file extension
        _, ext = os.path.splitext(safe_name)
        if not ext:
            ext = '.jpg'  # default extension
        
        final_filename = f"profile{ext}"
        abs_path = os.path.join(abs_profile_dir, final_filename)
        file_storage.save(abs_path)

        # Build public URL path (served by Flask static rule)
        public_url = f"{public_prefix}/profiles/{user_id}/{final_filename}"
        return public_url
    except Exception as e:
        logging.error(f"Error saving profile photo: {e}")
        return None


