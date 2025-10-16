import logging
from config_supabase import get_supabase_client


def list_comments(post_id: int):
    try:
        supabase = get_supabase_client()
        response = (
            supabase
            .table("comments")
            .select("id, post_id, author, content, created_at, attachment_url")
            .eq("post_id", post_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []
    except Exception as e:
        logging.error(f"Error listing comments (supabase): {e}")
        return []


