# Deployment Guide - MatrixCalc en Cloud Run + Supabase

Esta guía te ayudará a desplegar MatrixCalc en Google Cloud Run usando Supabase como base de datos PostgreSQL.

## 📋 Prerrequisitos

1. **Cuenta de Google Cloud** con facturación habilitada (usaremos tier gratuito)
2. **Cuenta de Supabase** (tier gratuito - 500MB PostgreSQL)
3. **gcloud CLI** instalado: https://cloud.google.com/sdk/docs/install
4. **Git** con repositorio en GitHub

## 🚀 Paso 1: Configurar Supabase

### 1.1 Crear proyecto en Supabase

1. Ve a https://supabase.com y crea una cuenta
2. Crea un nuevo proyecto:
   - **Name**: `matrixcalc-db`
   - **Database Password**: Guarda esta contraseña (la necesitarás)
   - **Region**: Elige la más cercana (ej: `South America (São Paulo)`)

3. Espera 2-3 minutos mientras se crea el proyecto

### 1.2 Obtener credenciales de la base de datos

1. En tu proyecto Supabase, ve a **Settings** → **Database**
2. Busca **Connection string** → **URI**
3. Copia la URL (se verá así):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxx.supabase.co:5432/postgres
   ```
4. Reemplaza `[YOUR-PASSWORD]` con tu contraseña

### 1.3 Ejecutar migraciones

```bash
# Instalar psql si no lo tienes
sudo apt-get install postgresql-client  # Ubuntu/Debian
# o brew install postgresql  # macOS

# Conectar a Supabase
psql "postgresql://postgres:[PASSWORD]@db.xxxxxxxxxx.supabase.co:5432/postgres"

# Ejecutar migraciones manualmente o usar:
python manage.py migrate --database=supabase
```

## ☁️ Paso 2: Configurar Google Cloud Platform

### 2.1 Crear y configurar proyecto

```bash
# Login en GCP
gcloud auth login

# Crear nuevo proyecto
gcloud projects create matrixcalc-prod --name="MatrixCalc Production"

# Configurar proyecto actual
gcloud config set project matrixcalc-prod

# Habilitar APIs necesarias
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  containeranalysis.googleapis.com
```

### 2.2 Crear Artifact Registry

```bash
# Crear repositorio para imágenes Docker
gcloud artifacts repositories create matrixcalc \
  --repository-format=docker \
  --location=us-central1 \
  --description="MatrixCalc container images"

# Configurar autenticación
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### 2.3 Configurar variables de entorno secretas

```bash
# Generar SECRET_KEY seguro
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Crear archivo de secretos (NO commitear)
cat > .env.production << EOF
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxxxxxxx.supabase.co:5432/postgres
SECRET_KEY=[TU_SECRET_KEY_GENERADO]
ALLOWED_HOSTS=matrixcalc-backend-xxxxxxxxxx-uc.a.run.app,*
DEBUG=False
MAX_DIMENSION=100
RETENTION_DAYS=30
EOF
```

## 🏗️ Paso 3: Build y Deploy Manual (Primera vez)

### 3.1 Build y Push Backend

```bash
# Build imagen backend
docker build -f Dockerfile.backend -t us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-backend:latest .

# Push a Artifact Registry
docker push us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-backend:latest
```

### 3.2 Deploy Backend a Cloud Run

```bash
# Deploy backend
gcloud run deploy matrixcalc-backend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-backend:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="postgresql://postgres:[PASSWORD]@db.xxxxxxxxxx.supabase.co:5432/postgres" \
  --set-env-vars SECRET_KEY="[TU_SECRET_KEY]" \
  --set-env-vars DEBUG=False \
  --set-env-vars ALLOWED_HOSTS="*" \
  --max-instances 10 \
  --min-instances 0 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60

# Obtener URL del backend
gcloud run services describe matrixcalc-backend --region us-central1 --format 'value(status.url)'
# Ejemplo: https://matrixcalc-backend-xxxxxxxxxx-uc.a.run.app
```

### 3.3 Actualizar Frontend con URL del Backend

```bash
# Editar frontend/.env.production
cat > frontend/.env.production << EOF
VITE_API_URL=https://matrixcalc-backend-xxxxxxxxxx-uc.a.run.app/api
EOF
```

### 3.4 Build y Deploy Frontend

```bash
# Build imagen frontend
docker build -f Dockerfile.frontend -t us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-frontend:latest .

# Push a Artifact Registry
docker push us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-frontend:latest

# Deploy frontend
gcloud run deploy matrixcalc-frontend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-frontend:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --max-instances 5 \
  --min-instances 0 \
  --memory 256Mi \
  --cpu 1

# Obtener URL del frontend
gcloud run services describe matrixcalc-frontend --region us-central1 --format 'value(status.url)'
# Ejemplo: https://matrixcalc-frontend-xxxxxxxxxx-uc.a.run.app
```

## 🔄 Paso 4: Configurar CI/CD con Cloud Build

### 4.1 Conectar GitHub

```bash
# Instalar app de Cloud Build en GitHub
gcloud builds triggers create github \
  --name="matrixcalc-deploy" \
  --repo-name="Matrixcalc" \
  --repo-owner="[TU_USUARIO_GITHUB]" \
  --branch-pattern="^main$" \
  --build-config="cloudbuild.yaml"
```

### 4.2 Configurar variables en Cloud Build

1. Ve a [Cloud Build Triggers](https://console.cloud.google.com/cloud-build/triggers)
2. Click en el trigger `matrixcalc-deploy`
3. Click **Edit**
4. En **Substitution variables**, agrega:
   - `_DATABASE_URL`: Tu URL de Supabase
   - `_SECRET_KEY`: Tu SECRET_KEY de Django
   - `_ALLOWED_HOSTS`: `*` (o tu dominio específico)
   - `_REGION`: `us-central1`
   - `_REPOSITORY`: `matrixcalc`

### 4.3 Primer Deploy Automático

```bash
# Hacer push a main para activar CI/CD
git add .
git commit -m "Add Cloud Run deployment"
git push origin main

# Monitorear build
gcloud builds list --limit=1
gcloud builds log [BUILD_ID]
```

## 📊 Paso 5: Verificación y Monitoreo

### 5.1 Verificar servicios

```bash
# Ver servicios desplegados
gcloud run services list --region us-central1

# Probar backend
curl https://matrixcalc-backend-xxxxxxxxxx-uc.a.run.app/api/health

# Probar frontend
curl https://matrixcalc-frontend-xxxxxxxxxx-uc.a.run.app/health
```

### 5.2 Ver logs

```bash
# Logs del backend
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=matrixcalc-backend" --limit 50

# Logs del frontend
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=matrixcalc-frontend" --limit 50
```

### 5.3 Monitoreo en consola

1. **Cloud Run**: https://console.cloud.google.com/run
2. **Cloud Build**: https://console.cloud.google.com/cloud-build
3. **Artifact Registry**: https://console.cloud.google.com/artifacts
4. **Supabase**: https://app.supabase.com

## 💰 Costos Estimados (Tier Gratuito)

### Google Cloud (Free Tier)
- ✅ **Cloud Run**: 2M requests/mes, 360,000 GB-seconds/mes
- ✅ **Cloud Build**: 120 builds/día
- ✅ **Artifact Registry**: 0.5GB storage

### Supabase (Free Tier)
- ✅ **PostgreSQL**: 500MB storage
- ✅ **Bandwidth**: 2GB/mes
- ✅ **Queries**: Ilimitadas

**Total: $0/mes** si te mantienes dentro de los límites

## 🔧 Comandos Útiles

### Actualizar solo backend
```bash
gcloud run deploy matrixcalc-backend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-backend:latest \
  --region us-central1
```

### Actualizar solo frontend
```bash
gcloud run deploy matrixcalc-frontend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/matrixcalc-frontend:latest \
  --region us-central1
```

### Ver variables de entorno
```bash
gcloud run services describe matrixcalc-backend --region us-central1 --format 'value(spec.template.spec.containers[0].env)'
```

### Rollback a versión anterior
```bash
# Listar revisiones
gcloud run revisions list --service matrixcalc-backend --region us-central1

# Rollback
gcloud run services update-traffic matrixcalc-backend \
  --to-revisions [REVISION_NAME]=100 \
  --region us-central1
```

### Escalar manualmente
```bash
# Aumentar máximo de instancias
gcloud run services update matrixcalc-backend \
  --max-instances 20 \
  --region us-central1

# Mínimo de instancias (siempre activo - COSTO)
gcloud run services update matrixcalc-backend \
  --min-instances 1 \
  --region us-central1
```

## 🐛 Troubleshooting

### Error: "Invalid DATABASE_URL"
- Verifica que la URL de Supabase esté correcta
- Asegúrate de reemplazar `[YOUR-PASSWORD]`
- Prueba conectarte con `psql` primero

### Error: "Permission denied"
- Ejecuta: `gcloud auth login`
- Verifica permisos: `gcloud projects get-iam-policy matrixcalc-prod`

### Build muy lento
- Usa `.dockerignore` para excluir archivos innecesarios
- Aprovecha cache de Docker layers

### Backend no responde
- Verifica logs: `gcloud logging read "resource.labels.service_name=matrixcalc-backend"`
- Verifica health check: `curl [BACKEND_URL]/api/health`

### Frontend no conecta con backend
- Verifica CORS en Django settings
- Verifica que `VITE_API_URL` esté correcta en frontend

## 🔐 Seguridad

1. **NUNCA** commitees `.env.production` al repositorio
2. Usa **Secret Manager** de GCP para producción real
3. Restringe `ALLOWED_HOSTS` a tu dominio específico
4. Habilita **Cloud Armor** para DDoS protection (opcional)
5. Configura **Identity-Aware Proxy** para admin (opcional)

## 📈 Siguientes Pasos

1. **Dominio Custom**: Configura tu dominio en Cloud Run
2. **HTTPS**: Cloud Run incluye HTTPS automático
3. **Monitoring**: Configura alertas en Cloud Monitoring
4. **Backups**: Automatiza backups de Supabase
5. **CDN**: Usa Cloud CDN para frontend (opcional)

---

¿Problemas? Crea un issue en el repositorio.
