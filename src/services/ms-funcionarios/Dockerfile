
# ==========================================
# Etapa 1: Builder (Instalação de dependências)
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Instala dependências do sistema necessárias para compilar libs (ex: psycopg2 para PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências Python em uma pasta de wheels
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# Etapa 2: Imagem Final (Execução leve e segura)
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Instala apenas as bibliotecas de tempo de execução necessárias (ex: libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia os pacotes instalados da etapa de build
COPY --from=builder /install /usr/local

# Cria um usuário sem privilégios de root para segurança
RUN addgroup --system appgroup && adduser --system --group appuser

# Copia o código-fonte da aplicação
COPY ./app ./app

# Ajusta permissões de arquivos
RUN chown -R appuser:appgroup /app

# Troca para o usuário não-root
USER appuser

# Expõe a porta da aplicação
EXPOSE 8000

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Comando para iniciar o servidor Uvicorn (FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]