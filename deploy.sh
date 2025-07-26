#!/bin/bash

echo "🚀 Iniciando deploy para Railway..."

# Commit das mudanças
echo "📝 Fazendo commit das mudanças..."
git add .
git commit -m "feat: integração frontend + backend para Railway"

# Push para o repositório
echo "📤 Enviando para GitHub..."
git push origin main

echo "✅ Deploy enviado!"
echo "🌐 Aguarde 3-5 minutos e acesse: https://terra-plana-production.up.railway.app"
echo ""
echo "🧪 Para testar:"
echo "curl https://terra-plana-production.up.railway.app/health"
echo ""
echo "📱 Interface web disponível em:"
echo "https://terra-plana-production.up.railway.app" 