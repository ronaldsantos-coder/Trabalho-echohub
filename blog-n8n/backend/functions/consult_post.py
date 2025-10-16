import logging
from n8n_client import n8n_client


def consult_post():
    try:
        # Buscar posts via n8n
        response = n8n_client.get_posts()
        
        if response and 'posts' in response:
            posts = response['posts']
            logging.info(f"Posts retrieved from n8n: {len(posts)} posts")
            return posts
        else:
            logging.info("No posts found in n8n response")
            return []
            
    except Exception as e:
        logging.error(f"n8n posts retrieval failed: {e}")
        return []
