#!/bin/bash

# Script para probar conexión con Supabase
# Uso: ./scripts/test-supabase-connection.sh

set -e

echo "🔍 Probando conexión a Supabase..."

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Cargar .env si existe
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo -e "${GREEN}✓${NC} Archivo .env cargado"
else
    echo -e "${YELLOW}⚠${NC} No se encontró archivo .env"
    echo "Copia .env.supabase.example a .env y completa la DATABASE_URL"
    exit 1
fi

# Verificar DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}✗${NC} DATABASE_URL no está definida"
    exit 1
fi

# Verificar si contiene [YOUR-PASSWORD]
if [[ "$DATABASE_URL" == *"[YOUR-PASSWORD]"* ]]; then
    echo -e "${RED}✗${NC} DATABASE_URL contiene [YOUR-PASSWORD]"
    echo "Reemplaza [YOUR-PASSWORD] con tu contraseña real de Supabase"
    exit 1
fi

echo -e "${GREEN}✓${NC} DATABASE_URL configurada"

# Test 1: Probar conexión con psql (si está instalado)
echo -e "\n📡 Test 1: Conexión directa con psql..."
if command -v psql &> /dev/null; then
    if psql "$DATABASE_URL" -c "SELECT version();" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Conexión exitosa con psql"
        psql "$DATABASE_URL" -c "SELECT version();" | head -n 3
    else
        echo -e "${RED}✗${NC} No se pudo conectar con psql"
        echo "Verifica que la contraseña sea correcta"
    fi
else
    echo -e "${YELLOW}⚠${NC} psql no está instalado, saltando test..."
fi

# Test 2: Probar con Django
echo -e "\n🐍 Test 2: Conexión con Django..."
python3 -c "
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'matrixcalc_web.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print('${GREEN}✓${NC} Conexión exitosa con Django')
        print(f'PostgreSQL: {version[0][:50]}...')
except Exception as e:
    print('${RED}✗${NC} Error de conexión:', str(e))
    sys.exit(1)
"

# Test 3: Ejecutar migraciones (dry-run)
echo -e "\n📋 Test 3: Verificando migraciones..."
if python3 manage.py migrate --plan > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Migraciones verificadas"
    pending=$(python3 manage.py showmigrations --plan 2>/dev/null | grep "\[ \]" | wc -l)
    if [ "$pending" -gt 0 ]; then
        echo -e "${YELLOW}⚠${NC} Hay $pending migraciones pendientes"
        echo "Ejecuta: python3 manage.py migrate"
    else
        echo -e "${GREEN}✓${NC} Todas las migraciones aplicadas"
    fi
else
    echo -e "${RED}✗${NC} Error al verificar migraciones"
fi

echo -e "\n${GREEN}✅ Tests completados!${NC}"
echo -e "\n📋 Próximos pasos:"
echo "1. Si hay migraciones pendientes: python3 manage.py migrate"
echo "2. Crear superusuario: python3 manage.py createsuperuser"
echo "3. Iniciar servidor: python3 manage.py runserver"
