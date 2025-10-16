import requests
import logging
from typing import Dict, Any, Optional
from config_n8n import N8N_ENDPOINTS, REQUEST_TIMEOUT, MAX_RETRIES

class N8NClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Faz uma requisição para o n8n com retry automático"""
        url = N8N_ENDPOINTS.get(endpoint)
        if not url:
            raise ValueError(f"Endpoint '{endpoint}' não encontrado")
        
        for attempt in range(MAX_RETRIES):
            try:
                logging.info(f"🌐 n8n Request: {method} {url}")
                if data:
                    logging.info(f"📤 Data: {data}")
                
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                elif method.upper() == 'POST':
                    response = self.session.post(url, json=data, timeout=REQUEST_TIMEOUT)
                elif method.upper() == 'PUT':
                    response = self.session.put(url, json=data, timeout=REQUEST_TIMEOUT)
                elif method.upper() == 'DELETE':
                    response = self.session.delete(url, json=data, timeout=REQUEST_TIMEOUT)
                else:
                    raise ValueError(f"Método HTTP '{method}' não suportado")
                
                logging.info(f"📥 n8n Response: {response.status_code}")
                response.raise_for_status()
                result = response.json()
                logging.info(f"✅ n8n Success: {result}")
                return result
                
            except requests.exceptions.RequestException as e:
                logging.warning(f"❌ Tentativa {attempt + 1} falhou: {e}")
                if attempt == MAX_RETRIES - 1:
                    logging.error(f"💥 Todas as tentativas falharam para {url}")
                    raise
                continue
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Autentica usuário via n8n"""
        data = {
            "email": username,  # n8n espera email em vez de username
            "password": password
        }
        return self._make_request('POST', 'login', data)
    
    def create_user(self, username: str, password: str, email: str = None) -> Dict[str, Any]:
        """Cria novo usuário via n8n"""
        data = {
            "email": email or username,  # n8n espera email
            "password": password
        }
        return self._make_request('POST', 'create_user', data)
    
    def create_post(self, name: str, title: str, description: str) -> Dict[str, Any]:
        """Cria novo post via n8n"""
        data = {
            "name": name,
            "title": title,
            "description": description
        }
        return self._make_request('POST', 'create_post', data)
    
    def update_post(self, post_id: int, name: str, title: str, description: str) -> Dict[str, Any]:
        """Atualiza post via n8n"""
        data = {
            "id": post_id,
            "name": name,
            "title": title,
            "description": description
        }
        return self._make_request('PUT', 'update_post', data)
    
    def delete_post(self, post_id: int) -> Dict[str, Any]:
        """Deleta post via n8n"""
        data = {
            "id": post_id
        }
        return self._make_request('DELETE', 'delete_post', data)
    
    def get_posts(self) -> Dict[str, Any]:
        """Busca todos os posts via n8n"""
        return self._make_request('GET', 'posts')

# Instância global do cliente
n8n_client = N8NClient()
