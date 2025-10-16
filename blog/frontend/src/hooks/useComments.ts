import { useEffect, useState } from 'react';
import { useToast } from '@/components/ui/use-toast';

export interface CommentItem {
  id: number;
  post_id: number;
  author?: string | null;
  content: string;
  created_at: string;
  attachment_url?: string | null;
}

export const useComments = (postId: number) => {
  const [comments, setComments] = useState<CommentItem[]>([]);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const fetchComments = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/posts/${postId}/comments`);
      const data = await response.json();
      if (response.ok) {
        setComments(data.comments || []);
      } else {
        toast({
          variant: 'destructive',
          title: 'Erro ao buscar comentários',
          description: data.detail || 'Falha ao carregar comentários',
        });
      }
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro de conexão',
        description: 'Não foi possível conectar ao servidor',
      });
    } finally {
      setLoading(false);
    }
  };

  const addComment = async (content: string, author?: string, file?: File | null) => {
    try {
      setLoading(true);
      let response: Response;
      if (file) {
        const form = new FormData();
        form.append('content', content);
        if (author) form.append('author', author);
        form.append('file', file);
        response = await fetch(`http://localhost:3002/api/posts/${postId}/comments`, {
          method: 'POST',
          body: form,
        });
      } else {
        response = await fetch(`http://localhost:3002/api/posts/${postId}/comments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content, author: author || undefined }),
        });
      }
      const data = await response.json();
      if (response.ok) {
        await fetchComments();
        return true;
      } else {
        toast({
          variant: 'destructive',
          title: 'Erro ao enviar comentário',
          description: data.detail || 'Falha ao enviar comentário',
        });
        return false;
      }
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro de conexão',
        description: 'Não foi possível conectar ao servidor',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const deleteComment = async (commentId: number) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/posts/${postId}/comments/${commentId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (response.ok) {
        await fetchComments();
        return true;
      } else {
        toast({
          variant: 'destructive',
          title: 'Erro ao deletar comentário',
          description: data.detail || 'Falha ao deletar comentário',
        });
        return false;
      }
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro de conexão',
        description: 'Não foi possível conectar ao servidor',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [postId]);

  return { comments, loading, fetchComments, addComment, deleteComment };
};


