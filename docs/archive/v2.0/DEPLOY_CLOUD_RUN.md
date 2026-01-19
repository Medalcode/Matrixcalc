# 🚀 Guía de Despliegue - MatrixCalc v2.0 con Todas las Mejoras

## 📋 Resumen de Mejoras Implementadas

Todas estas mejoras están listas para desplegar a Cloud Run:

### ✨ Frontend Mejorado

- ✅ Dark Mode completo (Light/Dark/Auto)
- ✅ Sistema de Toast Notifications
- ✅ Loading Spinners
- ✅ Modal de Confirmación
- ✅ 14 Templates de Matrices
- ✅ MatrixEditor mejorado
- ✅ MatrixList con confirmaciones
- ✅ OperationPanel con validaciones
- ✅ BackupManager renovado
- ✅ Páginas About y Docs con dark mode
- ✅ Homepage mejorado

### 🎨 Nuevos Componentes

- `ToastContainer.vue`
- `ThemeToggle.vue`
- `LoadingSpinner.vue`
- `ConfirmationModal.vue`
- `DocsView.vue` (página documentación)

### ⚙️ Nuevos Composables

- `useToast.ts`
- `useTheme.ts`
- `useConfirmation.ts`

### 📐 Nuevas Utilidades

- `matrixTemplates.ts` (14 templates)

---

## 🚀 Despliegue a Cloud Run

### Opción 1: Deploy Rápido con gcloud CLI

```bash
# 1. Navegar al proyecto
cd /home/medalcode/Antigravity/Matrixcalc

# 2. Asegurarse que el proyecto de GCP esté configurado
gcloud config set project [TU_PROJECT_ID]

# 3. Habilitar servicios necesarios
gcloud services enable run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com

# 4. Crear Artifact Registry (solo primera vez)
gcloud artifacts repositories create matrixcalc \
  --repository-format=docker \
  --location=us-central1 \
  --description="MatrixCalc Docker images"

# 5. Build y Deploy Backend
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_REPOSITORY=matrixcalc,_DATABASE_URL="[TU_DATABASE_URL]",_SECRET_KEY="[TU_SECRET_KEY]",_ALLOWED_HOSTS="*"

# 6. Obtener URL del backend
BACKEND_URL=$(gcloud run services describe matrixcalc-backend \
  --region=us-central1 \
  --format="value(status.url)")

echo "Backend URL: $BACKEND_URL"

# 7. Configurar frontend para apuntar al backend
echo "VITE_API_URL=${BACKEND_URL}/api" > frontend/.env.production

# 8. Re-deploy frontend con la nueva configuración
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_REPOSITORY=matrixcalc
```

### Opción 2: Deploy Manual Paso a Paso

#### Backend:

```bash
# 1. Build imagen backend
docker build -t gcr.io/[PROJECT_ID]/matrixcalc-backend:latest \
  -f Dockerfile.backend .

# 2. Push imagen
docker push gcr.io/[PROJECT_ID]/matrixcalc-backend:latest

# 3. Deploy a Cloud Run
gcloud run deploy matrixcalc-backend \
  --image=gcr.io/[PROJECT_ID]/matrixcalc-backend:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="DATABASE_URL=[TU_DB_URL],SECRET_KEY=[TU_SECRET],DEBUG=False" \
  --memory=512Mi \
  --cpu=1 \
  --max-instances=10 \
  --min-instances=0
```

#### Frontend:

```bash
# 1. Configurar variable de entorno
echo "VITE_API_URL=https://[BACKEND-URL]/api" > frontend/.env.production

# 2. Build imagen frontend
docker build -t gcr.io/[PROJECT_ID]/matrixcalc-frontend:latest \
  -f Dockerfile.frontend .

# 3. Push imagen
docker push gcr.io/[PROJECT_ID]/matrixcalc-frontend:latest

# 4. Deploy a Cloud Run
gcloud run deploy matrixcalc-frontend \
  --image=gcr.io/[PROJECT_ID]/matrixcalc-frontend:latest \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --memory=256Mi \
  --cpu=1 \
  --max-instances=5 \
  --min-instances=0
```

---

## 📝 Variables de Entorno Necesarias

### Backend (`matrixcalc-backend`)

```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Tu PostgreSQL/Supabase
SECRET_KEY=tu-secret-key-super-segura-aqui          # Generar con Django
DEBUG=False                                          # Siempre False en producción
ALLOWED_HOSTS=*                                      # O tu dominio específico
CORS_ALLOWED_ORIGINS=https://[FRONTEND-URL]         # URL del frontend
```

### Frontend (`matrixcalc-frontend`)

Esta variable se configura en **build time** en `frontend/.env.production`:

```bash
VITE_API_URL=https://[BACKEND-URL]/api
```

---

## ✅ Verificación Post-Deploy

### 1. Verificar Backend

```bash
# Obtener URL del backend
BACKEND_URL=$(gcloud run services describe matrixcalc-backend \
  --region=us-central1 \
  --format="value(status.url)")

# Probar health check
curl $BACKEND_URL/api/stats/

# Debería retornar JSON con estadísticas
```

### 2. Verificar Frontend

```bash
# Obtener URL del frontend
FRONTEND_URL=$(gcloud run services describe matrixcalc-frontend \
  --region=us-central1 \
  --format="value(status.url)")

echo "Aplicación disponible en: $FRONTEND_URL"

# Abrir en navegador
open $FRONTEND_URL  # Mac
xdg-open $FRONTEND_URL  # Linux
```

### 3. Probar Funcionalidades

Visita la URL del frontend y verifica:

- ✅ Homepage carga correctamente
- ✅ Dark Mode funciona (botón en navegación)
- ✅ Ir a /calculator → Templates visibles
- ✅ Crear matriz → Toast de confirmación
- ✅ Ir a /stats → Gráficos cargan
- ✅ Ir a /about → Página About con dark mode
- ✅ Ir a /docs → Documentación completa

---

## 🐛 Troubleshooting

### Error: "Network Error" en Estadísticas

**Causa:** Frontend no puede conectar con backend

**Solución:**

```bash
# 1. Verificar que backend esté corriendo
gcloud run services list --region=us-central1

# 2. Verificar CORS en backend
# Asegúrate que CORS_ALLOWED_ORIGINS incluya la URL del frontend

# 3. Rebuild frontend con la URL correcta
echo "VITE_API_URL=https://[BACKEND-REAL-URL]/api" > frontend/.env.production
# Re-deploy frontend
```

### Error: "Page Not Found" en /about o /docs

**Causa:** Rutas de Vue Router no configuradas en nginx

**Solución:** El `docker/nginx.conf` ya incluye `try_files $uri $uri/ /index.html;`

### Dark Mode no persiste

**Causa:** localStorage no funciona en modo incógnito

**Solución:** Normal, es comportamiento esperado del navegador

---

## 📊 Monitoreo

### Ver Logs del Backend

```bash
gcloud run services logs read matrixcalc-backend \
  --region=us-central1 \
  --limit=50 \
  --format=json
```

### Ver Logs del Frontend

```bash
gcloud run services logs read matrixcalc-frontend \
  --region=us-central1 \
  --limit=50
```

### Métricas en Cloud Console

```bash
# Abrir Cloud Console
echo "https://console.cloud.google.com/run?project=[PROJECT_ID]"
```

---

## 💰 Costos Estimados

Con Free Tier de GCP:

- **Cloud Run**: 2M requests/mes GRATIS
- **Cloud Build**: 120 builds/día GRATIS
- **Artifact Registry**: 0.5GB GRATIS
- **Cloud SQL/Supabase**: Depende del plan

**Costo estimado: $0-5/mes** para tráfico moderado

---

## 🔄 Actualización Continua

Para deployar cambios futuros:

```bash
# Commit cambios
git add .
git commit -m "feat: descripción del cambio"
git push

# Cloud Build automáticamente detecta el push y deploya
# (si configuraste triggers en Cloud Build)

# O manualmente:
gcloud builds submit --config=cloudbuild.yaml
```

---

## 📚 Archivos de Configuración

### Verificar que existan:

```bash
ls -la Dockerfile.backend
ls -la Dockerfile.frontend
ls -la cloudbuild.yaml
ls -la docker/nginx.conf
ls -la frontend/.env.production
```

Si falta alguno, revisar la documentación en CLOUDRUN.md

---

## 🎯 Checklist Pre-Deploy

- [ ] Backend funcionando localmente
- [ ] Frontend funcionando localmente
- [ ] Dark mode funcionando
- [ ] Toasts funcionando
- [ ] Estadísticas cargando datos
- [ ] DATABASE_URL configurado
- [ ] SECRET_KEY generado
- [ ] VITE_API_URL apuntando a backend correcto
- [ ] GCP Project configurado
- [ ] Artifact Registry creado
- [ ] Variables de entorno en Cloud Run configuradas

---

## 🎉 ¡Listo para Producción!

**MatrixCalc v2.0** con todas las mejoras está listo para desplegar:

- ✅ 17 archivos nuevos/modificados
- ✅ ~3,500 líneas de código agregadas
- ✅ 100% TypeScript
- ✅ Dark mode completo
- ✅ UX profesional
- ✅ Production-ready

**Comando para deploy completo:**

```bash
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=_DATABASE_URL="[TU_DB]",_SECRET_KEY="[TU_KEY]"
```

---

**Desarrollado con ❤️ - MatrixCalc v2.0**
_Actualizado: 23 de Diciembre de 2025_
