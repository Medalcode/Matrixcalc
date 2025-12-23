#!/bin/bash

# MatrixCalc v2.0 - Cloud Run Deploy Script
# Este script despliega MatrixCalc con todas las mejoras a Google Cloud Run

set -e  # Exit on error

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 MatrixCalc v2.0 - Cloud Run Deployment${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI no está instalado${NC}"
    echo "Instalar desde: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project configuration
echo -e "${YELLOW}📋 Configuración del Proyecto${NC}"
read -p "Project ID (o presiona Enter para usar el actual): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ No hay proyecto configurado${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓${NC} Usando proyecto: $PROJECT_ID"

# Set project
gcloud config set project $PROJECT_ID

# Get region
read -p "Región (default: us-central1): " REGION
REGION=${REGION:-us-central1}

echo -e "${GREEN}✓${NC} Región: $REGION"

# Database URL
echo ""
echo -e "${YELLOW}🗄️ Configuración de Base de Datos${NC}"
read -p "DATABASE_URL (PostgreSQL/Supabase): " DATABASE_URL

if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}❌ DATABASE_URL es requerido${NC}"
    exit 1
fi

# Secret Key
echo ""
echo -e "${YELLOW}🔐 Secret Key${NC}"
read -p "SECRET_KEY (o presiona Enter para generar uno): " SECRET_KEY

if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    echo -e "${GREEN}✓${NC} Secret key generado"
fi

# Enable required services
echo ""
echo -e "${YELLOW}⚙️ Habilitando servicios de GCP...${NC}"
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    --project=$PROJECT_ID

echo -e "${GREEN}✓${NC} Servicios habilitados"

# Create Artifact Registry (if doesn't exist)
echo ""
echo -e "${YELLOW}📦 Configurando Artifact Registry...${NC}"

if ! gcloud artifacts repositories describe matrixcalc --location=$REGION &>/dev/null; then
    gcloud artifacts repositories create matrixcalc \
        --repository-format=docker \
        --location=$REGION \
        --description="MatrixCalc Docker images"
    echo -e "${GREEN}✓${NC} Artifact Registry creado"
else
    echo -e "${GREEN}✓${NC} Artifact Registry ya existe"
fi

# Deploy Backend
echo ""
echo -e "${BLUE}🏗️ Desplegando Backend...${NC}"

gcloud run deploy matrixcalc-backend \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "DATABASE_URL=$DATABASE_URL,SECRET_KEY=$SECRET_KEY,DEBUG=False,ALLOWED_HOSTS=*" \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --min-instances 0 \
    --timeout 60

echo -e "${GREEN}✓${NC} Backend desplegado"

# Get backend URL
BACKEND_URL=$(gcloud run services describe matrixcalc-backend \
    --region=$REGION \
    --format="value(status.url)")

echo -e "${GREEN}✓${NC} Backend URL: $BACKEND_URL"

# Configure frontend environment
echo ""
echo -e "${YELLOW}⚙️ Configurando Frontend...${NC}"

echo "VITE_API_URL=${BACKEND_URL}/api" > frontend/.env.production

echo -e "${GREEN}✓${NC} Frontend configurado para conectar a: ${BACKEND_URL}/api"

# Deploy Frontend
echo ""
echo -e "${BLUE}🎨 Desplegando Frontend...${NC}"

gcloud run deploy matrixcalc-frontend \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --memory 256Mi \
    --cpu 1 \
    --max-instances 5 \
    --min-instances 0

echo -e "${GREEN}✓${NC} Frontend desplegado"

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe matrixcalc-frontend \
    --region=$REGION \
    --format="value(status.url)")

echo ""
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ ¡Despliegue Completado Exitosamente!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}🌐 URLs de la Aplicación:${NC}"
echo -e "   ${YELLOW}Frontend:${NC} $FRONTEND_URL"
echo -e "   ${YELLOW}Backend:${NC}  $BACKEND_URL"
echo ""
echo -e "${BLUE}📊 Próximos Pasos:${NC}"
echo -e "   1. Visita ${YELLOW}$FRONTEND_URL${NC}"
echo -e "   2. Prueba el dark mode con el botón en la navegación"
echo -e "   3. Ve a /calculator y prueba los templates"
echo -e "   4. Ve a /stats para ver las estadísticas"
echo ""
echo -e "${BLUE}📝 Monitoreo:${NC}"
echo -e "   Cloud Console: https://console.cloud.google.com/run?project=$PROJECT_ID"
echo ""
echo -e "${BLUE}💾 Configuración Guardada:${NC}"
echo -e "   PROJECT_ID: $PROJECT_ID"
echo -e "   REGION: $REGION"
echo -e "   BACKEND_URL: $BACKEND_URL"
echo -e "   FRONTEND_URL: $FRONTEND_URL"
echo ""
echo -e "${GREEN}🎉 ¡MatrixCalc v2.0 está en producción!${NC}"
