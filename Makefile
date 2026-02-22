.PHONY: help build up down logs shell test clean restart rebuild dev prod

help: ## Mostrar esta ayuda
	@echo "MatrixCalc - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Construir las imágenes Docker
	docker-compose build

up: ## Iniciar todos los servicios
	docker-compose up -d

down: ## Detener todos los servicios
	docker-compose down

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-backend: ## Ver logs del backend
	docker-compose logs -f backend

logs-frontend: ## Ver logs del frontend
	docker-compose logs -f frontend

logs-db: ## Ver logs de la base de datos
	docker-compose logs -f db

shell: ## Acceder a shell del backend
	docker-compose exec backend python manage.py shell

bash: ## Acceder a bash del backend
	docker-compose exec backend bash

dbshell: ## Acceder a PostgreSQL
	docker-compose exec db psql -U matrixcalc -d matrixcalc

migrate: ## Ejecutar migraciones
	docker-compose exec backend python manage.py migrate

makemigrations: ## Crear migraciones
	docker-compose exec backend python manage.py makemigrations

createsuperuser: ## Crear superusuario
	docker-compose exec backend python manage.py createsuperuser

collectstatic: ## Recolectar archivos estáticos
	docker-compose exec backend python manage.py collectstatic --noinput

backup: ## Exportar backup
	docker-compose exec backend python manage.py export_backup

cleanup: ## Limpiar datos antiguos (30 días)
	docker-compose exec backend python manage.py cleanup_old_data --days 30

test: ## Ejecutar tests
	docker-compose exec backend python manage.py test

restart: ## Reiniciar todos los servicios
	docker-compose restart

rebuild: ## Reconstruir todo desde cero
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d

clean: ## Limpiar contenedores, imágenes y volúmenes
	docker-compose down -v --rmi all

dev: ## Iniciar en modo desarrollo
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

prod: ## Iniciar en modo producción
	docker-compose up -d

status: ## Ver estado de los servicios
	docker-compose ps

deploy: ## Desplegar a Google Cloud Run vía Cloud Build
	gcloud builds submit --config cloudbuild.yaml .

setup: ## Setup inicial completo
	@echo "🚀 Iniciando setup de MatrixCalc..."
	@if [ ! -f .env ]; then \
		echo "📝 Copiando .env.example a .env..."; \
		cp .env.example .env; \
	fi
	@echo "🔨 Construyendo imágenes..."
	docker-compose build
	@echo "▶️  Iniciando servicios..."
	docker-compose up -d
	@echo "⏳ Esperando 10 segundos a que los servicios estén listos..."
	@sleep 10
	@echo "✅ Setup completado!"
	@echo ""
	@echo "📍 Servicios disponibles:"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000/api"
	@echo "   Admin:    http://localhost:8000/admin (admin/admin123)"
	@echo ""
	@echo "📋 Ver logs: make logs"
	@echo "🛑 Detener:  make down"
