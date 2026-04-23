# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a MatrixCalc! Este documento proporciona directrices para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Empezar](#cómo-empezar)
- [Flujo de Trabajo](#flujo-de-trabajo)
- [Estándares de Código](#estándares-de-código)
- [Commits](#commits)
- [Pull Requests](#pull-requests)
- [Testing](#testing)
- [Documentación](#documentación)

---

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta profesional y respetuoso:

- **Sé respetuoso**: Trata a todos con respeto y cortesía
- **Sé constructivo**: Las críticas deben ser constructivas y enfocadas en el código
- **Sé inclusivo**: Todos son bienvenidos sin importar experiencia, género, raza, religión, etc.
- **Sé profesional**: Mantén las discusiones enfocadas en el proyecto

---

## 🚀 Cómo Empezar

### 1. Fork y Clone

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/tu-usuario/Matrixcalc.git
cd Matrixcalc
```

### 2. Configurar Entorno de Desarrollo

#### Backend

```bash
# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar ESLint y Prettier
npm run lint
```

### 3. Crear Base de Datos de Desarrollo

```bash
# Opción 1: SQLite (más simple)
python manage.py migrate

# Opción 2: Docker PostgreSQL
docker-compose up -d db
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 4. Ejecutar en Modo Desarrollo

```bash
# Terminal 1: Backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend && npm run dev
```

---

## 🔄 Flujo de Trabajo

### 1. Crear una Rama

```bash
# Sincronizar con main
git checkout main
git pull origin main

# Crear rama descriptiva
git checkout -b feature/nueva-funcionalidad
# o
git checkout -b fix/correccion-bug
```

**Convenciones de nombres de ramas:**
- `feature/descripcion` - Nuevas funcionalidades
- `fix/descripcion` - Corrección de bugs
- `docs/descripcion` - Cambios en documentación
- `refactor/descripcion` - Refactorización de código
- `test/descripcion` - Añadir o mejorar tests
- `chore/descripcion` - Tareas de mantenimiento

### 2. Realizar Cambios

```bash
# Hacer cambios en el código

# Verificar que todo funciona
python manage.py test  # Backend
npm run test          # Frontend (cuando estén implementados)

# Verificar estilo de código
black .               # Backend
isort .               # Backend
npm run lint          # Frontend
```

### 3. Commit

```bash
git add .
git commit -m "feat: añadir validación de matriz singular"
```

Ver [Convenciones de Commits](#commits) abajo.

### 4. Push y Pull Request

```bash
git push origin feature/nueva-funcionalidad
```

Luego crea un Pull Request en GitHub.

---

## 📝 Estándares de Código

### Backend (Python/Django)

#### Estilo

- **PEP 8**: Seguir guía de estilo oficial de Python
- **Black**: Formateo automático con configuración por defecto
- **isort**: Ordenar imports alfabéticamente
- **Docstrings**: Documentar funciones y clases complejas

```python
def calcular_determinante(matriz: list[list[float]]) -> float:
    """
    Calcula el determinante de una matriz cuadrada.
    
    Args:
        matriz: Lista bidimensional representando la matriz
        
    Returns:
        float: El determinante de la matriz
        
    Raises:
        MatrizNoInvertibleError: Si la matriz no es cuadrada
    """
    # Implementación...
```

#### Organización

- **Modelos**: Un modelo por archivo cuando sea complejo
- **Serializers**: Agrupados por app en `serializers.py`
- **Views**: Usar ViewSets para CRUD, APIView para endpoints custom
- **Utils**: Funciones puras sin dependencias de Django

#### Buenas Prácticas

```python
# ✅ BIEN: Usar type hints
def validar_dimensiones(rows: int, cols: int) -> bool:
    return 0 < rows <= MAX_DIMENSION and 0 < cols <= MAX_DIMENSION

# ❌ MAL: Sin type hints
def validar_dimensiones(rows, cols):
    return 0 < rows <= MAX_DIMENSION and 0 < cols <= MAX_DIMENSION

# ✅ BIEN: Manejar errores específicos
try:
    resultado = calcular_inversa(matriz)
except MatrizNoInvertibleError as e:
    return Response({'error': str(e)}, status=400)

# ❌ MAL: Capturar todo
try:
    resultado = calcular_inversa(matriz)
except Exception as e:
    return Response({'error': str(e)}, status=500)
```

### Frontend (Vue.js/TypeScript)

#### Estilo

- **ESLint**: Configuración `@vue/eslint-config-typescript`
- **Prettier**: Formateo automático (2 espacios, single quotes)
- **Componentes**: Composition API con `<script setup lang="ts">`

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Matrix } from '@/types/matrix'

// Props con tipos
interface Props {
  matrix?: Matrix
  readonly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

// Emits tipados
interface Emits {
  (e: 'save', matrix: Matrix): void
  (e: 'cancel'): void
}

const emit = defineEmits<Emits>()

// Estado local
const loading = ref(false)
const error = ref<string | null>(null)

// Computados
const isValid = computed(() => {
  return props.matrix && props.matrix.rows > 0
})
</script>
```

#### Organización

```
src/
├── components/       # Componentes reutilizables
│   ├── MatrixEditor.vue
│   └── ResultViewer.vue
├── views/           # Vistas/páginas
│   ├── HomeView.vue
│   └── CalculatorView.vue
├── stores/          # Estado global (Pinia)
│   ├── matrixStore.ts
│   └── statsStore.ts
├── composables/     # Lógica reutilizable
│   └── useMatrixAPI.ts
├── types/           # Definiciones TypeScript
│   └── matrix.ts
└── router/          # Configuración de rutas
    └── index.ts
```

#### Buenas Prácticas

```typescript
// ✅ BIEN: Tipos explícitos
interface Matrix {
  id: number
  name: string
  rows: number
  cols: number
  data: number[][]
}

// ❌ MAL: Usar 'any'
const fetchMatrix = async (id: any): Promise<any> => {
  // ...
}

// ✅ BIEN: Manejar errores
const saveMatrix = async () => {
  try {
    loading.value = true
    error.value = null
    await matrixStore.createMatrix(matrixData)
    emit('saved')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Error desconocido'
  } finally {
    loading.value = false
  }
}

// ✅ BIEN: Desestructurar props reactivos
const { matrix, readonly } = toRefs(props)

// ❌ MAL: Acceder directamente a props en watchEffect
watchEffect(() => {
  console.log(props.matrix) // Pierde reactividad
})
```

---

## 💬 Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>(<scope>): <descripción>

[cuerpo opcional]

[footer opcional]
```

### Tipos

- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Formateo, puntos y comas, etc. (no afecta código)
- **refactor**: Refactorización sin cambiar funcionalidad
- **perf**: Mejoras de rendimiento
- **test**: Añadir o modificar tests
- **chore**: Tareas de mantenimiento (deps, build, etc.)

### Ejemplos

```bash
# Feature
git commit -m "feat(backend): añadir validación de matriz singular"
git commit -m "feat(frontend): implementar dark mode"

# Fix
git commit -m "fix(api): corregir cálculo de determinante para matrices 1x1"
git commit -m "fix(ui): resolver overflow en tabla de matrices grandes"

# Docs
git commit -m "docs: actualizar README con instrucciones Docker"

# Refactor
git commit -m "refactor(stores): extraer lógica de API a composable"

# Breaking change
git commit -m "feat(api)!: cambiar formato de respuesta de operaciones

BREAKING CHANGE: el campo 'result_matrix' ahora es 'result'"
```

---

## 🔍 Pull Requests

### Checklist antes de crear PR

- [ ] El código compila sin errores
- [ ] Los tests pasan (`python manage.py test` y `npm run test`)
- [ ] El código sigue los estándares de estilo (black, isort, eslint)
- [ ] Se añadió/actualizó documentación si es necesario
- [ ] Se añadieron tests para la nueva funcionalidad
- [ ] El commit message sigue Conventional Commits
- [ ] La rama está actualizada con `main`

### Plantilla de PR

```markdown
## 📝 Descripción

Breve descripción de los cambios realizados.

## 🎯 Tipo de Cambio

- [ ] 🐛 Bug fix
- [ ] ✨ Nueva funcionalidad
- [ ] 💥 Breaking change
- [ ] 📚 Documentación
- [ ] 🎨 Refactorización

## 🧪 ¿Cómo se ha probado?

Describe las pruebas que realizaste.

## 📸 Screenshots (si aplica)

Añade capturas de pantalla para cambios visuales.

## ✅ Checklist

- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado código complejo cuando es necesario
- [ ] He actualizado la documentación
- [ ] Mis cambios no generan nuevas advertencias
- [ ] He añadido tests que prueban mi fix/feature
- [ ] Los tests unitarios pasan localmente
```

### Proceso de Revisión

1. **Revisión automática**: CI/CD ejecuta tests y linters
2. **Revisión de código**: Al menos 1 aprobación requerida
3. **Correcciones**: Hacer cambios solicitados
4. **Merge**: Maintainer hace merge cuando está aprobado

---

## 🧪 Testing

### Backend (Django)

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos
python manage.py test calculator.tests.test_models
python manage.py test calculator.tests.test_views

# Con cobertura
coverage run --source='.' manage.py test
coverage report
coverage html  # Ver reporte en htmlcov/index.html
```

**Estructura de tests:**

```python
# calculator/tests/test_operations.py
from django.test import TestCase
from calculator.utils.matrix_model import MatrizModelo
from calculator.utils.exceptions import DimensionError

class MatrizSumaTestCase(TestCase):
    def setUp(self):
        self.matriz_a = MatrizModelo([[1, 2], [3, 4]])
        self.matriz_b = MatrizModelo([[5, 6], [7, 8]])
    
    def test_suma_correcta(self):
        """La suma de dos matrices debe devolver resultado correcto"""
        resultado = self.matriz_a + self.matriz_b
        self.assertEqual(resultado.obtener_matriz(), [[6, 8], [10, 12]])
    
    def test_suma_dimensiones_incompatibles(self):
        """Sumar matrices de diferentes dimensiones debe lanzar error"""
        matriz_c = MatrizModelo([[1, 2, 3]])
        with self.assertRaises(DimensionError):
            self.matriz_a + matriz_c
```

### Frontend (Vue/Vitest)

```bash
# Ejecutar tests (cuando estén implementados)
npm run test

# Tests en modo watch
npm run test:watch

# Cobertura
npm run test:coverage
```

**Estructura de tests:**

```typescript
// src/components/__tests__/MatrixEditor.spec.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import MatrixEditor from '@/components/MatrixEditor.vue'

describe('MatrixEditor', () => {
  it('renderiza correctamente con props por defecto', () => {
    const wrapper = mount(MatrixEditor)
    expect(wrapper.find('input[placeholder="Nombre de la matriz"]').exists()).toBe(true)
  })

  it('emite evento saved con datos correctos', async () => {
    const wrapper = mount(MatrixEditor)
    
    await wrapper.find('input[placeholder="Nombre"]').setValue('Matriz A')
    await wrapper.find('button[type="submit"]').trigger('click')
    
    expect(wrapper.emitted('saved')).toBeTruthy()
  })
})
```

---

## 📚 Documentación

### Documentar Código

- **Funciones complejas**: Añadir docstrings (Python) o JSDoc (TypeScript)
- **Componentes Vue**: Describir props, emits y slots en comentarios
- **API endpoints**: Documentar en `docs/API.md`

### Actualizar Documentación

Al añadir features, actualizar:

1. `README.md` - Características principales
2. `docs/API.md` - Nuevos endpoints
3. `docs/ROADMAP.md` - Completar items del roadmap
4. `CHANGELOG.md` - Añadir entrada en versión unreleased

### Ejemplo JSDoc

```typescript
/**
 * Ejecuta una operación matricial en el backend
 * 
 * @param operation - Tipo de operación a realizar
 * @param matrixAId - ID de la primera matriz
 * @param matrixBId - ID de la segunda matriz (opcional para operaciones unarias)
 * @returns Promise con el resultado de la operación
 * @throws Error si la operación falla o los parámetros son inválidos
 * 
 * @example
 * ```ts
 * const result = await performOperation('SUM', 1, 2)
 * console.log(result.result) // Matriz resultado
 * ```
 */
async function performOperation(
  operation: OperationType,
  matrixAId: number,
  matrixBId?: number
): Promise<Operation>
```

---

## 🆘 Ayuda y Soporte

- **Issues**: Abre un issue en GitHub para bugs o sugerencias
- **Discussions**: Usa GitHub Discussions para preguntas generales
- **Email**: Contacta a los maintainers (si está configurado)

---

## 🎉 Reconocimientos

Todos los contribuidores serán reconocidos en el archivo `CONTRIBUTORS.md` y en los release notes.

---

<div align="center">

**¡Gracias por contribuir a MatrixCalc!** 🙏

</div>
