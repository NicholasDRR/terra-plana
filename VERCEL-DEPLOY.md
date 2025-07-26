# 🚀 Deploy do Frontend no Vercel

## 📋 Pré-requisitos

1. **Conta no GitHub** com seu projeto
2. **Conta no Vercel** ([vercel.com](https://vercel.com))
3. **Railway API** já configurada e funcionando

---

## 🔧 Configuração do Frontend

O frontend já está configurado para se conectar à sua API no Railway, usando o arquivo `vercel.json` que adicionamos ao projeto.

---

## 🚀 Deploy Passo a Passo no Vercel

### Passo 1: Criar Repositório Separado (Opcional)

```bash
# Se quiser, crie um repo apenas para o frontend
mkdir terra-plana-frontend
cp -r frontend/* terra-plana-frontend/
cd terra-plana-frontend
git init
git add .
git commit -m "Criação do frontend"
# Criar repo no GitHub e push
```

### Passo 2: Deploy no Vercel

1. **Acesse** [vercel.com](https://vercel.com)
2. **Faça login** com GitHub
3. **"New Project"** → Selecione seu repositório
   - Se estiver usando o repo completo, configure "Root Directory" para `frontend`
   - Se criou um repo separado, deixe como padrão
4. **Em "Build & Development Settings"**:
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`
5. **Em "Environment Variables"**, adicione:
   ```
   REACT_APP_API_URL=https://terra-plana-production.up.railway.app
   ```
6. **Clique em "Deploy"**

---

## ✅ Verificação do Deploy

Após o deploy, o Vercel fornecerá uma URL:
- Exemplo: `https://terra-plana-frontend.vercel.app`

Acesse essa URL para confirmar que:
1. O frontend está carregando
2. Está se conectando com a API no Railway
3. O chat está funcionando corretamente

---

## 🔄 Atualização do Frontend

Sempre que fizer alterações no frontend:

```bash
git add .
git commit -m "feat: suas alterações"
git push origin main
```

O Vercel fará deploy automaticamente após cada push!

---

## 📝 Configuração Existente

Já incluímos no repositório:

1. **`vercel.json`** - Configuração do Vercel com:
   - Regras de rewrite para SPA routing
   - Configuração da API URL
   - Headers para CORS

2. **API URL** configurada no frontend (em App.js):
   ```js
   const API_BASE_URL = process.env.NODE_ENV === 'production' 
     ? process.env.REACT_APP_API_URL || ''
     : '';
   ```

---

## 🔍 Troubleshooting

### CORS Errors
- Verifique se a URL do frontend está incluída em `ALLOWED_ORIGINS` no backend
- Verifique os headers do Vercel

### API não responde
- Confirme se a API URL está correta
- Verifique se a API está funcionando no Railway

### Problemas de Routing
- Confirme que o `vercel.json` está configurado corretamente 