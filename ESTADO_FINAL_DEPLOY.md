# 🚀 MatrixCalc v3.0 - Estado Final del Despliegue

**Fecha:** 26 de Diciembre, 2025
**Estado:** ✅ OPERATIVO

## 🔗 URLs Definitivas

- **Frontend (Aplicación PWA):** [https://matrixcalc-frontend-541716295092.us-central1.run.app](https://matrixcalc-frontend-541716295092.us-central1.run.app)
- **Backend (API):** [https://matrixcalc-backend-772384307164.us-central1.run.app](https://matrixcalc-backend-772384307164.us-central1.run.app)

## 🛠️ Soluciones Aplicadas

### 1. Error de CORS (Cross-Origin Resource Sharing)

El navegador bloqueaba las peticiones porque el backend no enviaba los headers `Access-Control-Allow-Origin` correctamente.

- **Solución:** Se modificó `matrixcalc_web/settings.py` para leer y priorizar la variable de entorno `CORS_ALLOW_ALL_ORIGINS`.
- **Configuración:** `CORS_ALLOW_ALL_ORIGINS: "True"` en Cloud Run.

### 2. Error de Build en Backend (Cloud Build)

El despliegue fallaba al ejecutar `collectstatic` porque no tenía acceso a las credenciales de la base de datos durante la fase de construcción.

- **Solución:** Se comentó temporalmente `RUN python manage.py collectstatic` en el `Dockerfile`.

### 3. Error de Permisos en Backend (Permission Denied)

El contenedor fallaba al iniciar gunicorn (`exec: gunicorn: Permission denied`).

- **Solución:** Se comentó `USER appuser` en el `Dockerfile` para ejecutar el contenedor como root temporalmente y evitar problemas de permisos con ficheros copiados.

### 4. Mejoras UX y Debugging

- **Botón Guardar:** Se hizo visible, grande y azul en `MatrixEditor.vue`.
- **Logging:** Se añadió un sistema de logging detallado en `useMatrixAPI.ts` para facilitar el diagnóstico de errores en la consola del navegador.

## 📝 Comandos de Despliegue (Referencia)

**Backend:**

```bash
gcloud run deploy matrixcalc-backend --source . --region=us-central1 --project=matrixcalc-prod --allow-unauthenticated --env-vars-file=backend-prod-config.yaml
```

**Frontend:**

```bash
cd frontend && npm run build-only
cd ..
gcloud run deploy matrixcalc-frontend --source . --region=us-central1 --allow-unauthenticated --project=tuniforme-prod
```
