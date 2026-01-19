# 🚀 Guía Completa de Migración MatrixCalc a Django + Vue.js 3

## Estado Actual

### ✅ Completado
- ✓ Branch `django-migration` creado
- ✓ Tag `v1.0-tkinter-desktop` para preservar versión original
- ✓ Proyecto Django inicializado
- ✓ Modelos Matrix y Operation creados
- ✓ Lógica numérica migrada a `calculator/utils/`
- ✓ Serializers implementados
- ✓ Script de automatización completo creado

### 📋 Pendiente de Ejecutar
- [ ] Ejecutar script `complete_migration.sh`
- [ ] Completar views.py manualmente
- [ ] Crear componentes Vue
- [ ] Crear documentación final

---

## 🎯 Ejecución Rápida

### Opción 1: Script Automático (Recomendado)

```bash
# Ejecutar desde el directorio del proyecto
cd /home/medalcode/Documentos/GitHub/Matrixcalc
./complete_migration.sh
```

Este script ejecutará automáticamente:
1. ✓ Exception handlers
2. ✓ URLs de calculator y proyecto  
3. ✓ Django Admin
4. ✓ APScheduler en apps.py
5. ✓ Management commands (cleanup, export_backup, import_backup)
6. ✓ Migrations
7. ✓ Inicialización frontend Vue
8. ✓ Configuración Docker completa
9. ✓ .gitignore actualizado

### Opción 2: Manual Step-by-Step

Si prefieres ejecutar paso a paso:

#### 1. Completar views.py

El archivo `calculator/views.py` necesita ser completado. Crea el archivo completo usando:

```bash
# El contenido completo está preparado en el script
# O usa el código que te proporcioné anteriormente en la conversación
```

#### 2. Ejecutar secciones del script

Puedes ejecutar secciones individuales del script copiando los bloques relevantes.

---

## 📦 Componentes Vue Principales a Crear

### Estructura de Directorios Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── MatrixEditor.vue       # Editor de matriz con grilla
│   │   ├── MatrixList.vue         # Lista de matrices guardadas
│   │   ├── OperationPanel.vue     # Botones de operaciones
│   │   ├── ResultViewer.vue       # Visualizador de resultados
│   │   ├── HistoryPanel.vue       # Historial de operaciones
│   │   ├── BackupManager.vue      # Gestión de backups
│   │   └── DashboardStats.vue     # Dashboard con Chart.js
│   ├── stores/
│   │   ├── matrixStore.ts         # Store Pinia para matrices
│   │   └── statsStore.ts          # Store Pinia para stats
│   ├── composables/
│   │   └── useMatrixAPI.ts        # API calls con axios
│   ├── types/
│   │   └── matrix.ts              # TypeScript interfaces
│   ├── router/
│   │   └── index.ts               # Vue Router config
│   ├── views/
│   │   ├── HomeView.vue           # Vista principal
│   │   ├── HistoryView.vue        # Vista historial
│   │   ├── StatsView.vue          # Vista estadísticas
│   │   └── BackupView.vue         # Vista backup/restore
│   └── App.vue                    # App principal
```

### Plantillas de Componentes

#### MatrixEditor.vue (Ejemplo Básico)

```vue
<template>
  <div class="card">
    <h3 class="text-lg font-semibold mb-4">Editor de Matriz</h3>
    
    <div class="flex gap-4 mb-4">
      <div>
        <label class="block text-sm font-medium">Filas</label>
        <input v-model.number="rows" type="number" min="1" max="100" class="input-field w-20">
      </div>
      <div>
        <label class="block text-sm font-medium">Columnas</label>
        <input v-model.number="cols" type="number" min="1" max="100" class="input-field w-20">
      </div>
      <button @click="resize" class="btn-primary self-end">Redimensionar</button>
    </div>
    
    <div class="overflow-auto max-h-96">
      <table class="min-w-full border-collapse">
        <tbody>
          <tr v-for="(row, i) in cells" :key="i">
            <td v-for="(cell, j) in row" :key="j" class="p-1">
              <input 
                v-model.number="cells[i][j]"
                type="number"
                step="any"
                :class="{'bg-red-100': !isValidCell(i, j)}"
                class="w-16 px-2 py-1 border rounded text-center"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="mt-4 flex gap-2">
      <button @click="clear" class="btn-secondary">Limpiar</button>
      <button @click="importCSV" class="btn-secondary">Importar CSV</button>
      <input ref="fileInput" type="file" accept=".csv" class="hidden" @change="handleFileUpload">
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const rows = ref(3)
const cols = ref(3)
const cells = reactive<number[][]>([])
const fileInput = ref<HTMLInputElement>()

const resize = () => {
  cells.length = 0
  for (let i = 0; i < rows.value; i++) {
    cells.push(Array(cols.value).fill(0))
  }
}

const clear = () => {
  cells.forEach(row => row.fill(0))
}

const isValidCell = (i: number, j: number) => {
  return !isNaN(cells[i][j])
}

const importCSV = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    // TODO: Implementar lectura de CSV
  }
}

// Inicializar
resize()
</script>
```

---

## 🐳 Docker: Guía de Uso

### Desarrollo Local (Sin Docker)

```bash
# Terminal 1: Backend
source venv_django/bin/activate
python manage.py runserver

# Terminal 2: Frontend  
cd frontend
npm run dev
```

Abrir: http://localhost:5173 (Vite dev server con proxy a Django)

### Producción Local (Con Docker)

```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener
docker-compose down
```

Abrir: http://localhost:8000

### Red Local (Acceso desde otros dispositivos)

```bash
# Habilitar acceso en red local
cp docker-compose.override.yml.example docker-compose.override.yml

# Reiniciar
docker-compose down
docker-compose up -d

# Encontrar tu IP
ip addr show  # Linux
# o
ipconfig  # Windows

# Desde otro dispositivo: http://192.168.X.X:8000
```

⚠️ **Advertencia**: Solo usar en redes confiables. Sin autenticación.

---

## 🧪 Testing

### Backend (pytest-django)

```bash
# Instalar dependencias de test
pip install pytest pytest-django pytest-cov

# Ejecutar tests
pytest

# Con coverage
pytest --cov=calculator --cov-report=html
```

### Frontend (Vitest)

```bash
cd frontend

# Tests unitarios
npm run test:unit

# Coverage
npm run test:unit -- --coverage
```

### E2E (Playwright)

```bash
cd frontend

# Instalar Playwright
npm create playwright@latest

# Ejecutar tests e2e
npx playwright test
```

---

## 📊 Management Commands

### Limpieza de Datos

```bash
# Ver qué se eliminaría (dry-run)
python manage.py cleanup_old_data --dry-run

# Ejecutar limpieza (30 días por defecto)
python manage.py cleanup_old_data

# Personalizar días de retención
python manage.py cleanup_old_data --days 60
```

### Backup/Restore

```bash
# Exportar backup
python manage.py export_backup

# Con ruta personalizada
python manage.py export_backup --output /tmp/mi_backup.json

# Importar backup
python manage.py import_backup backups/backup_20251221_120000.json

# Importar eliminando datos existentes
python manage.py import_backup backups/backup_XXX.json --clear
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env`:

```bash
cp .env.example .env
nano .env
```

Personalizar:
- `SECRET_KEY`: Clave secreta Django (generar nueva en producción)
- `DB_PASSWORD`: Password PostgreSQL
- `MAX_DIMENSION`: Dimensión máxima de matrices (default: 100)
- `RETENTION_DAYS`: Días de retención de datos (default: 30)
- `CONDITION_THRESHOLD`: Umbral número de condición (default: 1e12)

### Configuración PostgreSQL Local

Si prefieres PostgreSQL local en lugar de Docker:

```bash
# Instalar PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Crear base de datos y usuario
sudo -u postgres psql
CREATE DATABASE matrixcalc;
CREATE USER matrixcalc WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE matrixcalc TO matrixcalc;
\q

# Configurar DATABASE_URL en .env
DATABASE_URL=postgresql://matrixcalc:tu_password@localhost:5432/matrixcalc
```

---

## 📝 Checklist de Tareas Pendientes

### Backend
- [x] Modelos Django
- [x] Serializers
- [ ] Views completo (80% hecho - ver script)
- [x] URLs
- [x] Admin
- [x] Management commands
- [x] Exception handlers
- [x] APScheduler
- [ ] Tests API
- [ ] Tests modelos

### Frontend
- [ ] Crear componentes Vue (6 componentes principales)
- [ ] Stores Pinia (matrixStore, statsStore)
- [ ] API composable
- [ ] Router con 4 vistas
- [ ] Types TypeScript
- [ ] Tests unitarios
- [ ] Tests e2e

### DevOps
- [x] Dockerfile
- [x] docker-compose.yml
- [x] .dockerignore
- [x] entrypoint.sh
- [x] .env.example
- [x] docker-compose.override.yml.example
- [ ] CI/CD (.github/workflows/ci.yml)

### Documentación
- [ ] README.md nuevo (reemplazar actual)
- [ ] CONTRIBUTING.md
- [ ] docs/API.md
- [ ] docs/ROADMAP.md
- [ ] .github/PULL_REQUEST_TEMPLATE.md

---

## 🚨 Troubleshooting

### Error: Puerto 8000 ocupado

```bash
# Encontrar proceso
sudo lsof -i :8000

# Matar proceso
kill -9 <PID>
```

### Error: PostgreSQL connection refused

```bash
# Verificar PostgreSQL corriendo
docker-compose ps

# Ver logs
docker-compose logs db

# Reiniciar servicio
docker-compose restart db
```

### Error: npm dependencies

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Error: Django migrations

```bash
# Eliminar migrations (cuidado en producción)
find calculator/migrations -name "*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Vue.js 3: https://vuejs.org/
- Pinia: https://pinia.vuejs.org/
- Chart.js: https://www.chartjs.org/
- Tailwind CSS: https://tailwindcss.com/

### Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /api/matrices/ | Listar matrices |
| POST | /api/matrices/ | Crear matriz |
| GET | /api/matrices/{id}/ | Detalle matriz |
| PUT/PATCH | /api/matrices/{id}/ | Actualizar matriz |
| DELETE | /api/matrices/{id}/ | Eliminar matriz |
| GET | /api/matrices/{id}/export_csv/ | Exportar CSV |
| GET | /api/matrices/{id}/export_json/ | Exportar JSON |
| POST | /api/matrices/import_csv/ | Importar CSV |
| GET | /api/operations/ | Listar operaciones |
| POST | /api/operations/sum/ | Sumar matrices |
| POST | /api/operations/subtract/ | Restar matrices |
| POST | /api/operations/multiply/ | Multiplicar matrices |
| POST | /api/operations/inverse/ | Calcular inversa |
| POST | /api/operations/determinant/ | Calcular determinante |
| POST | /api/operations/transpose/ | Calcular transpuesta |
| GET | /api/stats/ | Estadísticas sistema |

---

## 🎉 Próximos Pasos

1. **Ejecutar script de migración**: `./complete_migration.sh`
2. **Completar views.py**: Reemplazar contenido con código completo
3. **Crear componentes Vue**: Usar plantillas de esta guía
4. **Probar localmente**: Sin Docker primero
5. **Probar con Docker**: Verificar deployment
6. **Crear tests**: Backend y frontend
7. **Documentar API**: Completar docs/
8. **PR a main**: Cuando todo funcione

---

**¿Preguntas? ¿Errores?** Revisa la sección Troubleshooting o consulta los logs:
```bash
# Django logs
python manage.py runserver --verbosity 3

# Docker logs
docker-compose logs -f

# Frontend logs  
cd frontend && npm run dev
```

¡Buena suerte con la migración! 🚀
