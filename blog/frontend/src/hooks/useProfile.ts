import { useState } from 'react';
import { useToast } from '@/components/ui/use-toast';

export const useProfile = () => {
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const uploadProfilePhoto = async (file: File, email: string) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('photo', file);
      formData.append('email', email);

      const response = await fetch(`http://localhost:3002/api/profile/photo`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        toast({
          title: 'Foto de perfil atualizada!',
          description: 'Sua foto de perfil foi salva com sucesso.',
        });
        return data.profile_photo_url;
      } else {
        toast({
          variant: 'destructive',
          title: 'Erro ao enviar foto',
          description: data.detail || 'Falha ao enviar foto de perfil',
        });
        return null;
      }
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro de conexão',
        description: 'Não foi possível conectar ao servidor',
      });
      return null;
    } finally {
      setLoading(false);
    }
  };

  const getProfilePhoto = async (email: string) => {
    try {
      const response = await fetch(`http://localhost:3002/api/profile/photo/${email}`);
      const data = await response.json();
      
      if (response.ok) {
        return data.profile_photo_url;
      } else {
        return null;
      }
    } catch (error) {
      return null;
    }
  };

  return { uploadProfilePhoto, getProfilePhoto, loading };
};
