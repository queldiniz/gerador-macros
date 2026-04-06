# Imagem base leve (~150MB vs ~1GB da python:3.12)
FROM python:3.12-slim

WORKDIR /app

# Instala dependências primeiro (camada cacheada — só rebuilda se requirements.txt mudar)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copia o código da aplicação
COPY . .

# Diretório para o SQLite (será montado como volume)
RUN mkdir -p /app/instance

EXPOSE 5000

# Gunicorn: servidor WSGI de produção com 2 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:app"]
