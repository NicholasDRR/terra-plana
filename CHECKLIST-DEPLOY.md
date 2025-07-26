# ✅ Checklist de Deploy Railway

## 🔍 Pré-Deploy (Verificar antes de começar)

- [ ] **Conta GitHub** ativa com projeto commitado
- [ ] **Conta Railway** criada ([railway.app](https://railway.app))
- [ ] **OpenAI API Key** disponível
- [ ] **Supabase** configurado com URL e Anon Key
- [ ] **ElevenLabs Key** (opcional, só para áudio)

---

## 🚀 Processo de Deploy (15 minutos)

### ⚡ Preparação Local (2 min)
```bash
# 1. Commit das mudanças
git add .
git commit -m "feat: setup Railway deploy"
git push origin main
```

### 🚂 Railway Setup (5 min)
1. [ ] Acesse [railway.app](https://railway.app)
2. [ ] Login com GitHub
3. [ ] "New Project" → "Deploy from GitHub repo"
4. [ ] Selecione `oktasales-test`
5. [ ] Aguarde detecção automática do Dockerfile

### 🔧 Configurar Variáveis (3 min)
No Railway Dashboard:
```
OPENAI_API_KEY = sk-proj-sua-key-aqui
SUPABASE_URL = https://seu-projeto.supabase.co
SUPABASE_ANON_KEY = sua-anon-key-aqui
ELEVENLABS_API_KEY = sua-key-aqui (opcional)
```

### ⏱️ Deploy e Teste (5 min)
1. [ ] Aguardar build automático (2-3 min)
2. [ ] Testar URL: `https://seu-projeto.railway.app/health`
3. [ ] Testar chat: Frontend ou API direta

---

## 🎯 URLs Importantes

- **Dashboard Railway:** https://railway.app/dashboard
- **Logs do Deploy:** Dashboard → Projeto → Deployments
- **Métricas:** Dashboard → Projeto → Metrics
- **Domínio Custom:** Dashboard → Projeto → Settings → Domains

---

## ⚠️ Se Der Erro

### Build falhou?
```bash
# Verificar logs no Railway Dashboard
# Comum: dependência faltando no requirements.txt
```

### API não responde?
- Verificar variáveis de ambiente
- Verificar logs: "View Logs" no Railway
- Testar localmente primeiro

### CORS errors?
- Adicionar domínio do frontend no config.py
- Verificar ALLOWED_ORIGINS

---

## 💡 Dicas

- **Deploy automático:** Todo push em `main` redeploya
- **Logs em tempo real:** Dashboard → View Logs
- **Custom domain:** Gratuito no Railway
- **SSL:** Automático
- **Backup:** Railway mantém histórico de deploys 