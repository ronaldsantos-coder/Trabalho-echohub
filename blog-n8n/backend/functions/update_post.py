import logging
from n8n_client import n8n_client


def update_post_db(post_id: int, name: str, title: str, description: str) -> bool:
    try:
        # Atualizar post via n8n
        response = n8n_client.update_post(post_id, name, title, description)
        
        if response and response.get('success', False):
            logging.info(f"Post updated in n8n: ID {post_id}")
            return True
        else:
            logging.warning(f"Post not found in n8n: ID {post_id}")
            return False
            
    except Exception as e:
        logging.error(f"n8n update failed: {e}")
        return False
