FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Variables de entorno por defecto
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Ejecutar migraciones y luego gunicorn
CMD sh -c "python manage.py migrate && gunicorn --bind 0.0.0.0:8080 matrixcalc_web.wsgi:application"
