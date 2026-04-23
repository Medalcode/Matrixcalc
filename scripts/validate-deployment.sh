#!/bin/bash

# Script de validación pre-deployment
# Ejecutar antes de hacer deployment a Cloud Run

set -e

echo "🔍 Validando configuración para Cloud Run..."

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar archivos necesarios
echo "📁 Verificando archivos..."
files=("Dockerfile.backend" "Dockerfile.frontend" "cloudbuild.yaml" "requirements-web.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file existe"
    else
        echo -e "${RED}✗${NC} $file NO encontrado"
        exit 1
    fi
done

# Verificar variables de entorno necesarias
echo -e "\n🔐 Variables de entorno requeridas:"
required_vars=("DATABASE_URL" "SECRET_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${YELLOW}⚠${NC} $var no está definida (se debe configurar en Cloud Run)"
    else
        echo -e "${GREEN}✓${NC} $var está definida"
    fi
done

# Build test backend
echo -e "\n🏗️ Testing build del backend..."
if docker build -f Dockerfile.backend -t matrixcalc-backend-test . > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Backend build exitoso"
    docker rmi matrixcalc-backend-test > /dev/null 2>&1
else
    echo -e "${RED}✗${NC} Backend build falló"
    exit 1
fi

# Build test frontend
echo -e "\n🏗️ Testing build del frontend..."
if docker build -f Dockerfile.frontend -t matrixcalc-frontend-test . > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend build exitoso"
    docker rmi matrixcalc-frontend-test > /dev/null 2>&1
else
    echo -e "${RED}✗${NC} Frontend build falló"
    exit 1
fi

# Verificar Django settings
echo -e "\n⚙️ Verificando Django settings..."
if grep -q "whitenoise" requirements-web.txt; then
    echo -e "${GREEN}✓${NC} WhiteNoise configurado"
else
    echo -e "${RED}✗${NC} WhiteNoise no está en requirements"
fi

if grep -q "dj-database-url" requirements-web.txt; then
    echo -e "${GREEN}✓${NC} dj-database-url configurado"
else
    echo -e "${RED}✗${NC} dj-database-url no está en requirements"
fi

# Verificar frontend build config
echo -e "\n📦 Verificando frontend..."
if [ -f "frontend/package.json" ]; then
    if grep -q '"build"' frontend/package.json; then
        echo -e "${GREEN}✓${NC} Script de build encontrado"
    else
        echo -e "${RED}✗${NC} Script de build no encontrado"
    fi
else
    echo -e "${RED}✗${NC} package.json no encontrado"
fi

echo -e "\n${GREEN}✅ Validación completada!${NC}"
echo -e "\n📋 Próximos pasos:"
echo "1. Crear proyecto en Supabase y obtener DATABASE_URL"
echo "2. Generar SECRET_KEY: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo "3. Configurar GCP: gcloud config set project [PROJECT_ID]"
echo "4. Deploy: Ver instrucciones en DEPLOYMENT.md"
