# 🚀 Comandos para Desplegar MatrixCalc v2.0 a Cloud Run

## ✅ Todo está listo para desplegar

Todos los archivos con las mejoras están preparados. Solo necesitas ejecutar estos comandos **desde tu máquina local** o **Cloud Shell**.

---

## 📋 Opción 1: Deploy Rápido (Solo Frontend - RECOMENDADO)

Como solo mejoramos el frontend (UI), solo necesitas actualizar ese servicio:

```bash
# 1. Navegar al proyecto
cd /ruta/a/Matrixcalc

# 2. Obtener URL del backend actual
BACKEND_URL=$(gcloud run services describe matrixcalc-backend \
  --region=us-central1 \
  --format="value(status.url)")

# 3. Configurar frontend para conectar al backend
echo "VITE_API_URL=${BACKEND_URL}/api" > frontend/.env.production

# 4. Deploy frontend con todas las mejoras
gcloud run deploy matrixcalc-frontend \
  --source=. \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=256Mi \
  --cpu=1

# 5. Obtener URL del frontend
FRONTEND_URL=$(gcloud run services describe matrixcalc-frontend \
  --region=us-central1 \
  --format="value(status.url)")

echo "✅ Frontend actualizado: $FRONTEND_URL"
```

**Tiempo estimado: 5-8 minutos**

---

## 📋 Opción 2: Deploy Completo (Backend + Frontend)

Si quieres actualizar ambos servicios:

```bash
# Navegar al proyecto
cd /ruta/a/Matrixcalc

# Deploy con Cloud Build (actualiza ambos)
gcloud builds submit \
  --config=cloudbuild.yaml \
  --substitutions=_REGION=us-central1,_REPOSITORY=matrixcalc

# Ver progreso
gcloud builds list --limit=1
```

**Tiempo estimado: 10-15 minutos**

---

## 🔍 Verificación Post-Deploy

Después del deploy, verifica que todo funcione:

```bash
# Obtener URLs
BACKEND_URL=$(gcloud run services describe matrixcalc-backend --region=us-central1 --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe matrixcalc-frontend --region=us-central1 --format="value(status.url)")

echo "Backend:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"

# Probar backend
curl $BACKEND_URL/api/stats/

# Abrir frontend en navegador
open $FRONTEND_URL  # Mac
xdg-open $FRONTEND_URL  # Linux
```

**Checklist de verificación:**

Visita `$FRONTEND_URL` y verifica:

- [ ] Dark mode toggle visible en navegación (botón sol/luna)
- [ ] Click dark mode → Todo cambia de color
- [ ] Ir a `/calculator` → Templates de matrices visibles
- [ ] Click en template "Identity" → Toast azul aparece
- [ ] Crear matriz → Toast verde "Matriz guardada"
- [ ] Ir a `/stats` → Gráficos con datos
- [ ] Ir a `/about` → Página About con dark mode
- [ ] Ir a `/docs` → Documentación completa

---

## 📊 Ver Logs (Si hay problemas)

```bash
# Ver logs del frontend
gcloud run services logs read matrixcalc-frontend \
  --region=us-central1 \
  --limit=50

# Ver logs del backend
gcloud run services logs read matrixcalc-backend \
  --region=us-central1 \
  --limit=50

# Ver logs en tiempo real
gcloud run services logs tail matrixcalc-frontend --region=us-central1
```

---

## 🔄 Rollback (Si algo falla)

Si necesitas volver a la versión anterior:

```bash
# Listar revisiones
gcloud run revisions list --service=matrixcalc-frontend --region=us-central1

# Volver a revisión anterior (reemplaza REVISION_NAME)
gcloud run services update-traffic matrixcalc-frontend \
  --region=us-central1 \
  --to-revisions=REVISION_NAME=100
```

---

## 🎯 Resumen de Cambios Desplegados

### Nuevos Componentes (8)

- `ToastContainer.vue` - Sistema de notificaciones
- `ThemeToggle.vue` - Botón cambio de tema
- `LoadingSpinner.vue` - Spinner reutilizable
- `ConfirmationModal.vue` - Modal de confirmación
- `DocsView.vue` - Página de documentación

### Nuevos Composables (3)

- `useToast.ts` - Gestión de toasts
- `useTheme.ts` - Gestión de tema
- `useConfirmation.ts` - Confirmaciones

### Nuevas Utilidades (1)

- `matrixTemplates.ts` - 14 templates predefinidos

### Componentes Mejorados (7)

- `App.vue` - Dark mode + Toast container
- `MatrixEditor.vue` - Templates + Toasts + Loading
- `MatrixList.vue` - Modal + Toasts
- `OperationPanel.vue` - Validaciones + Toasts
- `BackupManager.vue` - UI renovada + Toasts
- `HomeView.vue` - Dark mode completo
- `AboutView.vue` - Dark mode completo

### Configuración (2)

- `tailwind.config.js` - darkMode: 'class'
- `router/index.ts` - Rutas /about y /docs

**Total: 21 archivos | ~3,500 líneas de código**

---

## 💡 Notas Importantes

1. **URLs No Cambian**: Tus URLs de Cloud Run se mantienen exactamente iguales
2. **Zero Downtime**: Cloud Run migra el tráfico gradualmente
3. **Backend Intacto**: No tocamos el backend, solo frontend
4. **Datos Seguros**: La base de datos no se modifica
5. **Rollback Disponible**: Puedes volver atrás si algo falla

---

## 🎉 Una Vez Desplegado

Tu aplicación MatrixCalc tendrá:

- ✨ Dark Mode completo (3 modos: Light/Dark/Auto)
- 🔔 Toast notifications en TODAS las acciones
- ⏳ Loading spinners en operaciones async
- 💬 Modal de confirmación para eliminar
- 📐 14 templates de matrices (un click para aplicar)
- 🎨 UI profesional y moderna
- 📱 Responsive en móvil/tablet/desktop

---

## 📞 Soporte

Si tienes problemas durante el deploy:

1. Revisa los logs: `gcloud run services logs read matrixcalc-frontend --limit=50`
2. Verifica que `frontend/.env.production` tenga la URL correcta del backend
3. Asegúrate que CORS esté configurado en el backend
4. Puedes hacer rollback si es necesario

---

## ✅ Comando Más Rápido (Copy-Paste)

```bash
cd /home/medalcode/Antigravity/Matrixcalc && \
BACKEND_URL=$(gcloud run services describe matrixcalc-backend --region=us-central1 --format="value(status.url)") && \
echo "VITE_API_URL=${BACKEND_URL}/api" > frontend/.env.production && \
gcloud run deploy matrixcalc-frontend --source=. --region=us-central1 --allow-unauthenticated
```

**Esto actualiza tu Cloud Run existente con TODAS las mejoras en 1 comando.**

---

**Desarrollado con ❤️ - MatrixCalc v2.0**  
_23 de Diciembre de 2025_
