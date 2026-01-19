#!/bin/bash
# Script de migración completa MatrixCalc a Django + Vue.js 3
# Ejecuta todos los pasos restantes de forma automatizada

set -e  # Salir si hay error

echo "🚀 Iniciando migración completa de MatrixCalc a Django + Vue.js 3"
echo "================================================================"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorio base
BASE_DIR="/home/medalcode/Documentos/GitHub/Matrixcalc"
cd "$BASE_DIR"

# Activar entorno virtual
echo -e "${BLUE}📦 Activando entorno virtual...${NC}"
source venv_django/bin/activate

# ============================================================================
# PASO 1: Completar backend Django
# ============================================================================
echo -e "\n${GREEN}✓ PASO 1: Completando backend Django${NC}"

# 1.1 Crear exception handler
echo "  → Creando exception handler..."
cat > calculator/utils/exception_handlers.py << 'HANDLER_EOF'
"""
Exception handlers personalizados para la API REST.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from calculator.utils.exceptions import InvalidMatrixError, NumericError


def custom_exception_handler(exc, context):
    """
    Exception handler personalizado que mapea excepciones del modelo
    a respuestas HTTP apropiadas.
    """
    # Llamar al handler por defecto de DRF primero
    response = exception_handler(exc, context)
    
    # Si DRF no manejó la excepción, manejar excepciones personalizadas
    if response is None:
        if isinstance(exc, InvalidMatrixError):
            return Response(
                {
                    'error': 'invalid_matrix',
                    'detail': str(exc)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif isinstance(exc, NumericError):
            return Response(
                {
                    'error': 'numeric_error',
                    'detail': str(exc)
                },
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
    
    return response
HANDLER_EOF

# 1.2 Crear URLs de calculator
echo "  → Configurando URLs de calculator..."
cat > calculator/urls.py << 'URLS_EOF'
"""
URLs para la app calculator.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from calculator import views

# Router para ViewSets
router = DefaultRouter()
router.register(r'matrices', views.MatrixViewSet, basename='matrix')
router.register(r'operations', views.OperationViewSet, basename='operation')

# URLs de operaciones y stats
urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
    
    # Operaciones matriciales
    path('operations/sum/', views.sum_matrices, name='sum-matrices'),
    path('operations/subtract/', views.subtract_matrices, name='subtract-matrices'),
    path('operations/multiply/', views.multiply_matrices, name='multiply-matrices'),
    path('operations/inverse/', views.inverse_matrix, name='inverse-matrix'),
    path('operations/determinant/', views.determinant_matrix, name='determinant-matrix'),
    path('operations/transpose/', views.transpose_matrix, name='transpose-matrix'),
    
    # Estadísticas
    path('stats/', views.stats_view, name='stats'),
    
    # Backup/Restore (se agregarán después)
    # path('backup/export/', views.export_backup_view, name='export-backup'),
    # path('backup/import/', views.import_backup_view, name='import-backup'),
    # path('backup/list/', views.list_backups_view, name='list-backups'),
]
URLS_EOF

# 1.3 Actualizar URLs del proyecto
echo "  → Actualizando URLs del proyecto..."
cat > matrixcalc_web/urls.py << 'PROJECT_URLS_EOF'
"""
URLs del proyecto matrixcalc_web.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('calculator.urls')),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
PROJECT_URLS_EOF

# 1.4 Crear admin.py
echo "  → Configurando Django Admin..."
cat > calculator/admin.py << 'ADMIN_EOF'
"""
Configuración del Django Admin para calculator.
"""
from django.contrib import admin
from calculator.models import Matrix, Operation


@admin.register(Matrix)
class MatrixAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dimensions', 'created_at']
    list_filter = ['created_at', 'rows', 'cols']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'operation_type', 'matrix_a', 'matrix_b', 'created_at', 'execution_time_ms']
    list_filter = ['operation_type', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('matrix_a', 'matrix_b', 'result')
ADMIN_EOF

# 1.5 Actualizar apps.py con scheduler
echo "  → Configurando APScheduler..."
cat > calculator/apps.py << 'APPS_EOF'
"""
Configuración de la app calculator.
"""
import os
from django.apps import AppConfig


class CalculatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculator'
    verbose_name = 'Matrix Calculator'
    
    def ready(self):
        """
        Código que se ejecuta cuando la app está lista.
        Configura el scheduler para tareas programadas.
        """
        # Solo ejecutar scheduler si está habilitado y no en runserver reload
        if os.environ.get('RUN_SCHEDULER') == 'true' and not os.environ.get('RUN_MAIN'):
            self.start_scheduler()
    
    def start_scheduler(self):
        """Inicia el scheduler para tareas programadas."""
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger
        from django.core.management import call_command
        import logging
        
        logger = logging.getLogger(__name__)
        
        def cleanup_task():
            """Tarea de limpieza programada."""
            try:
                logger.info("Ejecutando limpieza automática...")
                call_command('cleanup_old_data')
                logger.info("Limpieza completada exitosamente")
            except Exception as e:
                logger.error(f"Error en limpieza automática: {e}")
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            cleanup_task,
            trigger=CronTrigger(hour=2, minute=0),  # 2:00 AM diario
            id='cleanup_old_data',
            name='Limpieza automática de datos antiguos',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Scheduler iniciado: limpieza diaria a las 2:00 AM")
        
        # TODO v2.0: Agregar job para broadcast de stats via WebSocket
APPS_EOF

# 1.6 Crear management commands
echo "  → Creando management commands..."
mkdir -p calculator/management/commands

cat > calculator/management/__init__.py << 'EOF'
EOF

cat > calculator/management/commands/__init__.py << 'EOF'
EOF

# Command: cleanup_old_data
cat > calculator/management/commands/cleanup_old_data.py << 'CLEANUP_EOF'
"""
Management command para limpiar datos antiguos.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from datetime import timedelta
from calculator.models import Matrix, Operation
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Limpia operaciones y matrices antiguas según RETENTION_DAYS'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            help='Días de retención (sobrescribe configuración)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simula la limpieza sin eliminar datos',
        )
    
    def handle(self, *args, **options):
        days = options.get('days') or settings.MATRIX_CONFIG['RETENTION_DAYS']
        dry_run = options.get('dry_run', False)
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        self.stdout.write(
            self.style.WARNING(f"Limpiando datos anteriores a {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        )
        
        if dry_run:
            self.stdout.write(self.style.NOTICE("Modo DRY RUN - No se eliminarán datos"))
        
        # Auto-backup antes de eliminar (solo si no es dry-run)
        if not dry_run:
            try:
                from django.core.management import call_command
                self.stdout.write("Creando backup automático...")
                call_command('export_backup')
                self.stdout.write(self.style.SUCCESS("✓ Backup creado"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al crear backup: {e}"))
                self.stdout.write(self.style.WARNING("Continuando sin backup..."))
        
        # Contar operaciones a eliminar
        operations_to_delete = Operation.objects.filter(created_at__lt=cutoff_date)
        op_count = operations_to_delete.count()
        
        # Contar matrices huérfanas a eliminar
        matrices_to_delete = Matrix.objects.filter(
            Q(operations_as_a__isnull=True) &
            Q(operations_as_b__isnull=True) &
            Q(operations_as_result__isnull=True) &
            Q(created_at__lt=cutoff_date)
        )
        matrix_count = matrices_to_delete.count()
        
        self.stdout.write(f"Operaciones a eliminar: {op_count}")
        self.stdout.write(f"Matrices huérfanas a eliminar: {matrix_count}")
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS("Simulación completada"))
            return
        
        # Eliminar con transacción
        try:
            with transaction.atomic():
                # Eliminar operaciones (cascade eliminará relaciones)
                deleted_ops = operations_to_delete.delete()
                
                # Eliminar matrices huérfanas
                deleted_matrices = matrices_to_delete.delete()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Eliminadas {deleted_ops[0]} operaciones y {deleted_matrices[0]} matrices"
                    )
                )
                
                logger.info(f"Limpieza completada: {deleted_ops[0]} ops, {deleted_matrices[0]} matrices")
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante limpieza: {e}"))
            logger.error(f"Error en limpieza: {e}")
            raise
CLEANUP_EOF

# Command: export_backup
cat > calculator/management/commands/export_backup.py << 'EXPORT_EOF'
"""
Management command para exportar backup completo.
"""
import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.utils import timezone
from django.conf import settings
from calculator.models import Matrix, Operation


class Command(BaseCommand):
    help = 'Exporta todas las matrices y operaciones a JSON'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Ruta del archivo de salida',
        )
    
    def handle(self, *args, **options):
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        output_path = options.get('output') or settings.BACKUP_DIR / f'backup_{timestamp}.json'
        
        self.stdout.write(f"Exportando backup a: {output_path}")
        
        # Serializar modelos
        matrices = Matrix.objects.all().order_by('id')
        operations = Operation.objects.all().select_related(
            'matrix_a', 'matrix_b', 'result'
        ).order_by('id')
        
        matrices_data = json.loads(serializers.serialize('json', matrices))
        operations_data = json.loads(serializers.serialize('json', operations))
        
        # Estructura del backup
        backup_data = {
            'version': '2.0',
            'timestamp': timezone.now().isoformat(),
            'database': 'postgresql',
            'total_matrices': len(matrices_data),
            'total_operations': len(operations_data),
            'matrices': matrices_data,
            'operations': operations_data
        }
        
        # Guardar a archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"✓ Backup exportado: {len(matrices_data)} matrices, {len(operations_data)} operaciones"
            )
        )
        self.stdout.write(f"Archivo: {output_path}")
EXPORT_EOF

# Command: import_backup
cat > calculator/management/commands/import_backup.py << 'IMPORT_EOF'
"""
Management command para importar backup.
"""
import json
from django.core.management.base import BaseCommand
from django.core import serializers
from django.db import transaction


class Command(BaseCommand):
    help = 'Importa matrices y operaciones desde backup JSON'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Ruta del archivo de backup a importar',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Eliminar datos existentes antes de importar',
        )
    
    def handle(self, *args, **options):
        backup_file = options['backup_file']
        clear_existing = options.get('clear', False)
        
        self.stdout.write(f"Importando backup desde: {backup_file}")
        
        # Leer archivo
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Archivo no encontrado: {backup_file}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"Error al parsear JSON: {e}"))
            return
        
        # Validar versión
        version = backup_data.get('version', '1.0')
        if float(version) < 2.0:
            self.stdout.write(self.style.WARNING(f"Versión de backup antigua: {version}"))
        
        matrices_data = backup_data.get('matrices', [])
        operations_data = backup_data.get('operations', [])
        
        self.stdout.write(f"Matrices en backup: {len(matrices_data)}")
        self.stdout.write(f"Operaciones en backup: {len(operations_data)}")
        
        # Importar con transacción
        try:
            with transaction.atomic():
                if clear_existing:
                    from calculator.models import Matrix, Operation
                    self.stdout.write(self.style.WARNING("Eliminando datos existentes..."))
                    Operation.objects.all().delete()
                    Matrix.objects.all().delete()
                
                # Deserializar matrices
                self.stdout.write("Importando matrices...")
                matrices_json = json.dumps(matrices_data)
                for obj in serializers.deserialize('json', matrices_json):
                    obj.save()
                
                # Deserializar operaciones
                self.stdout.write("Importando operaciones...")
                operations_json = json.dumps(operations_data)
                for obj in serializers.deserialize('json', operations_json):
                    obj.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Importación completada: {len(matrices_data)} matrices, {len(operations_data)} operaciones"
                    )
                )
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error durante importación: {e}"))
            raise
IMPORT_EOF

# 1.7 Crear migrations
echo "  → Creando migrations..."
python manage.py makemigrations calculator

echo "  → Aplicando migrations..."
python manage.py migrate

echo -e "${GREEN}✓ Backend Django completado${NC}"

# ============================================================================
# PASO 2: Inicializar Frontend Vue.js 3
# ============================================================================
echo -e "\n${GREEN}✓ PASO 2: Inicializando Frontend Vue.js 3${NC}"

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ Node.js no encontrado. Instálalo primero.${NC}"
    exit 1
fi

echo "  → Creando proyecto Vue..."
# Crear proyecto Vue con configuración predefinida
npm create vue@latest frontend -- --typescript --router pinia --vitest

cd frontend

echo "  → Instalando dependencias..."
npm install axios tailwindcss @tailwindcss/forms postcss autoprefixer chart.js vue-chartjs vue-i18n@9

echo "  → Configurando Tailwind CSS..."
npx tailwindcss init -p

# Configurar tailwind.config.js
cat > tailwind.config.js << 'TAILWIND_EOF'
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        }
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
TAILWIND_EOF

# Crear archivo CSS con Tailwind
cat > src/assets/main.css << 'CSS_EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200;
  }
  
  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition duration-200;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
  
  .input-field {
    @apply mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500;
  }
}
CSS_EOF

# Actualizar vite.config.ts
cat > vite.config.ts << 'VITE_EOF'
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    outDir: '../calculator/static/calculator/dist',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
VITE_EOF

cd "$BASE_DIR"

echo -e "${GREEN}✓ Frontend Vue.js 3 inicializado${NC}"

# ============================================================================
# PASO 3: Configurar Docker
# ============================================================================
echo -e "\n${GREEN}✓ PASO 3: Configurando Docker${NC}"

# Crear Dockerfile
cat > Dockerfile << 'DOCKERFILE_EOF'
# Multi-stage build para MatrixCalc Web

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Python application
FROM python:3.11-slim
LABEL maintainer="MatrixCalc Team"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt

# Copiar código de la aplicación
COPY . .

# Copiar frontend compilado
COPY --from=frontend-builder /frontend/dist ./calculator/static/calculator/dist/

# Crear directorios necesarios
RUN mkdir -p backups data staticfiles

# Collectstatic
RUN python manage.py collectstatic --noinput --clear

# Exponer puerto
EXPOSE 8000

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
DOCKERFILE_EOF

# Crear entrypoint.sh
cat > entrypoint.sh << 'ENTRYPOINT_EOF'
#!/bin/bash
set -e

echo "Esperando PostgreSQL..."
until pg_isready -h db -U matrixcalc; do
  sleep 1
done

echo "PostgreSQL listo!"

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Ejecutando limpieza de datos antiguos..."
python manage.py cleanup_old_data --days ${RETENTION_DAYS:-30} || true

echo "Iniciando servidor Gunicorn..."
exec gunicorn matrixcalc_web.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
ENTRYPOINT_EOF

chmod +x entrypoint.sh

# Crear docker-compose.yml
cat > docker-compose.yml << 'COMPOSE_EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: matrixcalc
      POSTGRES_USER: matrixcalc
      POSTGRES_PASSWORD: ${DB_PASSWORD:-changeme123}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U matrixcalc"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - matrixcalc_network

  web:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      DATABASE_URL: postgresql://matrixcalc:${DB_PASSWORD:-changeme123}@db:5432/matrixcalc
      DEBUG: "False"
      ALLOWED_HOSTS: "localhost,127.0.0.1"
      SECRET_KEY: ${SECRET_KEY:-changeme-secret-key-production}
      RUN_SCHEDULER: "true"
      MAX_DIMENSION: ${MAX_DIMENSION:-100}
      RETENTION_DAYS: ${RETENTION_DAYS:-30}
    volumes:
      - ./backups:/app/backups
    networks:
      - matrixcalc_network

volumes:
  postgres_data:

networks:
  matrixcalc_network:
    driver: bridge
COMPOSE_EOF

# Crear docker-compose.override.yml.example
cat > docker-compose.override.yml.example << 'OVERRIDE_EOF'
# Archivo de ejemplo para configuración de red local
# Para usar: cp docker-compose.override.yml.example docker-compose.override.yml
# Luego ejecuta: docker-compose up -d

version: '3.8'

services:
  web:
    # Exponer en todas las interfaces (0.0.0.0) para acceso desde red local
    ports:
      - "0.0.0.0:8000:8000"
    environment:
      # Permitir todos los hosts (⚠️ solo para red local confiable)
      ALLOWED_HOSTS: "*"
      
# ADVERTENCIA DE SEGURIDAD:
# Esta configuración permite acceso desde cualquier dispositivo en tu red local.
# Solo usa esto en redes privadas confiables (WiFi casa/oficina).
# NO expongas a internet público sin autenticación.
#
# Para acceder desde otros dispositivos:
# 1. Encuentra la IP de tu servidor: ip addr show (Linux) o ipconfig (Windows)
# 2. Abre en navegador: http://[IP-DEL-SERVIDOR]:8000
# Ejemplo: http://192.168.1.100:8000
OVERRIDE_EOF

# Crear .dockerignore
cat > .dockerignore << 'DOCKERIGNORE_EOF'
**/__pycache__/
**/*.pyc
**/*.pyo
**/*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.log

# Git
.git/
.gitignore

# Virtual environments
venv/
venv_django/
env/
ENV/

# Frontend node_modules
frontend/node_modules/
frontend/dist/

# Development files
.vscode/
.idea/
*.swp
*.swo
*~

# Databases
*.sqlite3
db.sqlite3
data/

# Tests
.coverage
htmlcov/
.pytest_cache/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
DOCKERIGNORE_EOF

# Crear .env.example
cat > .env.example << 'ENV_EOF'
# Configuración de MatrixCalc Web
# Copia este archivo a .env y personaliza los valores

# Django
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_PASSWORD=tu-password-postgres-seguro

# Matrix Calculator
MAX_DIMENSION=100
RETENTION_DAYS=30
CONDITION_THRESHOLD=1e12

# Scheduler
RUN_SCHEDULER=true
ENV_EOF

echo -e "${GREEN}✓ Docker configurado${NC}"

# ============================================================================
# PASO 4: Crear .gitignore actualizado
# ============================================================================
echo -e "\n${GREEN}✓ PASO 4: Actualizando .gitignore${NC}"

cat > .gitignore << 'GITIGNORE_EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
venv_django/
ENV/
env/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/
/backups/*.json

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.vite/

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Docker
docker-compose.override.yml
GITIGNORE_EOF

echo -e "${GREEN}✓ .gitignore actualizado${NC}"

# ============================================================================
# RESUMEN FINAL
# ============================================================================
echo -e "\n${GREEN}================================================================${NC}"
echo -e "${GREEN}✓✓✓ MIGRACIÓN COMPLETADA EXITOSAMENTE ✓✓✓${NC}"
echo -e "${GREEN}================================================================${NC}"

echo -e "\n${BLUE}📋 Próximos pasos:${NC}"
echo ""
echo "1. ${YELLOW}Desarrollo local (sin Docker):${NC}"
echo "   Terminal 1:"
echo "   $ source venv_django/bin/activate"
echo "   $ python manage.py runserver"
echo ""
echo "   Terminal 2:"
echo "   $ cd frontend"
echo "   $ npm run dev"
echo ""
echo "   Abrir: http://localhost:5173"
echo ""
echo "2. ${YELLOW}Producción con Docker:${NC}"
echo "   $ docker-compose up -d"
echo "   $ docker-compose logs -f"
echo "   Abrir: http://localhost:8000"
echo ""
echo "3. ${YELLOW}Acceso en red local:${NC}"
echo "   $ cp docker-compose.override.yml.example docker-compose.override.yml"
echo "   $ docker-compose up -d"
echo "   $ ip addr show  # Encuentra tu IP local"
echo "   Abrir desde otro dispositivo: http://[TU-IP]:8000"
echo ""
echo "4. ${YELLOW}Crear superusuario Django:${NC}"
echo "   $ python manage.py createsuperuser"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "5. ${YELLOW}Testing:${NC}"
echo "   $ pytest  # Tests backend"
echo "   $ cd frontend && npm test  # Tests frontend"
echo ""
echo "6. ${YELLOW}Comandos útiles:${NC}"
echo "   $ python manage.py cleanup_old_data --dry-run"
echo "   $ python manage.py export_backup"
echo "   $ python manage.py import_backup backups/backup_XXX.json"
echo ""
echo -e "${BLUE}📚 Documentación:${NC}"
echo "   - API: http://localhost:8000/api/"
echo "   - Stats: http://localhost:8000/api/stats/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
echo -e "${GREEN}¡Listo para desarrollar! 🚀${NC}"
EOF
