# Multi-stage build para optimizar tamaño de imagen
FROM python:3.13-slim as builder

WORKDIR /app

# Instalar dependencias de sistema necesarias para compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements para aprovechar cache de Docker
COPY requirements-web.txt .
# Instalar globalmente para facilitar acceso
RUN pip install --no-cache-dir -r requirements-web.txt

# Etapa final - imagen mínima
FROM python:3.13-slim

WORKDIR /app

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias instaladas desde builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código de la aplicación
COPY . .

# Collectstatic ANTES de cambiar de usuario
RUN python manage.py collectstatic --noinput

# Crear usuario no-root y dar permisos
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exponer puerto
EXPOSE 8080

# Variables de entorno por defecto (se sobrescriben en Cloud Run)
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    DEBUG=False

# Comando para iniciar aplicación
CMD exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 60 matrixcalc_web.wsgi:application
