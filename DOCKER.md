# 🚀 MatrixCalc - Docker Quick Start

## Requisitos Previos

- Docker Engine 20.10+
- Docker Compose 2.0+

## 🏃 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/Matrixcalc.git
cd Matrixcalc
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` y cambia los valores por defecto (especialmente SECRET_KEY y POSTGRES_PASSWORD en producción).

### 3. Construir y ejecutar con Docker Compose

```bash
# Construir las imágenes
docker-compose build

# Iniciar los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 4. Acceder a la aplicación

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/api
- **Admin Django:** http://localhost:8000/admin

**Credenciales de superusuario (creadas automáticamente):**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **Cambiar estas credenciales en producción**

## 📋 Comandos Útiles

### Ver estado de los servicios

```bash
docker-compose ps
```

### Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Solo base de datos
docker-compose logs -f db
```

### Ejecutar comandos Django

```bash
# Crear migraciones
docker-compose exec backend python manage.py makemigrations

# Aplicar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Shell de Django
docker-compose exec backend python manage.py shell

# Exportar backup
docker-compose exec backend python manage.py export_backup

# Limpiar datos antiguos
docker-compose exec backend python manage.py cleanup_old_data --days 30
```

### Acceder a la base de datos PostgreSQL

```bash
docker-compose exec db psql -U matrixcalc -d matrixcalc
```

### Detener servicios

```bash
# Detener sin eliminar contenedores
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores y volúmenes
docker-compose down -v
```

## 🔧 Desarrollo Local con Docker

Para desarrollo con hot-reload:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Esto:
- Monta los volúmenes de código para hot-reload
- Usa el servidor de desarrollo de Django (en lugar de Gunicorn)
- Usa el servidor de desarrollo de Vite (en lugar de Nginx)
- Frontend en http://localhost:5173

## 🏗️ Arquitectura Docker

```
┌─────────────────┐
│   Frontend      │
│   (Nginx)       │
│   Port: 3000    │
└────────┬────────┘
         │
         │ HTTP
         │
┌────────▼────────┐
│   Backend       │
│   (Gunicorn)    │
│   Port: 8000    │
└────────┬────────┘
         │
         │ SQL
         │
┌────────▼────────┐
│   PostgreSQL    │
│   Port: 5432    │
└─────────────────┘
```

## 📦 Volúmenes

- `postgres_data`: Datos persistentes de PostgreSQL
- `static_volume`: Archivos estáticos de Django
- `./backups`: Backups exportados desde el backend

## 🔒 Seguridad en Producción

1. Cambiar `SECRET_KEY` en `.env`
2. Cambiar `POSTGRES_PASSWORD` en `.env`
3. Cambiar credenciales del superusuario
4. Configurar `ALLOWED_HOSTS` con tu dominio
5. Configurar `CORS_ALLOWED_ORIGINS` con tu dominio frontend
6. Usar HTTPS con certificados SSL/TLS
7. Configurar firewall para puertos 80/443 solamente

## 🐛 Solución de Problemas

### La base de datos no está lista

Si el backend falla porque PostgreSQL no está listo, el `entrypoint.sh` tiene reintentos automáticos. Espera 30-60 segundos.

### Puerto ya en uso

Si el puerto 3000 o 8000 ya está en uso:

```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8080:80"  # Frontend en 8080
  - "8001:8000"  # Backend en 8001
```

### Reconstruir contenedores

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Ver más detalles de errores

```bash
docker-compose logs --tail=100 backend
docker-compose exec backend python manage.py check
```

## 📚 Más Información

- [Documentación completa](./docs/README.md)
- [API Documentation](./docs/API.md)
- [Contributing Guide](./CONTRIBUTING.md)
