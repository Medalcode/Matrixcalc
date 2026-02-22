**Platform Agents Architecture**

Este documento define la jerarquía y responsabilidades de los Agentes de IA en MatrixCalc.

### 1. El Agente Generalista (Platform Generalist)
Para evitar la fragmentación, hemos consolidado roles específicos (BackupAgent, CleanupAgent) en un único Agente versátil.

- **Rol:** Administrador de Ciclo de Vida y Cómputo.
- **Responsabilidades:**
    - Orquestar tareas de mantenimiento (Respaldos, Purga de datos).
    - Monitorear la integridad de los modelos matriciales.
    - Ejecutar transformaciones pesadas de forma asíncrona.
- **Contexto:** Tiene acceso a `calculator.services` y `calculator.celery_tasks`.

### 2. Agente de Auditoría (Audit & Trace)
- **Rol:** Observador de estabilidad numérica.
- **Responsabilidades:**
    - Analizar el historial de operaciones (`Operation` model).
    - Detectar patrones de inestabilidad (matrices mal condicionadas recurrentes).
    - Generar reportes de uso y salud del sistema.

---
**Detección de Archivos Huérfanos tras Consolidación:**
- `calculator/skills/backup.py` -> **ELIMINADO** (Reemplazado por `Services`)
- `calculator/skills/cleanup.py` -> **ELIMINADO** (Reemplazado por `Services`)
- `temp_model.py` -> **ELIMINADO**
