#!/bin/bash

echo "🚀 Iniciando Blog CMS com n8n Backend"
echo "======================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Por favor, instale Python3."
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Por favor, instale Node.js."
    exit 1
fi

echo "📦 Instalando dependências do backend..."
cd backend
pip install -r requirements.txt

echo "📦 Instalando dependências do frontend..."
cd ../frontend
npm install

echo "🔧 Construindo frontend..."
npm run build

echo "✅ Configuração concluída!"
echo ""
echo "Para iniciar o projeto:"
echo "1. Backend: cd backend && python main.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "🌐 URLs:"
echo "- Frontend: http://localhost:3001"
echo "- Backend: http://localhost:3002"
echo "- Health Check: http://localhost:3002/health"
