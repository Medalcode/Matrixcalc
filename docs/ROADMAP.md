# 🗺️ Roadmap - MatrixCalc

Hoja de ruta del proyecto con características implementadas y planeadas.

---

## ✅ Versión 2.0 - Web Migration (Actual)

### Backend
- [x] Django 4.2 con PostgreSQL
- [x] API REST con Django REST Framework
- [x] Modelos Matrix y Operation con JSONField
- [x] Serializers con validación robusta
- [x] ViewSets CRUD completos
- [x] Endpoints de operaciones (suma, resta, multiplicación, inversa, determinante, transpuesta)
- [x] Sistema de backup/restore (export_backup, import_backup)
- [x] Management commands para limpieza automática
- [x] Rate limiting (100 req/hora)
- [x] CORS configurado
- [x] Manejo de errores personalizado
- [x] Scheduler para tareas programadas
- [x] Importar/exportar CSV
- [x] Estadísticas completas

### Frontend
- [x] Vue.js 3.5 con TypeScript
- [x] Pinia para state management
- [x] Vue Router para navegación SPA
- [x] Tailwind CSS 4 para estilos
- [x] Componentes principales:
  - [x] MatrixEditor (editor interactivo)
  - [x] MatrixList (listado CRUD)
  - [x] OperationPanel (ejecutar operaciones)
  - [x] ResultViewer (visualizar resultados)
  - [x] BackupManager (import/export)
  - [x] DashboardStats (gráficos Chart.js)
- [x] Vistas:
  - [x] HomeView (landing page)
  - [x] CalculatorView (calculadora principal)
  - [x] StatsView (estadísticas)
  - [x] AboutView (información)
- [x] Composables para API (useMatrixAPI)
- [x] Tipos TypeScript completos
- [x] Dashboard con Chart.js (3 tipos de gráficos)

### DevOps
- [x] Docker Compose con PostgreSQL
- [x] Dockerfile backend multi-stage
- [x] Dockerfile frontend con Nginx
- [x] docker-compose.yml con healthchecks
- [x] docker-compose.dev.yml para desarrollo
- [x] Makefile con comandos útiles
- [x] Variables de entorno (.env.example)
- [x] Entrypoint script para backend
- [x] Nginx configurado con gzip y cache

### Documentación
- [x] README completo con arquitectura
- [x] DOCKER.md con guía de Docker
- [x] CONTRIBUTING.md con guía de contribución
- [x] docs/API.md con documentación de API
- [x] docs/ROADMAP.md (este archivo)

---

## 🚧 Versión 2.1 - Testing & Quality (Próximo)

### Testing
- [ ] Backend:
  - [ ] Tests unitarios con pytest-django
  - [ ] Tests de modelos (Matrix, Operation)
  - [ ] Tests de serializers
  - [ ] Tests de views/endpoints
  - [ ] Tests de utils (matrix_model, exceptions)
  - [ ] Coverage > 80%
- [ ] Frontend:
  - [ ] Tests unitarios con Vitest
  - [ ] Tests de componentes con Vue Test Utils
  - [ ] Tests de stores (Pinia)
  - [ ] Tests de composables
  - [ ] Coverage > 70%
- [ ] E2E:
  - [ ] Tests end-to-end con Playwright
  - [ ] Flujo completo: crear matriz → operar → ver resultado
  - [ ] Tests de regresión visual

### CI/CD
- [ ] GitHub Actions:
  - [ ] Workflow para tests backend
  - [ ] Workflow para tests frontend
  - [ ] Workflow para build Docker
  - [ ] Workflow para deployment
  - [ ] Code quality checks (linters)
  - [ ] Security scanning (Snyk, Dependabot)

### Quality Improvements
- [ ] Backend:
  - [ ] Logging estructurado (structlog)
  - [ ] Monitoring con Sentry
  - [ ] Prometheus metrics
  - [ ] Pre-commit hooks (black, isort, flake8)
- [ ] Frontend:
  - [ ] Pre-commit hooks (ESLint, Prettier)
  - [ ] Bundle analysis
  - [ ] Performance monitoring

---

## 🎯 Versión 2.2 - Enhanced Features

### Autenticación & Autorización
- [ ] Sistema de usuarios con Django Auth
- [ ] JWT tokens para API
- [ ] Login/Register en frontend
- [ ] Protección de endpoints
- [ ] Roles (admin, user)
- [ ] Matrices privadas/públicas

### Features Backend
- [ ] Websockets para operaciones en tiempo real
- [ ] Queue de operaciones pesadas (Celery + Redis)
- [ ] Cache con Redis para queries frecuentes
- [ ] Versionado de matrices
- [ ] Tags y categorías para matrices
- [ ] Búsqueda full-text
- [ ] Filtros avanzados (dimensiones, fechas, tags)

### Features Frontend
- [ ] Dark mode completo
- [ ] Internacionalización (i18n) - Español/Inglés
- [ ] Editor de matrices mejorado:
  - [ ] Arrastrar y soltar para reordenar filas/columnas
  - [ ] Copiar/pegar desde Excel
  - [ ] Atajos de teclado
  - [ ] Autocompletado
- [ ] Visualización avanzada:
  - [ ] Heatmap de matrices
  - [ ] 3D plots para matrices grandes
  - [ ] Animaciones de operaciones
- [ ] Exportar reportes PDF
- [ ] Modo offline con Service Workers (PWA)

### Operaciones Avanzadas
- [ ] Descomposición LU
- [ ] Descomposición QR
- [ ] Valores y vectores propios (eigenvalues/eigenvectors)
- [ ] Factorización de Cholesky
- [ ] Normas de matrices (Frobenius, infinito)
- [ ] Rango de matriz
- [ ] Traza de matriz
- [ ] Producto de Kronecker
- [ ] Pseudoinversa (Moore-Penrose)

---

## 🚀 Versión 3.0 - Advanced Platform

### Machine Learning Integration
- [ ] Operaciones de álgebra lineal para ML:
  - [ ] PCA (Principal Component Analysis)
  - [ ] SVD (Singular Value Decomposition)
  - [ ] Gradient descent visualization
- [ ] Datasets de ejemplo (MNIST, etc.)
- [ ] Integración con TensorFlow/PyTorch para operaciones GPU

### Collaboration
- [ ] Compartir matrices con otros usuarios
- [ ] Comentarios y discusiones en matrices
- [ ] Workspaces colaborativos
- [ ] Control de versiones tipo Git
- [ ] Merge/diff de matrices

### Performance
- [ ] Procesamiento paralelo para operaciones grandes
- [ ] Soporte para matrices sparse (scipy.sparse)
- [ ] Paginación de matrices muy grandes
- [ ] Compresión de datos almacenados
- [ ] CDN para assets estáticos

### Mobile
- [ ] Progressive Web App (PWA)
- [ ] Aplicación móvil con React Native / Flutter
- [ ] Gestos táctiles optimizados
- [ ] Modo landscape para matrices grandes

---

## 💭 Ideas Futuras (No Planeadas)

- Plugin system para operaciones custom
- Marketplace de matrices (plantillas, datasets)
- API GraphQL además de REST
- Jupyter Notebook integration
- LaTeX export para documentos académicos
- CLI tool para operaciones batch
- Embedded widgets para sitios web
- Integración con Wolfram Alpha / SymPy
- Realidad Aumentada para visualización 3D

---

## 📊 Métricas de Progreso

### Versión 2.0 ✅
```
Progress: ████████████████████ 100%
```
- Backend: 100%
- Frontend: 100%
- DevOps: 100%
- Documentation: 100%

### Versión 2.1 🚧
```
Progress: ░░░░░░░░░░░░░░░░░░░░ 0%
```
- Testing: 0%
- CI/CD: 0%
- Quality: 0%

### Overall Project
```
Progress: ████████░░░░░░░░░░░░ 40%
```

---

## 🤝 Contribuir al Roadmap

Si tienes ideas o quieres trabajar en alguna feature:

1. **Abre un Issue** en GitHub con la etiqueta `enhancement`
2. **Discute la propuesta** con los maintainers
3. **Crea un PR** con la implementación
4. **Actualiza este roadmap** al completar la feature

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para más detalles.

---

## 📅 Timeline Estimado

| Versión | Release Estimado | Estado |
|---------|-----------------|---------|
| v2.0    | Q4 2025        | ✅ Completo |
| v2.1    | Q1 2026        | 🚧 Planeado |
| v2.2    | Q2 2026        | 📋 Planeado |
| v3.0    | Q4 2026        | 💭 Futuro |

---

## 🔗 Enlaces

- [Volver al README](../README.md)
- [Documentación de API](./API.md)
- [Guía de Docker](../DOCKER.md)
- [Guía de Contribución](../CONTRIBUTING.md)

---

<div align="center">

**MatrixCalc - Building the future of matrix calculations** 🚀

Última actualización: 21 de diciembre de 2025

</div>
