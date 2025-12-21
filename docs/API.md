# 🔌 Documentación API REST - MatrixCalc

**Base URL**: `http://localhost:8000/api`

Esta documentación describe todos los endpoints disponibles en la API REST de MatrixCalc.

---

## 📋 Tabla de Contenidos

- [Autenticación](#autenticación)
- [Rate Limiting](#rate-limiting)
- [Formato de Respuestas](#formato-de-respuestas)
- [Endpoints](#endpoints)
  - [Matrices](#matrices)
  - [Operaciones](#operaciones)
  - [Estadísticas](#estadísticas)
- [Códigos de Error](#códigos-de-error)
- [Ejemplos](#ejemplos)

---

## 🔐 Autenticación

Actualmente la API es **pública** y no requiere autenticación. En futuras versiones se implementará autenticación JWT.

---

## ⏱️ Rate Limiting

- **Límite**: 100 peticiones por hora por IP
- **Headers de respuesta**:
  - `X-RateLimit-Limit`: Límite total
  - `X-RateLimit-Remaining`: Peticiones restantes
  - `X-RateLimit-Reset`: Timestamp de reset

**Respuesta cuando se excede el límite:**
```json
{
  "error": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## 📦 Formato de Respuestas

### Éxito (200, 201)

```json
{
  "id": 1,
  "name": "Matriz A",
  "rows": 2,
  "cols": 2,
  "data": [[1, 2], [3, 4]],
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T10:30:00Z"
}
```

### Error (400, 404, 500)

```json
{
  "error": "Dimensiones incompatibles para suma"
}
```

---

## 📍 Endpoints

### Matrices

#### 📝 Listar Matrices

```http
GET /api/matrices/
```

**Query Parameters:**
- `page` (opcional): Número de página (default: 1)
- `page_size` (opcional): Elementos por página (default: 10, max: 100)

**Respuesta (200):**
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/matrices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Matriz A",
      "rows": 2,
      "cols": 2,
      "data": [[1, 2], [3, 4]],
      "created_at": "2025-12-21T10:30:00Z",
      "updated_at": "2025-12-21T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Matriz B",
      "rows": 2,
      "cols": 2,
      "data": [[5, 6], [7, 8]],
      "created_at": "2025-12-21T10:31:00Z",
      "updated_at": "2025-12-21T10:31:00Z"
    }
  ]
}
```

---

#### 🔍 Obtener Matriz por ID

```http
GET /api/matrices/{id}/
```

**Parámetros de URL:**
- `id`: ID de la matriz (entero)

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Matriz A",
  "rows": 2,
  "cols": 2,
  "data": [[1, 2], [3, 4]],
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T10:30:00Z"
}
```

**Errores:**
- `404`: Matriz no encontrada

---

#### ➕ Crear Matriz

```http
POST /api/matrices/
```

**Body (JSON):**
```json
{
  "name": "Matriz Nueva",
  "rows": 3,
  "cols": 3,
  "data": [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
  ]
}
```

**Validaciones:**
- `name`: Requerido, máximo 100 caracteres
- `rows`: Entero entre 1 y 100
- `cols`: Entero entre 1 y 100
- `data`: Array bidimensional con dimensiones correctas
- Todos los valores deben ser numéricos

**Respuesta (201):**
```json
{
  "id": 3,
  "name": "Matriz Nueva",
  "rows": 3,
  "cols": 3,
  "data": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
  "created_at": "2025-12-21T11:00:00Z",
  "updated_at": "2025-12-21T11:00:00Z"
}
```

**Errores:**
- `400`: Datos inválidos (ver mensaje de error)

---

#### ✏️ Actualizar Matriz

```http
PUT /api/matrices/{id}/
PATCH /api/matrices/{id}/
```

**Body (JSON):**
```json
{
  "name": "Matriz Actualizada",
  "data": [[2, 4], [6, 8]]
}
```

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Matriz Actualizada",
  "rows": 2,
  "cols": 2,
  "data": [[2, 4], [6, 8]],
  "created_at": "2025-12-21T10:30:00Z",
  "updated_at": "2025-12-21T11:15:00Z"
}
```

---

#### 🗑️ Eliminar Matriz

```http
DELETE /api/matrices/{id}/
```

**Respuesta (204):** Sin contenido

**Errores:**
- `404`: Matriz no encontrada

---

#### 📥 Importar Matriz desde CSV

```http
POST /api/matrices/import_csv/
```

**Body (multipart/form-data):**
- `file`: Archivo CSV
- `name`: Nombre de la matriz

**Formato CSV:**
```csv
1,2,3
4,5,6
7,8,9
```

**Respuesta (201):**
```json
{
  "id": 4,
  "name": "Matriz Importada",
  "rows": 3,
  "cols": 3,
  "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
  "created_at": "2025-12-21T11:30:00Z",
  "updated_at": "2025-12-21T11:30:00Z"
}
```

---

#### 📤 Exportar Matriz a CSV

```http
GET /api/matrices/{id}/export_csv/
```

**Respuesta (200):**
- Content-Type: `text/csv`
- Content-Disposition: `attachment; filename="matriz_{id}.csv"`

**Contenido:**
```csv
1,2,3
4,5,6
7,8,9
```

---

### Operaciones

#### ➕ Suma de Matrices

```http
POST /api/operations/sum/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1,
  "matrix_b_id": 2
}
```

**Validación:** Ambas matrices deben tener las mismas dimensiones (n×m).

**Respuesta (201):**
```json
{
  "id": 1,
  "operation_type": "SUM",
  "matrix_a": 1,
  "matrix_b": 2,
  "result": 5,
  "execution_time_ms": 2.45,
  "created_at": "2025-12-21T12:00:00Z",
  "matrix_a_data": {
    "id": 1,
    "name": "Matriz A",
    "data": [[1, 2], [3, 4]]
  },
  "matrix_b_data": {
    "id": 2,
    "name": "Matriz B",
    "data": [[5, 6], [7, 8]]
  },
  "result_data": {
    "id": 5,
    "name": "Resultado Suma",
    "data": [[6, 8], [10, 12]]
  }
}
```

**Errores:**
- `400`: Dimensiones incompatibles
- `404`: Una de las matrices no existe

---

#### ➖ Resta de Matrices

```http
POST /api/operations/subtract/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1,
  "matrix_b_id": 2
}
```

**Validación:** Mismas dimensiones.

**Respuesta (201):** Similar a suma

---

#### ✖️ Multiplicación de Matrices

```http
POST /api/operations/multiply/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1,
  "matrix_b_id": 2
}
```

**Validación:** Columnas de A = Filas de B (A: n×m, B: m×p → Resultado: n×p)

**Respuesta (201):** Similar a suma

**Errores:**
- `400`: Dimensiones incompatibles para multiplicación

---

#### 🔄 Transpuesta

```http
POST /api/operations/transpose/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1
}
```

**Respuesta (201):**
```json
{
  "id": 2,
  "operation_type": "TRANSPOSE",
  "matrix_a": 1,
  "matrix_b": null,
  "result": 6,
  "execution_time_ms": 1.23,
  "created_at": "2025-12-21T12:05:00Z",
  "matrix_a_data": {
    "id": 1,
    "name": "Matriz A",
    "data": [[1, 2, 3], [4, 5, 6]]
  },
  "result_data": {
    "id": 6,
    "name": "Resultado Transpuesta",
    "data": [[1, 4], [2, 5], [3, 6]]
  }
}
```

---

#### 🔢 Determinante

```http
POST /api/operations/determinant/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1
}
```

**Validación:** Matriz cuadrada (n×n)

**Respuesta (201):**
```json
{
  "id": 3,
  "operation_type": "DETERMINANT",
  "matrix_a": 1,
  "matrix_b": null,
  "result": 7,
  "execution_time_ms": 3.12,
  "created_at": "2025-12-21T12:10:00Z",
  "matrix_a_data": {
    "id": 1,
    "name": "Matriz A",
    "data": [[1, 2], [3, 4]]
  },
  "result_data": {
    "id": 7,
    "name": "Resultado Determinante",
    "data": [[-2.0]]
  }
}
```

**Nota:** El determinante se devuelve como matriz 1×1.

---

#### ↩️ Inversa

```http
POST /api/operations/inverse/
```

**Body (JSON):**
```json
{
  "matrix_a_id": 1
}
```

**Validaciones:**
- Matriz cuadrada (n×n)
- Determinante ≠ 0 (matriz no singular)
- Número de condición < 1e12 (estabilidad numérica)

**Respuesta (201):**
```json
{
  "id": 4,
  "operation_type": "INVERSE",
  "matrix_a": 1,
  "matrix_b": null,
  "result": 8,
  "execution_time_ms": 5.67,
  "created_at": "2025-12-21T12:15:00Z",
  "matrix_a_data": {
    "id": 1,
    "name": "Matriz A",
    "data": [[1, 2], [3, 4]]
  },
  "result_data": {
    "id": 8,
    "name": "Resultado Inversa",
    "data": [[-2.0, 1.0], [1.5, -0.5]]
  }
}
```

**Errores:**
- `400`: Matriz no cuadrada
- `400`: Matriz singular (determinante = 0)
- `400`: Matriz numéricamente inestable

---

### Estadísticas

#### 📊 Obtener Estadísticas Generales

```http
GET /api/stats/
```

**Respuesta (200):**
```json
{
  "total_matrices": 15,
  "total_operations": 42,
  "average_execution_time_ms": 3.45,
  "storage_mb": 0.25,
  "operations_by_type": {
    "SUM": 12,
    "SUBTRACT": 8,
    "MULTIPLY": 10,
    "TRANSPOSE": 6,
    "DETERMINANT": 4,
    "INVERSE": 2
  },
  "operations_timeline": [
    {
      "date": "2025-12-20",
      "count": 15
    },
    {
      "date": "2025-12-21",
      "count": 27
    }
  ],
  "average_execution_by_operation": {
    "SUM": 2.1,
    "SUBTRACT": 2.3,
    "MULTIPLY": 4.5,
    "TRANSPOSE": 1.8,
    "DETERMINANT": 3.2,
    "INVERSE": 5.9
  }
}
```

**Descripción de campos:**
- `total_matrices`: Total de matrices almacenadas
- `total_operations`: Total de operaciones realizadas
- `average_execution_time_ms`: Tiempo promedio de ejecución en milisegundos
- `storage_mb`: Espacio ocupado en base de datos (MB)
- `operations_by_type`: Conteo por tipo de operación
- `operations_timeline`: Operaciones de últimos 30 días
- `average_execution_by_operation`: Tiempo promedio por tipo de operación

---

## ⚠️ Códigos de Error

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Petición exitosa |
| 201 | Created | Recurso creado exitosamente |
| 204 | No Content | Recurso eliminado exitosamente |
| 400 | Bad Request | Datos inválidos o validación fallida |
| 404 | Not Found | Recurso no encontrado |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Error interno del servidor |

---

## 💡 Ejemplos

### Ejemplo Completo: Crear y Sumar Matrices

```bash
# 1. Crear Matriz A
curl -X POST http://localhost:8000/api/matrices/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Matriz A",
    "rows": 2,
    "cols": 2,
    "data": [[1, 2], [3, 4]]
  }'

# Respuesta: {"id": 1, ...}

# 2. Crear Matriz B
curl -X POST http://localhost:8000/api/matrices/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Matriz B",
    "rows": 2,
    "cols": 2,
    "data": [[5, 6], [7, 8]]
  }'

# Respuesta: {"id": 2, ...}

# 3. Sumar A + B
curl -X POST http://localhost:8000/api/operations/sum/ \
  -H "Content-Type: application/json" \
  -d '{
    "matrix_a_id": 1,
    "matrix_b_id": 2
  }'

# Respuesta: 
# {
#   "result_data": {
#     "data": [[6, 8], [10, 12]]
#   }
# }
```

### Ejemplo Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Crear matriz
response = requests.post(
    f"{BASE_URL}/matrices/",
    json={
        "name": "Matriz Identidad",
        "rows": 3,
        "cols": 3,
        "data": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    }
)
matriz = response.json()
print(f"Matriz creada con ID: {matriz['id']}")

# Calcular determinante
response = requests.post(
    f"{BASE_URL}/operations/determinant/",
    json={"matrix_a_id": matriz['id']}
)
operacion = response.json()
determinante = operacion['result_data']['data'][0][0]
print(f"Determinante: {determinante}")  # Salida: 1.0
```

### Ejemplo JavaScript (Axios)

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

// Crear matriz
const createMatrix = async () => {
  const response = await axios.post(`${API_BASE}/matrices/`, {
    name: 'Matriz Test',
    rows: 2,
    cols: 2,
    data: [[1, 2], [3, 4]]
  });
  return response.data;
};

// Calcular inversa
const calculateInverse = async (matrixId) => {
  try {
    const response = await axios.post(`${API_BASE}/operations/inverse/`, {
      matrix_a_id: matrixId
    });
    return response.data.result_data;
  } catch (error) {
    if (error.response?.status === 400) {
      console.error('Error:', error.response.data.error);
    }
    throw error;
  }
};

// Uso
const matrix = await createMatrix();
const inverse = await calculateInverse(matrix.id);
console.log('Inversa:', inverse.data);
```

---

## 🔗 Enlaces Útiles

- [Volver al README](../README.md)
- [Guía de Docker](../DOCKER.md)
- [Guía de Contribución](../CONTRIBUTING.md)

---

<div align="center">

**MatrixCalc API v2.0**

</div>
