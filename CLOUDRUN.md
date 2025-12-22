# 🚀 Quick Start - Cloud Run Deployment

## Configuración completa para desplegar MatrixCalc en GCP Cloud Run + Supabase

### ✅ Archivos Creados

#### Dockerfiles
- **[Dockerfile.backend](Dockerfile.backend)** - Backend Django optimizado con multi-stage build
- **[Dockerfile.frontend](Dockerfile.frontend)** - Frontend Vue con nginx

#### Configuración
- **[cloudbuild.yaml](cloudbuild.yaml)** - CI/CD automático con Cloud Build
- **[.env.cloudrun.example](.env.cloudrun.example)** - Template de variables de entorno
- **[docker/nginx.conf](docker/nginx.conf)** - Nginx optimizado para Cloud Run (puerto 8080)

#### Scripts
- **[scripts/validate-deployment.sh](scripts/validate-deployment.sh)** - Validación pre-deployment

#### Documentación
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa paso a paso

### 🎯 Optimizaciones Implementadas

#### Backend
- ✅ Multi-stage build (reduce tamaño imagen)
- ✅ Python 3.13-slim
- ✅ Usuario no-root (seguridad)
- ✅ WhiteNoise para static files
- ✅ Gunicorn con 2 workers + 4 threads
- ✅ Health checks de BD
- ✅ SSL support para Supabase

#### Frontend
- ✅ Build optimizado con Vite
- ✅ Nginx con gzip compression
- ✅ Cache de assets (1 año)
- ✅ Security headers
- ✅ Health check endpoint

#### Settings Django
- ✅ Cloud Run auto-detection
- ✅ CORS configurable via env vars
- ✅ DATABASE_URL con Supabase support
- ✅ Static files con WhiteNoise
- ✅ Debug automáticamente False en producción

### 🔥 Deploy Rápido (5 pasos)

```bash
# 1. Crear DB en Supabase (https://supabase.com)
#    Copiar DATABASE_URL

# 2. Configurar GCP
gcloud config set project [TU_PROJECT_ID]
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# 3. Crear Artifact Registry
gcloud artifacts repositories create matrixcalc \
  --repository-format=docker \
  --location=us-central1

# 4. Deploy Backend
gcloud run deploy matrixcalc-backend \
  --source . \
  --region us-central1 \
  --set-env-vars DATABASE_URL="[TU_SUPABASE_URL]" \
  --set-env-vars SECRET_KEY="[GENERAR_CON_DJANGO]" \
  --allow-unauthenticated

# 5. Deploy Frontend (actualizar VITE_API_URL con URL del backend)
echo "VITE_API_URL=https://[BACKEND_URL]/api" > frontend/.env.production
gcloud run deploy matrixcalc-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### 💰 Costo: $0/mes

- ✅ Cloud Run: 2M requests gratis
- ✅ Cloud Build: 120 builds/día gratis
- ✅ Supabase: 500MB PostgreSQL gratis
- ✅ Artifact Registry: 0.5GB gratis

### 📚 Documentación Completa

Ver **[DEPLOYMENT.md](DEPLOYMENT.md)** para:
- Setup detallado de Supabase
- Configuración de CI/CD
- Troubleshooting
- Comandos útiles
- Monitoreo y logs

---

**¿Listo para deploy?** Ejecuta el validador:
```bash
./scripts/validate-deployment.sh
```
