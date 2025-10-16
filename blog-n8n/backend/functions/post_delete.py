import logging
from n8n_client import n8n_client


def post_delete(post_id: int) -> bool:
    try:
        # Deletar post via n8n
        response = n8n_client.delete_post(post_id)
        
        if response and response.get('success', False):
            logging.info(f"Post deleted from n8n: ID {post_id}")
            return True
        else:
            logging.warning(f"Post not found in n8n: ID {post_id}")
            return False
            
    except Exception as e:
        logging.error(f"n8n delete failed: {e}")
        return False
