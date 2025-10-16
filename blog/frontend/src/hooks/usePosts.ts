import { useState, useEffect } from 'react';
import { useToast } from '@/hooks/use-toast';

export interface Post {
  id: number;
  name: string;
  title: string;
  description: string;
}

export const usePosts = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/posts`);
      const data = await response.json();
      
      if (response.ok) {
        setPosts(data.posts || []);
      } else {
        toast({
          variant: "destructive",
          title: "Error fetching posts",
          description: data.detail || 'Failed to load posts',
        });
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Connection error",
        description: 'Could not connect to server',
      });
    } finally {
      setLoading(false);
    }
  };

  const createPost = async (post: Omit<Post, 'id'>) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/create_blog`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: "Post created successfully!",
          description: `"${post.title}" has been published`,
        });
        await fetchPosts(); // Refresh the posts list
        return true;
      } else {
        toast({
          variant: "destructive",
          title: "Error creating post",
          description: data.detail || 'Failed to create post',
        });
        return false;
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Connection error",
        description: 'Could not connect to server',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const updatePost = async (postId: number, post: Omit<Post, 'id'>) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/update_post`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: postId,
          ...post,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: "Post updated successfully!",
          description: `Post ID ${postId} has been updated`,
        });
        await fetchPosts(); // Refresh the posts list
        return true;
      } else {
        toast({
          variant: "destructive",
          title: "Error updating post",
          description: data.detail || 'Failed to update post',
        });
        return false;
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Connection error",
        description: 'Could not connect to server',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const deletePost = async (postId: number) => {
    try {
      setLoading(true);
      const response = await fetch(`http://localhost:3002/api/delete_post`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: postId }),
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: "Post deleted successfully!",
          description: `Post ID ${postId} has been removed`,
        });
        await fetchPosts(); // Refresh the posts list
        return true;
      } else {
        toast({
          variant: "destructive",
          title: "Error deleting post",
          description: data.detail || 'Failed to delete post',
        });
        return false;
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Connection error",
        description: 'Could not connect to server',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  return {
    posts,
    loading,
    fetchPosts,
    createPost,
    updatePost,
    deletePost,
  };
};