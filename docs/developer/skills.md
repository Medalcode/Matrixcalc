**Overview**

En este proyecto una "skill" es una unidad reutilizable de trabajo que un agent puede invocar: p. ej. exportar backups, limpiar datos, ejecutar SVD/tranformaciones grandes o exportar CSV.

**Contrato de la skill**

- Entrada: parámetros serializables (dict) y opciones (timeout, force).
- Salida: objeto con `status`, `result` (o `error`) y `meta` (tiempos, ids de recursos).
- Requisitos: idempotencia o guardado de marca de ejecución para evitar duplicados.

**Implementación (ejemplos)**

- Management command-wrapper: convertir la lógica existente en funciones reutilizables y exponerlas como comandos y skills.
- Tarea Celery: envolver la función en una tarea para ejecución asíncrona y programada.
- HTTP wrapper: exponer una skill vía endpoint protegido para invocación remota.

**Testing & validation**

- Unit tests para cada skill (entrada/salida y manejo de errores).
- Tests de integración que ejecuten la skill como tarea Celery (puede usar broker in-memory para CI).

**Registro y descubrimiento**

- Registrar skills en `calculator/skills/__init__.py` o mantener convención de nombres (`*_skill`) para descubrimiento dinámico.

**Operacionalizar**

- Estimar recursos por skill (memoria/CPU) y documentarlos.
- Añadir métricas y trazas por skill; usar etiquetas para agrupación (backup, cleanup, compute).
