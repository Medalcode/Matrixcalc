**Overview**

Este documento describe el patrón de "agents" para MatrixCalc: procesos autorizados y orquestados que realizan tareas automáticas, programadas o asíncronas (backups, limpieza, cálculos pesados) fuera del flujo síncrono HTTP.

**Cuándo usar un agent**

- Backups periódicos o restauraciones agendadas.
- Tareas de limpieza/retención a gran escala.
- Operaciones computacionalmente intensivas que deben ejecutarse fuera del request-response.

**Modelos de ejecución**

- In-process (APScheduler): simple; buen fallback para entornos sin broker.
- External workers (Celery + Redis): recomendado para producción escalable; tolerancia, retries y control de recursos.
- Serverless jobs (Cloud Run Jobs): útil para ejecuciones puntuales y escalado por invocación.

**Puntos de integración**

- Management commands: [calculator/management/commands](../../calculator/management/commands) — reusar como skills.
- Scheduler app: [calculator/apps.py](../../calculator/apps.py) — programar invocaciones.
- REST API: [calculator/views.py](../../calculator/views.py) — iniciar workflows y consultar estado.
- Models: [calculator/models.py](../../calculator/models.py) — persistencia de resultados y metadatos.

**Seguridad y autenticación**

- Los agents deben usar credenciales de servicio (env vars o Secret Manager). No hardcodear secrets.
- Para llamadas HTTP internas, usar tokens de servicio o JWT con permisos mínimos.

**Operación y monitorización**

- Logging estructurado y métricas por task (duración, éxito/fracaso).
- Retries con backoff y idempotencia por task.
- Límites de recursos y separación de servicios (worker vs web).
