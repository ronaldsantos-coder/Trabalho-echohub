import axios from 'axios';

const API_BASE = '/api';

const instance = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add JWT token to requests if available
instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  async login(username: string, password: string) {
    try {
      const response = await instance.post('/login', { username, password });
      return response.data;
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      throw error;
    }
  },

  async createPost(name: string, title: string, description: string) {
    try {
      const response = await instance.post('/posts', { name, title, description });
      return response.data;
    } catch (error) {
      console.error('Erro ao criar post:', error);
      throw error;
    }
  },

  async getPosts() {
    try {
      const response = await instance.get('/posts');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar posts:', error);
      throw error;
    }
  },

  async updatePost(postId: number, name: string, title: string, description: string) {
    try {
      const response = await instance.put(`/update_post`, { id: postId, name, title, description });
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar post:', error);
      throw error;
    }
  },

  async deletePost(postId: number) {
    try {
      const response = await instance.delete(`/delete_post`, { data: { id: postId } });
      return response.data;
    } catch (error) {
      console.error('Erro ao deletar post:', error);
      throw error;
    }
  }
};