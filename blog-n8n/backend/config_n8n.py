import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do n8n - URLs atualizadas
N8N_ENDPOINTS = {
    'login': "https://primary-production-e91c.up.railway.app/webhook/login",
    'create_user': "https://primary-production-e91c.up.railway.app/webhook-test/create",
    'create_post': "https://primary-production-e91c.up.railway.app/webhook/create_post",
    'update_post': "https://primary-production-e91c.up.railway.app/webhook/update_post",
    'delete_post': "https://primary-production-e91c.up.railway.app/webhook/delete_post",
    'posts': "https://primary-production-e91c.up.railway.app/webhook/list_posts"
}

# Configurações de timeout e retry
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
