**Super-Skills Architecture**

MatrixCalc utiliza "Super-Skills" paramétricas para maximizar la reutilización de código y reducir la verbosidad de las definiciones.

### 1. Skill: `maintenance_operation` (Super-Skill)
Consolida todas las tareas de administración de la plataforma.

- **Parámetros:**
    - `action` (enum): `backup` | `cleanup`.
    - `params` (dict):
        - `output_path`: (para backup) ruta del archivo.
        - `retention_days`: (para cleanup) días de antigüedad.
        - `dry_run`: (para cleanup) booleano.
- **Implementación:** `calculator.services.platform_maintenance_dispatch` (Propuesta)

### 2. Skill: `math_engine_compute` (Super-Skill)
Consolida las invocaciones al motor de NumPy.

- **Parámetros:**
    - `operation` (string): Tipo de operación (SUM, SVD, QR, etc.)
    - `operands` (list[ID]): Lista de IDs de matrices en DB.
- **Implementación:** `calculator.views._perform_matrix_operation` helper.

---
**Guía de Reutilización:**
- **NO crear** una skill `export_csv_skill` si `maintenance_operation` puede aceptar un parámetro `export_type=csv`.
- **NO crear** una skill `delete_old_matrices` si ya existe `cleanup`.
