# 🌍 Terra Plana Chat

> Sistema de chat inteligente com IA especializada em teoria da Terra Plana, desenvolvido com FastAPI e React.

[![Deploy Status](https://img.shields.io/badge/Backend-Railway-green)](https://terra-plana-production.up.railway.app/)
[![Deploy Status](https://img.shields.io/badge/Frontend-Vercel-blue)](https://terra-plana-frontend.vercel.app/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📖 Sobre o Projeto

O **Terra Plana Chat** é uma aplicação web que simula conversas com Eduardo Mayer, um professor especialista em teoria da Terra Plana. A IA foi treinada para manter conversas convincentes e educativas sobre este tema, mantendo um tom acadêmico e científico.

### ✨ Funcionalidades

- 💬 **Chat em tempo real** com IA especializada
- 🎤 **Mensagens de áudio** (transcrição e síntese de voz)
- 📊 **Histórico persistente** de conversas
- 🔄 **Scroll inteligente** estilo WhatsApp
- 📱 **Interface moderna** e responsiva
- 🔒 **Sessões isoladas** por usuário

## 🚀 Demo

- **Frontend:** [https://terra-plana-frontend.vercel.app/](https://terra-plana-frontend.vercel.app/)
- **API:** [https://terra-plana-production.up.railway.app/](https://terra-plana-production.up.railway.app/)
- **Documentação:** [https://terra-plana-production.up.railway.app/docs](https://terra-plana-production.up.railway.app/docs)

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web moderno para APIs
- **OpenAI GPT-4** - Inteligência artificial
- **ElevenLabs** - Síntese de voz (opcional)
- **Supabase** - Banco de dados PostgreSQL
- **Railway** - Deploy em produção

### Frontend
- **React 18** - Biblioteca de interface
- **Axios** - Cliente HTTP
- **CSS Modules** - Estilização moderna
- **Vercel** - Deploy em produção

## 📁 Estrutura do Projeto

```
oktasales-test/
├── 📁 app/                    # Backend API
│   ├── 📄 main.py            # Aplicação FastAPI
│   ├── 📄 config.py          # Configurações
│   ├── 📁 models/            # Modelos de dados
│   ├── 📁 routers/           # Endpoints da API
│   └── 📁 services/          # Lógica de negócio
├── 📁 frontend/              # Frontend React
│   ├── 📁 src/
│   │   ├── 📄 App.js         # Componente principal
│   │   └── 📄 index.js       # Entrada da aplicação
│   └── 📄 package.json       # Dependências Node.js
├── 📄 requirements.txt       # Dependências Python
├── 📄 Dockerfile             # Container para produção
└── 📄 README.md              # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Chaves de API:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [Supabase URL + Key](https://supabase.com)
  - [ElevenLabs API Key](https://elevenlabs.io) (opcional)

### 1. Configurar Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/terra-plana.git
cd terra-plana

# Crie o arquivo .env
cp .env.example .env
```

Edite o `.env` com suas chaves:
```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-aqui
ELEVENLABS_API_KEY=sua-chave-aqui
```

### 2. Backend (API)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API disponível em: http://localhost:8000

### 3. Frontend (React)

```bash
# Navegar para frontend
cd frontend

# Instalar dependências
npm install

# Executar aplicação
npm start
```

Frontend disponível em: http://localhost:3000

## 🐳 Executar com Docker

```bash
# Construir e executar
docker-compose up --build

# Executar em background
docker-compose up -d
```

## 📚 API Endpoints

### Base URL: `https://terra-plana-production.up.railway.app`

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/health` | Status da API |
| `POST` | `/chat/` | Enviar mensagem |
| `GET` | `/chat/history` | Obter histórico |
| `DELETE` | `/chat/history` | Limpar histórico |
| `POST` | `/chat/audio` | Enviar áudio |

### Exemplos de Uso

#### Enviar Mensagem
```bash
curl -X POST "https://terra-plana-production.up.railway.app/chat/" \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: minha-sessao" \
  -d '{"message": "Olá! Como você pode provar que a Terra é plana?"}'
```

#### Obter Histórico
```bash
curl -X GET "https://terra-plana-production.up.railway.app/chat/history" \
  -H "X-Session-ID: minha-sessao"
```

## 🌐 Deploy em Produção

### Backend (Railway)

1. Conecte seu repositório ao [Railway](https://railway.app)
2. Configure as variáveis de ambiente:
   ```
   OPENAI_API_KEY=sua-chave
   SUPABASE_URL=sua-url
   SUPABASE_ANON_KEY=sua-chave
   ```
3. Deploy automático a cada push

### Frontend (Vercel)

1. Conecte seu repositório ao [Vercel](https://vercel.com)
2. Configure:
   - **Root Directory:** `frontend`
   - **Framework:** Create React App
   - **Environment Variable:**
     ```
     REACT_APP_API_URL=https://sua-api.railway.app
     ```
3. Deploy automático a cada push

## 🔧 Configuração do Banco (Supabase)

1. Crie um projeto no [Supabase](https://supabase.com)
2. Execute o script SQL em **SQL Editor**:

```sql
-- Criar tabela de mensagens
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id TEXT NOT NULL,
    content TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índice para performance
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id, timestamp);
```

## 🎨 Funcionalidades da Interface

### Chat Inteligente
- **Scroll automático** apenas quando necessário
- **Botão "voltar ao final"** quando navegando histórico
- **Indicadores visuais** de status e carregamento
- **Layout responsivo** para mobile e desktop

### Controles de Áudio
- **Gravação de áudio** com indicador visual
- **Transcrição automática** com OpenAI Whisper
- **Síntese de voz** das respostas com ElevenLabs
- **Player integrado** para reproduzir áudios

## 📖 Documentação Avançada

- **API Docs:** [/docs](https://terra-plana-production.up.railway.app/docs)
- **ReDoc:** [/redoc](https://terra-plana-production.up.railway.app/redoc)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Desenvolvido por NicholasDRR

Criado como projeto educacional para demonstrar integração de IA com desenvolvimento web moderno.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!
