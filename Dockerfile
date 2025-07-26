# Dockerfile Multi-Stage Otimizado para Railway
# Stage 1: Build do Frontend React
FROM node:18-alpine as frontend-builder

WORKDIR /app/frontend

# Copiar package.json e instalar dependências
COPY frontend/package*.json ./
RUN npm ci --only=production --no-audit --no-fund

# Copiar código do frontend
COPY frontend/ ./

# Build do React para produção (otimizado)
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false
RUN npm run build

# Stage 2: Backend Python + Servir Frontend
FROM python:3.11-slim

# Configurar timezone
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Instalar apenas dependências essenciais
RUN apt-get update && apt-get install -y \
    gcc \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash app

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python primeiro (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app/ ./app/

# Copiar build do frontend do stage anterior
COPY --from=frontend-builder /app/frontend/build ./app/static

# Criar diretório para arquivos temporários
RUN mkdir -p /tmp/audio && chown -R app:app /tmp/audio /app

# Mudar para usuário não-root
USER app

# Expor porta
EXPOSE 8000

# Health check simplificado
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Comando otimizado para produção
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 