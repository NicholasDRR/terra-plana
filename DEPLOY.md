# 🚀 Deploy do Terra Plana Chat no Railway

## 📋 Pré-requisitos

1. **Conta no GitHub** com seu projeto
2. **Conta no Railway** ([railway.app](https://railway.app))
3. **Chaves de API necessárias:**
   - OpenAI API Key
   - ElevenLabs API Key (opcional, para áudio)
   - Supabase URL e Anon Key

---

## 🔧 Preparação do Projeto

### 1. Variáveis de Ambiente Necessárias

```bash
# OpenAI (OBRIGATÓRIO)
OPENAI_API_KEY=sk-your-openai-api-key-here

# ElevenLabs (opcional - apenas para síntese de voz)
ELEVENLABS_API_KEY=your-elevenlabs-api-key-here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Supabase (OBRIGATÓRIO)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key-here

# Sistema (Railway configura automaticamente)
PORT=8000
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

---

## 🚂 Deploy Passo a Passo

### Passo 1: Commit das Mudanças

```bash
git add .
git commit -m "feat: configuração para deploy Railway"
git push origin main
```

### Passo 2: Configurar Railway

1. **Acesse** [railway.app](https://railway.app)
2. **Faça login** com GitHub
3. **Clique em** "New Project"
4. **Selecione** "Deploy from GitHub repo"
5. **Escolha** seu repositório `oktasales-test`

### Passo 3: Configurar Variáveis de Ambiente

1. **No dashboard do Railway**, clique no seu projeto
2. **Vá para** a aba "Variables"
3. **Adicione as variáveis:**

```
OPENAI_API_KEY = sk-seu-api-key-aqui
SUPABASE_URL = https://seu-projeto.supabase.co
SUPABASE_ANON_KEY = sua-anon-key-aqui
ELEVENLABS_API_KEY = sua-elevenlabs-key-aqui (opcional)
```

### Passo 4: Deploy Automático

1. **Railway detectará** o Dockerfile automaticamente
2. **O build iniciará** automaticamente
3. **Aguarde** 2-5 minutos para completar
4. **Teste** a URL fornecida pelo Railway

---

## 🌐 Frontend (Opcional - Vercel)

### Para hospedar o frontend separadamente:

1. **Fork/Clone** apenas a pasta `frontend`
2. **No Vercel:**
   - Conecte ao GitHub
   - Configure build command: `npm run build`
   - Configure output directory: `build`
   - Adicione variável: `REACT_APP_API_URL=https://sua-api.railway.app`

---

## ✅ Verificação de Deploy

### 1. Teste a API

```bash
curl https://seu-projeto.railway.app/health
```

**Resposta esperada:**
```json
{"status": "healthy", "timestamp": "2024-01-XX..."}
```

### 2. Teste o Chat

```bash
curl -X POST https://seu-projeto.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-session" \
  -d '{"message": "olá"}'
```

### 3. Interface Web

Acesse: `https://seu-projeto.railway.app` (se servindo frontend junto)

---

## 🔍 Troubleshooting

### Problemas Comuns:

**1. Build falha - "ModuleNotFoundError"**
```bash
# Solução: Verificar requirements.txt
pip freeze > requirements.txt
git add requirements.txt && git commit -m "fix: update requirements" && git push
```

**2. API não responde - "502 Bad Gateway"**
- Verificar variáveis de ambiente no Railway
- Verificar logs: Railway Dashboard > Deployments > View Logs

**3. CORS errors no frontend**
- Verificar ALLOWED_ORIGINS no config.py
- Adicionar domínio do frontend nas origens permitidas

**4. OpenAI errors**
- Verificar se OPENAI_API_KEY está configurada
- Verificar se tem créditos na conta OpenAI

---

## 💰 Custos Estimados

### Railway: ~$5/mês
- 512MB RAM
- Compute time baseado no uso
- Domínio personalizado incluído

### APIs Externas:
- **OpenAI:** $0.03 por 1K tokens (GPT-4)
- **ElevenLabs:** $1/mês (10K caracteres)
- **Supabase:** Grátis até 500MB

**Total estimado:** $6-8/mês

---

## 🔄 Deploy Automático

Após configuração inicial, qualquer push para `main` redeploya automaticamente:

```bash
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
# Railway faz deploy automaticamente
```

---

## 📞 Suporte

- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Logs em tempo real:** Railway Dashboard > View Logs
- **Monitoramento:** Railway Dashboard > Metrics 