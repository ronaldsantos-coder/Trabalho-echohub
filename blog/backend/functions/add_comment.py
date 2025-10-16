import logging
from typing import Optional
from config_supabase import get_supabase_client


def add_comment(post_id: int, content: str, author: Optional[str] = None, attachment_url: Optional[str] = None) -> Optional[dict]:
    try:
        supabase = get_supabase_client()
        payload = {"post_id": post_id, "content": content}
        if author is not None:
            payload["author"] = author
        if attachment_url is not None:
            payload["attachment_url"] = attachment_url
        response = supabase.table("comments").insert(payload).execute()

        data = getattr(response, "data", None) or []
        if data:
            # Return first inserted row
            row = data[0]
            # Ensure only expected fields are returned if DB returns extra
            return {
                "id": row.get("id"),
                "post_id": row.get("post_id"),
                "author": row.get("author"),
                "content": row.get("content"),
                "created_at": row.get("created_at"),
                "attachment_url": row.get("attachment_url"),
            }
        else:
            logging.error(f"Supabase insert comment failed: {getattr(response, 'error', None)}")
            return None
    except Exception as e:
        logging.error(f"Error adding comment (supabase): {e}")
        return None


