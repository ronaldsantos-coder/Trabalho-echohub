import logging
from typing import Optional
from auth_supabase import authenticate_user_supabase


def verify_user_credentials(username: str, password: str) -> bool:
    try:
        # Usar apenas Supabase para autenticação
        result = authenticate_user_supabase(username, password)
        return result is not None
    except Exception as e:
        logging.error(f"Error verifying credentials with Supabase: {e}")
        return False

