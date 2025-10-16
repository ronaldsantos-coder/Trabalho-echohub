from config_supabase import get_supabase_client
import logging
import requests

def authenticate_user_supabase(username: str, password: str):
    """
    Autentica usuário usando Supabase com URL específica de login
    """
    try:
        
        login_url = "https://txfevmlhzqchiylfewrz.supabase.co/auth/v1/token?grant_type=password"
        
        
        headers = {
            'Content-Type': 'application/json',
            'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4ZmV2bWxoenFjaGl5bGZld3J6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxNTM5NDksImV4cCI6MjA3NDcyOTk0OX0.Fjz4_RkeZMWXTdeAsHVmEHY6schtADJ1ijlu5FYxJLI'
        }
        
        
        auth_data = {
            "email": username,
            "password": password
        }
        
       
        logging.info(f"Fazendo requisição para Supabase: {login_url}")
        logging.info(f"Dados enviados: {auth_data}")
        response = requests.post(login_url, json=auth_data, headers=headers)
        
        logging.info(f"Resposta do Supabase: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            auth_response = response.json()
            logging.info(f"Supabase login successful for user: {username}")
            return {
                "success": True,
                "user": {
                    "id": auth_response.get("user", {}).get("id"),
                    "email": auth_response.get("user", {}).get("email"),
                    "username": username
                },
                "token": auth_response.get("access_token"),
                "refresh_token": auth_response.get("refresh_token")
            }
        else:
            logging.warning(f"Supabase login failed for user: {username}")
            return {
                "success": False,
                "error": f"Authentication failed: {response.text}"
            }
            
    except Exception as e:
        logging.error(f"Supabase authentication error: {e}")
        return {
            "success": False,
            "error": f"Authentication failed: {str(e)}"
        }

def create_user_supabase(username: str, password: str, email: str = None):
    """
    Cria um novo usuário no Supabase
    """
    try:
        supabase = get_supabase_client()
        
        
        user_email = email or f"{username}@example.com"
        
        
        response = supabase.auth.sign_up({
            "email": user_email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })
        
        if response.user:
            logging.info(f"User created successfully: {username}")
            return {
                "success": True,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "username": username
                }
            }
        else:
            logging.warning(f"User creation failed for: {username}")
            return {
                "success": False,
                "error": "Failed to create user"
            }
            
    except Exception as e:
        logging.error(f"Supabase user creation error: {e}")
        return {
            "success": False,
            "error": f"User creation failed: {str(e)}"
        }

def verify_token_supabase(token: str):
    """
    Verifica se o token do Supabase é válido
    """
    try:
        supabase = get_supabase_client()
        
        # Verificar token
        response = supabase.auth.get_user(token)
        
        if response.user:
            return {
                "success": True,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email
                }
            }
        else:
            return {
                "success": False,
                "error": "Invalid token"
            }
            
    except Exception as e:
        logging.error(f"Token verification error: {e}")
        return {
            "success": False,
            "error": f"Token verification failed: {str(e)}"
        }
