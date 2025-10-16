# Configuração do Supabase

## 1. Obter as chaves do Supabase

1. Acesse seu projeto no Supabase: https://supabase.com/dashboard
2. Vá para Settings > API
3. Copie a URL e a chave anon (public)

## 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na pasta `backend/` com:

```env
SUPABASE_URL=https://txfevmlhzqchiylfewrz.supabase.co
SUPABASE_ANON_KEY=sua-chave-anon-aqui
```

## 3. Configurar autenticação no Supabase

1. No dashboard do Supabase, vá para Authentication > Settings
2. Configure as políticas de autenticação conforme necessário
3. Habilite o provider de email/password se necessário

## 4. Testar a conexão

O backend agora tentará:
1. Autenticar com Supabase primeiro
2. Se falhar, usar autenticação local como fallback

## 5. Endpoints disponíveis

- `POST /api/login` - Login com Supabase
- `POST /api/register` - Criar usuário no Supabase
- `GET /health` - Verificar status da API

## 6. Estrutura de resposta do login

```json
{
  "message": "Login successful",
  "username": "usuario",
  "user": {
    "id": "uuid-do-usuario",
    "email": "email@exemplo.com",
    "username": "usuario"
  },
  "token": "jwt-token-do-supabase",
  "success": true
}
```

