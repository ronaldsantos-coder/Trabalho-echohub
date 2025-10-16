import logging
import os
from urllib.parse import urlparse
from typing import Optional
from config_supabase import get_supabase_client


def _local_path_from_url(attachment_url: Optional[str], uploads_root: str) -> Optional[str]:
    if not attachment_url:
        return None
    try:
        parsed = urlparse(attachment_url)
        path = parsed.path or attachment_url  # supports absolute or relative
        if not path.startswith('/uploads/'):
            return None
        rel = path[len('/uploads/'):]
        return os.path.join(uploads_root, rel)
    except Exception:
        return None


def delete_comment(post_id: int, comment_id: int, uploads_root: str) -> bool:
    try:
        supabase = get_supabase_client()

        # Fetch to get attachment_url
        sel = (
            supabase
            .table('comments')
            .select('id, post_id, attachment_url')
            .eq('id', comment_id)
            .eq('post_id', post_id)
            .limit(1)
            .execute()
        )
        row = (sel.data or [None])[0]

        # Delete row
        res = (
            supabase
            .table('comments')
            .delete()
            .eq('id', comment_id)
            .eq('post_id', post_id)
            .execute()
        )

        ok = bool(res.data is not None)

        # Remove local file if exists
        if row and row.get('attachment_url'):
            local_path = _local_path_from_url(row.get('attachment_url'), uploads_root)
            if local_path and os.path.exists(local_path):
                try:
                    os.remove(local_path)
                except Exception as e:
                    logging.warning(f"Failed to remove local attachment: {e}")

        return ok
    except Exception as e:
        logging.error(f"Error deleting comment: {e}")
        return False


