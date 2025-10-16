import os
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

# Criar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_supabase_client():
    """Retorna o cliente Supabase configurado"""
    return supabase
