import logging
from config_supabase import get_supabase_client


def update_post_db(post_id: int, name: str, title: str, description: str) -> bool:
    try:
        # Usar apenas Supabase
        supabase = get_supabase_client()
        
        # Atualizar post na tabela 'posts' do Supabase usando ID
        response = supabase.table('posts').update({
            'name': name,
            'title': title,
            'description': description
        }).eq('id', post_id).execute()
        
        if response.data:
            logging.info(f"Post updated in Supabase: ID {post_id}")
            return True
        else:
            logging.warning(f"Post not found in Supabase: ID {post_id}")
            return False
            
    except Exception as e:
        logging.error(f"Supabase update failed: {e}")
        return False