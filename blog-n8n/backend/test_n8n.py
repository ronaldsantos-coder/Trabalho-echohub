#!/usr/bin/env python3
"""
Script de teste para verificar a conectividade com n8n
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from n8n_client import n8n_client
from config_n8n import N8N_ENDPOINTS
import json

def test_n8n_connection():
    """Testa a conexão com todos os endpoints do n8n"""
    
    print("🧪 Testando conexão com n8n...")
    print("=" * 60)
    
    # Mostrar todas as URLs configuradas
    print("📋 URLs configuradas:")
    for endpoint, url in N8N_ENDPOINTS.items():
        print(f"   {endpoint}: {url}")
    print()
    
    # Teste 1: Health check (posts)
    print("1. 📝 Testando endpoint de posts...")
    try:
        response = n8n_client.get_posts()
        print(f"   ✅ Posts: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Posts falhou: {e}")
    
    print()
    
    # Teste 2: Login (com credenciais de teste)
    print("2. 🔐 Testando endpoint de login...")
    try:
        response = n8n_client.login("test_user", "test_password")
        print(f"   ✅ Login: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Login falhou: {e}")
    
    print()
    
    # Teste 3: Criar usuário
    print("3. 👤 Testando endpoint de criar usuário...")
    try:
        response = n8n_client.create_user("test_user_new", "test_password", "test@example.com")
        print(f"   ✅ Criar usuário: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Criar usuário falhou: {e}")
    
    print()
    
    # Teste 4: Criar post
    print("4. ✍️ Testando endpoint de criar post...")
    try:
        response = n8n_client.create_post("Test Author", "Test Post", "This is a test post content")
        print(f"   ✅ Criar post: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Criar post falhou: {e}")
    
    print()
    
    # Teste 5: Atualizar post
    print("5. ✏️ Testando endpoint de atualizar post...")
    try:
        response = n8n_client.update_post(1, "Updated Author", "Updated Post", "Updated content")
        print(f"   ✅ Atualizar post: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Atualizar post falhou: {e}")
    
    print()
    
    # Teste 6: Deletar post
    print("6. 🗑️ Testando endpoint de deletar post...")
    try:
        response = n8n_client.delete_post(1)
        print(f"   ✅ Deletar post: {json.dumps(response, indent=2)}")
    except Exception as e:
        print(f"   ❌ Deletar post falhou: {e}")
    
    print()
    print("🏁 Teste concluído!")

if __name__ == "__main__":
    test_n8n_connection()
