# 🚀 Despliegue a Google Cloud Run - MatrixCalc v2.0

## ✨ Todas las Mejoras Incluidas

Esta versión incluye **TODAS** las mejoras implementadas:

- ✅ Dark Mode completo (Light/Dark/Auto)
- ✅ Sistema de Toast Notifications (4 tipos)
- ✅ Loading Spinners en operaciones async
- ✅ Modal de Confirmación
- ✅ 14 Templates de Matrices
- ✅ Componentes mejorados (MatrixEditor, MatrixList, OperationPanel, BackupManager)
- ✅ Páginas About y Docs con dark mode
- ✅ Homepage renovado

**Total: 17 archivos nuevos/modificados | ~3,500 líneas de código**

---

## 🎯 Despliegue Rápido (1 Comando)

```bash
./scripts/deploy-cloudrun.sh
```

Este script interactivo te guiará paso a paso para:

1. Configurar tu proyecto de GCP
2. Habilitar servicios necesarios
3. Crear Artifact Registry
4. Desplegar backend
5. Desplegar frontend
6. Configurar variables de entorno

**Tiempo estimado: 10-15 minutos**

---

## 📋 Pre-requisitos

### 1. Cuenta de Google Cloud Platform

- Crear cuenta en: https://cloud.google.com/
- Free tier incluye: $300 créditos + servicios gratis permanentes

### 2. gcloud CLI Instalado

```bash
# Verificar instalación
gcloud --version

# Si no está instalado, descargar de:
# https://cloud.google.com/sdk/docs/install
```

### 3. Base de Datos PostgreSQL

**Opción A: Supabase (Recomendado - Gratis)**

```
1. Ir a https://supabase.com
2. Crear nuevo proyecto
3. Ir a Settings → Database
4. Copiar "Connection String" (URI mode)
```

**Opción B: Cloud SQL**

```bash
# Crear instancia de PostgreSQL
gcloud sql instances create matrixcalc-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1
```

### 4. Proyecto de GCP Configurado

```bash
# Listar proyectos
gcloud projects list

# Configurar proyecto activo
gcloud config set project [PROJECT_ID]
```

---

## 🚀 Opciones de Despliegue

### Opción 1: Script Automático (Recomendado)

```bash
# Ejecutar script interactivo
./scripts/deploy-cloudrun.sh

# El script te pedirá:
# - Project ID
# - Región (default: us-central1)
# - DATABASE_URL
# - SECRET_KEY (puede generar uno automático)
```

### Opción 2: Manual con Cloud Build

```bash
# 1. Configurar variables
export PROJECT_ID="tu-project-id"
export REGION="us-central1"
export DATABASE_URL="postgresql://..."
export SECRET_KEY="tu-secret-key"

# 2. Deploy con Cloud Build
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=$REGION,_DATABASE_URL="$DATABASE_URL",_SECRET_KEY="$SECRET_KEY"
```

### Opción 3: Deploy Separado (Backend y Frontend)

Ver guía completa en: [DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md)

---

## 🔧 Configuración Avanzada

### Variables de Entorno del Backend

Configurables en Cloud Run:

```bash
DATABASE_URL=postgresql://user:pass@host:5432/db    # Requerido
SECRET_KEY=your-secret-key-here                    # Requerido
DEBUG=False                                         # Recomendado
ALLOWED_HOSTS=*                                     # O tu dominio
CORS_ALLOWED_ORIGINS=https://frontend-url          # URL del frontend
```

### Variables de Entorno del Frontend

Configurar en `frontend/.env.production` antes del build:

```bash
VITE_API_URL=https://[BACKEND-URL]/api
```

---

## ✅ Verificación Post-Deploy

### 1. Verificar Servicios Desplegados

```bash
# Listar servicios en Cloud Run
gcloud run services list --region=us-central1

# Deberías ver:
# ✓ matrixcalc-backend
# ✓ matrixcalc-frontend
```

### 2. Probar Backend

```bash
# Obtener URL
BACKEND_URL=$(gcloud run services describe matrixcalc-backend \
  --region=us-central1 --format="value(status.url)")

# Probar endpoint
curl $BACKEND_URL/api/stats/

# Debe retornar JSON con estadísticas
```

### 3. Probar Frontend

```bash
# Obtener URL
FRONTEND_URL=$(gcloud run services describe matrixcalc-frontend \
  --region=us-central1 --format="value(status.url)")

# Abrir en navegador
echo "Aplicación: $FRONTEND_URL"
```

### 4. Probar Funcionalidades

Visita la URL del frontend y verifica:

| Funcionalidad | URL           | Verificar                |
| ------------- | ------------- | ------------------------ |
| Homepage      | `/`           | Dark mode toggle visible |
| Calculator    | `/calculator` | Templates funcionando    |
| Estadísticas  | `/stats`      | Gráficos cargando        |
| About         | `/about`      | Dark mode aplicado       |
| Docs          | `/docs`       | Página completa          |

---

## 🐛 Troubleshooting

### Error: "Network Error" en /stats

**Problema:** Frontend no puede conectar con backend

**Solución:**

```bash
# 1. Verificar URL del backend
gcloud run services describe matrixcalc-backend \
  --region=us-central1 --format="value(status.url)"

# 2. Actualizar frontend/.env.production
echo "VITE_API_URL=https://[BACKEND-URL]/api" > frontend/.env.production

# 3. Re-deploy frontend
gcloud run deploy matrixcalc-frontend --source=. --region=us-central1
```

### Error: "Page not found" en rutas

**Problema:** Nginx no redirige a index.html

**Solución:** Ya está configurado en `docker/nginx.conf`

### Dark Mode no se guarda

**Problema:** Normal en modo incógnito

**Solución:** Usar navegador normal (localStorage)

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Backend
gcloud run services logs tail matrixcalc-backend --region=us-central1

# Frontend
gcloud run services logs tail matrixcalc-frontend --region=us-central1
```

### Cloud Console

```bash
# Abrir Cloud Run dashboard
echo "https://console.cloud.google.com/run?project=[PROJECT_ID]"
```

### Métricas

- Requests por segundo
- Latencia
- Errores 4xx/5xx
- Uso de memoria/CPU

---

## 💰 Costos

### Free Tier de Cloud Run

- ✅ 2,000,000 requests/mes
- ✅ 360,000 GB-seconds
- ✅ 180,000 vCPU-seconds
- ✅ 2GB egress/mes

### Costo Estimado

- **Tráfico bajo** (< 10k requests/mes): **$0/mes**
- **Tráfico medio** (100k requests/mes): **~$2-5/mes**
- **Tráfico alto** (1M requests/mes): **~$10-20/mes**

---

## 🔄 Actualizar la Aplicación

### Después de hacer cambios en el código:

```bash
# 1. Commit cambios
git add .
git commit -m "feat: nueva funcionalidad"

# 2. Re-deploy
./scripts/deploy-cloudrun.sh

# O manualmente:
gcloud builds submit --config=cloudbuild.yaml
```

---

## 📚 Documentación Adicional

- [DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md) - Guía detallada
- [CLOUDRUN.md](CLOUDRUN.md) - Configuración original
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment general
- [MEJORAS_COMPLETAS.md](MEJORAS_COMPLETAS.md) - Resumen de mejoras

---

## 🎯 Checklist Pre-Deploy

- [ ] gcloud CLI instalado y configurado
- [ ] Proyecto de GCP creado
- [ ] Base de datos PostgreSQL disponible (Supabase/Cloud SQL)
- [ ] DATABASE_URL obtenido
- [ ] SECRET_KEY generado o disponible
- [ ] Servicios de GCP habilitados
- [ ] Código actualizado en local
- [ ] Tests pasando (opcional)

---

## 🎉 ¡Listo!

Tu aplicación MatrixCalc v2.0 con **TODAS** las mejoras está lista para desplegar a Cloud Run.

**Comando para empezar:**

```bash
./scripts/deploy-cloudrun.sh
```

**Tiempo total: 10-15 minutos**

---

**¿Necesitas ayuda?**

- Revisa [DEPLOY_CLOUD_RUN.md](DEPLOY_CLOUD_RUN.md) para troubleshooting
- Verifica logs en Cloud Console
- Contacta al equipo de desarrollo

---

_MatrixCalc v2.0 - Desarrollado con ❤️_  
_Actualizado: 23 de Diciembre de 2025_
