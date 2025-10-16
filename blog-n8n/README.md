# Blog CMS com n8n Backend

Este projeto é uma versão do Blog CMS que usa n8n como backend através de webhooks.

## Estrutura do Projeto

```
blog-n8n/
├── frontend/          # React + TypeScript + Vite
├── backend/           # Flask + n8n webhooks
│   ├── functions/     # Funções de negócio
│   ├── routers/       # Rotas da API
│   ├── config_n8n.py  # Configuração do n8n
│   ├── n8n_client.py  # Cliente para n8n
│   └── main.py        # Aplicação principal
└── README.md
```

## Configuração do n8n

O backend usa os seguintes webhooks do n8n (URLs atualizadas):

- **Login**: `https://primary-production-e91c.up.railway.app/webhook/login`
- **Criar Usuário**: `https://primary-production-e91c.up.railway.app/webhook-test/create`
- **Criar Post**: `https://primary-production-e91c.up.railway.app/webhook/create_post`
- **Atualizar Post**: `https://primary-production-e91c.up.railway.app/webhook/update_post`
- **Deletar Post**: `https://primary-production-e91c.up.railway.app/webhook-test/create` ⚠️
- **Listar Posts**: `https://primary-production-e91c.up.railway.app/webhook-test/posts`

> ⚠️ **Nota**: O endpoint de deletar post usa `/create` conforme especificado

## Instalação e Execução

> ⚠️ **Importante**: O frontend se conecta diretamente às URLs do n8n, não precisa do backend local.

### Frontend (Conecta diretamente ao n8n)

```bash
cd frontend
npm install
npm run dev
```

### Backend (Opcional - para desenvolvimento)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

## Funcionalidades

- ✅ Autenticação de usuários via n8n
- ✅ Criação de usuários via n8n
- ✅ CRUD completo de posts via n8n
- ✅ Interface moderna com React + TypeScript
- ✅ Sistema de notificações
- ✅ Design responsivo

## Diferenças do Projeto Original

- **Backend**: Usa n8n webhooks em vez de Supabase/MySQL
- **Arquitetura**: Cliente n8n com retry automático
- **Configuração**: URLs do n8n centralizadas
- **Logs**: Logging detalhado das requisições n8n

## Configuração

Crie um arquivo `.env` no diretório `backend/` com:

```env
N8N_BASE_URL=https://primary-production-e91c.up.railway.app/webhook-test
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## API Endpoints

- `POST /api/login` - Autenticação
- `POST /api/register` - Criação de usuário
- `GET /api/posts` - Listar posts
- `POST /api/create_blog` - Criar post
- `PUT /api/update_post` - Atualizar post
- `DELETE /api/delete_post` - Deletar post
- `GET /health` - Health check
