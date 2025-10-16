import logging
from n8n_client import n8n_client


def create_post_db(name: str, title: str, description: str) -> bool:
    try:
        # Criar post via n8n
        response = n8n_client.create_post(name, title, description)
        
        if response and response.get('success', False):
            logging.info(f"Post created in n8n: {title}")
            return True
        else:
            logging.warning(f"Failed to create post in n8n: {title}")
            return False
            
    except Exception as e:
        logging.error(f"n8n create failed: {e}")
        return False
