# Testing & Coverage Guide

## 🧪 Infraestructura de Testing

Este proyecto cuenta con una infraestructura de testing completa para backend (Django/pytest) y frontend (Vue/Vitest).

## Backend Testing (Django + pytest)

### Dependencias Instaladas
- `pytest` 9.0.2
- `pytest-django` 4.11.1
- `pytest-cov` 7.0.0
- `factory-boy` 3.3.3
- `faker` 39.0.0

### Ejecutar Tests

```bash
# Tests básicos
python3 -m pytest

# Tests con coverage
python3 -m pytest --cov=calculator --cov-report=html --cov-report=term-missing --cov-report=xml -v

# Tests específicos
python3 -m pytest calculator/tests/test_models.py -v
```

### Estado Actual
- ✅ **12/12 tests pasando** en test_models.py (100%)
- 📊 **97% coverage** en calculator/models.py
- 📁 Reportes HTML en `htmlcov/index.html`
- 📄 Reportes XML en `coverage.xml` (para CI/CD)

### Archivos de Test
- `calculator/tests/conftest.py` - Fixtures y configuración
- `calculator/tests/test_models.py` - Tests de modelos (COMPLETO)
- `calculator/tests/test_serializers.py` - Tests de serializers (PENDIENTE)
- `calculator/tests/test_views.py` - Tests de views (PENDIENTE)

## Frontend Testing (Vue + Vitest)

### Dependencias Instaladas
- `@vitejs/plugin-vue` 5.2.1
- `@vue/test-utils` 2.4.6
- `vitest` 3.0.5
- `jsdom` 25.0.1
- `@vitest/coverage-v8` 4.0.16

### Ejecutar Tests

```bash
cd frontend

# Tests básicos
npm run test:unit

# Tests con coverage
npm run test:coverage

# Tests en modo watch
npm run test:unit -- --watch
```

### Estado Actual
- ✅ **32/37 tests pasando** (86.5%)
- 🔧 5 tests pendientes de corrección:
  - MatrixEditor: emits save event
  - OperationPanel: enables execute button (2 tests)
  - ResultViewer: displays execution time (2 tests)

### Archivos de Test
- `src/components/__tests__/` - Tests de componentes
  - ✅ MatrixEditor.spec.ts (8/9 pasando)
  - ✅ MatrixList.spec.ts (11/11 pasando)
  - ✅ OperationPanel.spec.ts (9/11 pasando)
  - ✅ ResultViewer.spec.ts (4/6 pasando)
- `src/composables/__tests__/` - Tests de composables
  - ✅ useMatrix.spec.ts (todas pasando)
  - ✅ useMatrixAPI.spec.ts (todas pasando)

## 📊 Reportes de Coverage

### Backend
- **Formato HTML**: `htmlcov/index.html` (abrir en navegador)
- **Formato XML**: `coverage.xml` (para integración CI/CD)
- **Terminal**: Se muestra automáticamente al ejecutar tests

### Frontend
- **Formato HTML**: `frontend/coverage/index.html`
- **Formato Terminal**: Se muestra al ejecutar `npm run test:coverage`

## 🎯 Próximos Pasos

### Backend
1. Completar tests de serializers (`test_serializers.py`)
2. Completar tests de views (`test_views.py`)
3. Agregar tests de utils (`test_matrix_model.py`)
4. Meta: **>80% coverage** en todo el backend

### Frontend
1. Corregir 5 tests pendientes
2. Agregar tests de stores
3. Agregar tests E2E con Cypress/Playwright
4. Meta: **100% de tests pasando**

## 🔧 Configuración

### pytest.ini
```ini
[pytest]
DJANGO_SETTINGS_MODULE = backend.settings
python_files = tests.py test_*.py *_tests.py
addopts = 
    --cov=calculator
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    -v
```

### vitest.config.ts
```typescript
export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html']
    }
  }
})
```

## 📝 Comandos Útiles

```bash
# Backend: Ver coverage específico
python3 -m pytest --cov=calculator.models --cov-report=term-missing

# Backend: Generar solo reporte HTML
python3 -m pytest --cov=calculator --cov-report=html

# Frontend: Tests de un archivo específico
npm run test:unit -- MatrixEditor.spec.ts

# Frontend: Tests en modo watch con coverage
npm run test:coverage -- --watch
```

## ✅ Checklist de Calidad

- [x] pytest-cov instalado y configurado
- [x] @vitest/coverage-v8 instalado
- [x] Tests de modelos backend (12/12)
- [x] Tests de componentes frontend (32/37)
- [x] Reportes HTML generados
- [ ] Tests de serializers backend
- [ ] Tests de views backend
- [ ] Tests de stores frontend
- [ ] Coverage >80% backend
- [ ] Tests 100% pasando frontend
