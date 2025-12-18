# Stage 1: Build Vue frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ .
RUN npm ci && npm run build-only

# Stage 2: Python Django backend
FROM python:3.13-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=frontend-builder /app/frontend/dist frontend/dist/

RUN python manage.py collectstatic --noinput

ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

EXPOSE 8080

CMD python manage.py migrate --noinput && exec gunicorn --bind :$PORT --workers 2 --threads 4 --timeout 120 matrixcalc_web.wsgi:application
