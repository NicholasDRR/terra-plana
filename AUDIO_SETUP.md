# Configuração de Funcionalidades de Áudio

## Variáveis de Ambiente Necessárias

Adicione estas variáveis ao seu arquivo `.env`:

```env
# OpenAI Configuration (para Whisper)
OPENAI_API_KEY=your_openai_api_key_here

# ElevenLabs Configuration (para síntese de voz)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Supabase Configuration (para persistência)
SUPABASE_URL=your_supabase_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## Como Obter as Chaves

### OpenAI API Key
1. Acesse [OpenAI Platform](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá para API Keys e gere uma nova chave
4. Certifique-se de ter créditos para usar Whisper

### ElevenLabs API Key
1. Acesse [ElevenLabs](https://elevenlabs.io)
2. Crie uma conta ou faça login
3. Vá para Profile → API Key
4. Copie sua chave API
5. Para vozes em português, recomendamos usar vozes multilíngues

### Supabase
1. Acesse [Supabase](https://supabase.com)
2. Crie um novo projeto
3. Execute o script `supabase_setup.sql` no SQL Editor
4. Copie a URL do projeto e a chave anônima

## Funcionalidades Implementadas

### Frontend
- 🎤 **Gravação de áudio** usando MediaRecorder API
- ⏺️ **Indicador visual** de gravação com timer
- 🔊 **Player de áudio** para reproduzir respostas do Eduardo
- 📱 **Responsivo** e compatível com dispositivos móveis

### Backend
- 🎯 **Transcrição** com OpenAI Whisper (português)
- 🗣️ **Síntese de voz** com ElevenLabs (português brasileiro)
- 💾 **Cache temporário** de arquivos de áudio
- 🔧 **Validação** de formatos e tamanhos de áudio

## Formatos Suportados

**Entrada (gravação):**
- WebM (preferido para navegadores modernos)
- OGG (fallback)
- MP3, WAV, M4A (upload manual)

**Saída (resposta):**
- MP3 (ElevenLabs)

## Limites

- **Tamanho máximo:** 25MB por arquivo
- **Duração:** Sem limite definido (mas considere custos da API)
- **Idioma:** Português (configurado no Whisper)

## Endpoints da API

```
POST /chat/audio              # Enviar áudio e receber resposta
GET  /chat/audio/download/{id} # Download do áudio gerado
GET  /chat/audio/voices        # Listar vozes disponíveis
DELETE /chat/audio/cache       # Limpar cache (manutenção)
```

## Troubleshooting

### Áudio não é suportado
- Verifique se está usando HTTPS (necessário para MediaRecorder)
- Alguns navegadores antigos não suportam gravação
- Verifique permissões do microfone

### Erro na transcrição
- Verifique se OPENAI_API_KEY está configurada
- Confirme se há créditos na conta OpenAI
- Fale claramente e evite ruído de fundo

### Erro na síntese de voz
- Verifique se ELEVENLABS_API_KEY está configurada
- Confirme se há caracteres disponíveis na conta ElevenLabs
- Teste com textos menores primeiro

## Custos

- **Whisper:** ~$0.006 por minuto de áudio
- **ElevenLabs:** ~$0.18 por 1000 caracteres (plano starter)

Monitore o uso para evitar custos inesperados! 