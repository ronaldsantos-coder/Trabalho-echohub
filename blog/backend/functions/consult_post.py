import logging
from config_supabase import get_supabase_client


def consult_post():
    try:
        # Usar apenas Supabase
        supabase = get_supabase_client()
        
        # Buscar posts na tabela 'posts' do Supabase
        response = supabase.table('posts').select('*').execute()
        
        if response.data:
            logging.info(f"Posts retrieved from Supabase: {len(response.data)} posts")
            return response.data
        else:
            logging.info("No posts found in Supabase")
            return []
            
    except Exception as e:
        logging.error(f"Supabase posts retrieval failed: {e}")
        return []