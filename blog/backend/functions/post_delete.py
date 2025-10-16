import logging
from config_supabase import get_supabase_client


def post_delete(post_id: int) -> bool:
    try:
        # Usar apenas Supabase
        supabase = get_supabase_client()
        
        # Deletar post na tabela 'posts' do Supabase usando ID
        response = supabase.table('posts').delete().eq('id', post_id).execute()
        
        if response.data:
            logging.info(f"Post deleted from Supabase: ID {post_id}")
            return True
        else:
            logging.warning(f"Post not found in Supabase: ID {post_id}")
            return False
            
    except Exception as e:
        logging.error(f"Supabase delete failed: {e}")
        return False