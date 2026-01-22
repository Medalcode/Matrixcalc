# 🧮 MatrixCalc Web

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.5-brightgreen.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Calculadora de matrices profesional con API REST y frontend moderno**

[Características](#-características) • [Demo](#-demo) • [Instalación](#-instalación) • [Documentación](#-documentación) • [Contribuir](#-contribuir)

</div>

---

## 📋 Índice

- [Características](#-características)
- [Arquitectura](#️-arquitectura)
- [Instalación](#-instalación)
  - [Con Docker (Recomendado)](#con-docker-recomendado)
  - [Desarrollo Local](#desarrollo-local)
- [Uso](#-uso)
- [API REST](#-api-rest)
- [Tecnologías](#️-tecnologías)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)
- [Versiones](#-versiones)

---

## ✨ Características

### 🔢 Operaciones Matriciales

- **Básicas** - Suma, Resta, Multiplicación
- **Avanzadas (Nuevo v3.0)** - Rank, Eigenvalues/Eigenvectors
- **Descomposiciones (Nuevo v3.0)** - SVD (Singular Value Decomposition), QR, Cholesky, LU
- **Propiedades** - Determinante, Inversa, Transpuesta, Traza
- **Transformaciones** - Potencia de matriz

### 💾 Gestión de Datos

- **CRUD completo** - Crear, leer, actualizar y eliminar matrices
- **Persistencia** - Almacenamiento en PostgreSQL/SQLite
- **Backup/Restore** - Exportación e importación en JSON/CSV
- **Historial** - Registro completo de operaciones realizadas
- **Limpieza automática** - Eliminación de datos antiguos configurable

### 📊 Estadísticas y Visualización

- **Dashboard interactivo** - Gráficos con Chart.js
- **Métricas en tiempo real** - Total de matrices, operaciones, tiempos de ejecución
- **Análisis temporal** - Timeline de operaciones de últimos 30 días
- **Distribución** - Operaciones por tipo con porcentajes

### 🛡️ Seguridad y Rendimiento

- **Rate Limiting** - Protección contra abuso de API (100 req/hora)
- **Validaciones** - Límites de dimensión y valores numéricos
- **Manejo de errores** - Excepciones personalizadas con mensajes claros
- **Optimización** - Índices de base de datos, caché de queries
- **CORS configurado** - Seguridad para peticiones cross-origin

### 🎨 Interfaz Moderna

- **Responsive** - Diseño adaptable mobile-first con Tailwind CSS
- **TypeScript** - Tipos estrictos para mayor robustez
- **Componentes reutilizables** - Arquitectura modular Vue 3
- **UX optimizada** - Feedback visual, validaciones en tiempo real
- **Dark Mode Ready** - Preparado para tema oscuro

---

## ☁️ Depsliegue en Producción

La aplicación está desplegada y operativa en Google Cloud Run:

- 🚀 **Frontend (App):** [https://matrixcalc-frontend-541716295092.us-central1.run.app](https://matrixcalc-frontend-541716295092.us-central1.run.app)
- 🔌 **Backend (API):** [https://matrixcalc-backend-772384307164.us-central1.run.app](https://matrixcalc-backend-772384307164.us-central1.run.app)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENTE (Navegador)                      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Vue.js 3 SPA (TypeScript)                │    │
│  │                                                     │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐ │    │
│  │  │  Components │  │   Stores    │  │  Router   │ │    │
│  │  │   (Views)   │  │   (Pinia)   │  │ (Vue Router)│ │    │
│  │  └─────────────┘  └─────────────┘  └───────────┘ │    │
│  │                                                     │    │
│  │  ┌─────────────────────────────────────────────┐  │    │
│  │  │       Composables (useMatrixAPI)            │  │    │
│  │  └─────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS (Axios)
                            │
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND (Servidor)                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Django 4.2 REST API                   │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────┐ │    │
│  │  │   ViewSets   │  │ Serializers  │  │  URLs   │ │    │
│  │  │   (CRUD)     │  │ (Validation) │  │(Routes) │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────┘ │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────────┐ │    │
│  │  │         Business Logic (Utils)               │ │    │
│  │  │  • matrix_model.py (NumPy/SciPy)             │ │    │
│  │  │  • exceptions.py (Custom errors)             │ │    │
│  │  │  • scheduler.py (Cleanup tasks)              │ │    │
│  │  └──────────────────────────────────────────────┘ │    │
│  │                                                     │    │
│  │  ┌─────────────┐  ┌──────────────────────────┐   │    │
│  │  │   Models    │  │  Management Commands     │   │    │
│  │  │ (ORM)       │  │  • export_backup         │   │    │
│  │  │             │  │  • import_backup         │   │    │
│  │  │             │  │  • cleanup_old_data      │   │    │
│  │  └─────────────┘  └──────────────────────────┘   │    │
│  │  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ ORM (Django)
                            │
┌─────────────────────────────────────────────────────────────┐
│                  BASE DE DATOS (PostgreSQL/SQLite)           │
│                                                              │
│  ┌────────────────┐          ┌────────────────┐            │
│  │  calculator_   │          │  calculator_   │            │
│  │    matrix      │ ◄─────── │   operation    │            │
│  │                │   FK     │                │            │
│  │  • id          │          │  • id          │            │
│  │  • name        │          │  • operation_  │            │
│  │  • rows        │          │    type        │            │
│  │  • cols        │          │  • matrix_a    │            │
│  │  • data (JSON) │          │  • matrix_b    │            │
│  │  • created_at  │          │  • result      │            │
│  │  • updated_at  │          │  • execution_  │            │
│  │                │          │    time        │            │
│  │  Índices:      │          │  • created_at  │            │
│  │  - created_at  │          │                │            │
│  │  - updated_at  │          │  Índices:      │            │
│  └────────────────┘          │  - operation_  │            │
│                              │    type        │            │
│                              │  - created_at  │            │
│                              │  - matrix_a    │            │
│                              │  - result      │            │
│                              └────────────────┘            │
│                              │  - extra_data  │            │
│                              └────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Flujo de Datos

1. **Cliente → Backend**: Usuario interactúa con Vue.js → Axios envía petición HTTP → Django recibe en ViewSet
2. **Backend → Lógica**: ViewSet valida con Serializer → Llama a utils/matrix_model.py (NumPy/SciPy) → Guarda en DB
3. **Backend → Cliente**: Serializa respuesta → Retorna JSON → Pinia actualiza estado → Vue re-renderiza

---

## 🚀 Instalación

### Con Docker (Recomendado)

**Requisitos**: Docker 20.10+ y Docker Compose 2.0+

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/Matrixcalc.git
cd Matrixcalc

# 2. Setup completo automático
make setup

# O manualmente:
cp .env.example .env
docker-compose build
docker-compose up -d
```

**Acceder a la aplicación:**

- 🌐 **Frontend**: http://localhost:3000
- 🔌 **API Backend**: http://localhost:8000/api
- 🔧 **Admin Django**: http://localhost:8000/admin (admin/admin123)

📖 Ver [DOCKER.md](./DOCKER.md) para documentación completa de Docker

### Desarrollo Local

#### Backend (Django)

```bash
# 1. Crear y activar entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements-web.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Iniciar servidor de desarrollo
python manage.py runserver
```

Backend disponible en: http://127.0.0.1:8000

#### Frontend (Vue.js)

```bash
cd frontend

# 1. Instalar dependencias
npm install

# 2. Configurar variables de entorno
cp .env.example .env
# VITE_API_URL=http://127.0.0.1:8000/api

# 3. Iniciar servidor de desarrollo
npm run dev
```

Frontend disponible en: http://localhost:5173

---

## 💻 Uso

### Interfaz Web

1. **Crear Matriz**
   - Ir a "Calculadora" → pestaña "Editor"
   - Especificar nombre y dimensiones
   - Rellenar valores manualmente o usar rellenos rápidos
   - Guardar

2. **Realizar Operación**
   - Pestaña "Operaciones"
   - Seleccionar matriz(ces) de los dropdowns
   - Elegir operación (suma, producto, inversa, SVD, etc.)
   - Ver resultado en pantalla (incluyendo descomposiciones complejas)

3. **Ver Estadísticas**
   - Ir a "Estadísticas"
   - Ver métricas generales y gráficos interactivos

4. **Backup/Restore**
   - Pestaña "Backup"
   - Exportar: descarga JSON con todas las matrices
   - Importar: subir archivo CSV con formato específico

### API REST

Ver documentación completa en [docs/API.md](./docs/API.md)

**Ejemplo: Crear matriz**

```bash
curl -X POST http://localhost:8000/api/matrices/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Matriz A",
    "rows": 2,
    "cols": 2,
    "data": [[1, 2], [3, 4]]
  }'
```

**Ejemplo: Sumar matrices**

```bash
curl -X POST http://localhost:8000/api/operations/sum/ \
  -H "Content-Type: application/json" \
  -d '{
    "matrix_a_id": 1,
    "matrix_b_id": 2
  }'
```

---

## 🛠️ Tecnologías

### Backend

- **Django 4.2** - Framework web Python
- **Django REST Framework** - API REST toolkit
- **PostgreSQL 15** - Base de datos relacional
- **NumPy & SciPy** - Cálculos matriciales y científicos avanzados
- **Gunicorn** - Servidor WSGI para producción
- **APScheduler** - Tareas programadas (limpieza)

### Frontend

- **Vue.js 3.5** - Framework JavaScript progresivo
- **TypeScript 5.7** - Superset tipado de JavaScript
- **Pinia** - State management
- **Vue Router** - Enrutamiento SPA
- **Tailwind CSS 4** - Framework CSS utility-first
- **Chart.js + vue-chartjs** - Visualización de datos
- **Axios** - Cliente HTTP

### DevOps

- **Docker + Docker Compose** - Contenedorización
- **Google Cloud Run** - Despliegue serverless escalable
- **Buildpacks / Dockerfile** - Estrategias de build

---

## 📚 Documentación

### 📖 Guías Principales

- **[Índice de Documentación](./docs/README.md)** - Navegación completa
- **[Guía de Deployment](./docs/deployment/README.md)** - Despliegue en producción
  - Google Cloud Run (recomendado)
  - Docker Compose
  - Servidor tradicional
- **[Troubleshooting](./docs/deployment/troubleshooting.md)** - Solución de problemas
- **[Guía de Testing](./docs/developer/testing.md)** - Ejecutar y escribir tests
- **[Migración v1→v2](./docs/migration/v1-to-v2.md)** - Migración Tkinter a Web

### 🔧 Para Desarrolladores

- **[Contribuir](./CONTRIBUTING.md)** - Guía de contribución
- **[API Documentation](./docs/API.md)** - Referencia de API REST
- **[Roadmap](./docs/ROADMAP.md)** - Hoja de ruta del proyecto

### 📦 Archivo Histórico

- **[v2.0 Docs](./docs/archive/v2.0/)** - Documentación histórica v2.0
- **[v3.0 Planning](./docs/archive/v3.0/)** - Planificación de mejoras v3.0

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](./CONTRIBUTING.md) para detalles sobre:

- Código de conducta
- Proceso de pull requests
- Estándares de código
- Flujo de desarrollo

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](./LICENSE) para más detalles.

---

## 📌 Versiones

### v3.0 (En Producción - Enero 2026)

- ✅ **Operaciones Avanzadas:** Rank, Eigenvalues, SVD, QR, Cholesky, LU.
- ✅ **Exportación LaTeX:** Múltiples formatos para documentos académicos.
- ✅ **UI Mejorada:** Atajos de teclado, animaciones fluidas, visualización de resultados complejos.
- ✅ **Documentación:** Consolidada y organizada.
- ✅ **Despliegue:** Cloud Run unificado (Frontend + Backend).

### v2.0 - Django Web Migration (Diciembre 2025)

- ✅ Migración completa de Tkinter a Django + Vue.js
- ✅ API REST con Django REST Framework
- ✅ Frontend moderno con Vue 3 + TypeScript
- ✅ Dashboard con estadísticas y gráficos
- ✅ Docker Compose con PostgreSQL
- ✅ Sistema de backup/restore
- ✅ Rate limiting y seguridad
- ✅ Dark mode completo
- ✅ Sistema de toasts y notificaciones

### v1.0 - Tkinter Desktop (Legacy - Archivado)

- GUI de escritorio con Tkinter
- Operaciones matriciales básicas
- Deprecado (código eliminado)

---

<div align="center">

**Desarrollado con ❤️ usando Django y Vue.js**

[⬆ Volver arriba](#-matrixcalc-web)

</div>
