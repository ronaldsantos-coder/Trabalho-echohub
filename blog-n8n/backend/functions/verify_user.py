import logging
from n8n_client import n8n_client


def verify_user_credentials(username: str, password: str) -> bool:
    try:
        # Credenciais de teste temporárias
        if username == "admin" and password == "admin":
            logging.info(f"User authenticated with test credentials: {username}")
            return True
            
        # Verificar credenciais via n8n
        response = n8n_client.login(username, password)
        
        if response and response.get('success', False):
            logging.info(f"User authenticated via n8n: {username}")
            return True
        else:
            logging.warning(f"Authentication failed via n8n: {username}")
            return False
            
    except Exception as e:
        logging.error(f"n8n authentication failed: {e}")
        return False
