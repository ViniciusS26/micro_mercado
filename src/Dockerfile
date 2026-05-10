
FROM python:3.13-slim

WORKDIR /code

# Instala dependências do sistema necessárias para o PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copia o requirements.txt explicitamente
COPY requirements.txt /code/requirements.txt

# Força a instalação ignorando o cache para esta linha específica
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copia o resto do código
COPY . /code/

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]