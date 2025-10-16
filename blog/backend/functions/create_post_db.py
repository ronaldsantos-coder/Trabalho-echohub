import logging
from config_supabase import get_supabase_client


def create_post_db(name: str, title: str, description: str) -> bool:
    try:
        # Usar apenas Supabase
        supabase = get_supabase_client()
        
        # Criar post na tabela 'posts' do Supabase
        response = supabase.table('posts').insert({
            'name': name,
            'title': title,
            'description': description
        }).execute()
        
        if response.data:
            logging.info(f"Post created in Supabase: {title}")
            return True
        else:
            logging.warning(f"Failed to create post in Supabase: {title}")
            return False
            
    except Exception as e:
        logging.error(f"Supabase create failed: {e}")
        return False