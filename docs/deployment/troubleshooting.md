# Deployment Troubleshooting Guide

Common issues and solutions for MatrixCalc deployment.

---

## 📋 Table of Contents

- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Database Issues](#database-issues)
- [Docker Issues](#docker-issues)
- [Cloud Run Issues](#cloud-run-issues)
- [CORS Issues](#cors-issues)

---

## Backend Issues

### Error: "Invalid DATABASE_URL"

**Symptoms:**

- Backend fails to start
- Error message about database connection

**Solutions:**

1. Verify DATABASE_URL format:

   ```
   postgresql://user:password@host:port/database
   ```

2. Test connection manually:

   ```bash
   psql "postgresql://user:password@host:port/database"
   ```

3. Check for special characters in password:
   - URL-encode special characters
   - Example: `p@ssw0rd` → `p%40ssw0rd`

4. Verify database exists:
   ```bash
   psql -h host -U user -l
   ```

---

### Error: "Permission Denied"

**Symptoms:**

- Cannot access Cloud Run
- Cannot push to Artifact Registry

**Solutions:**

1. Re-authenticate:

   ```bash
   gcloud auth login
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

2. Check project permissions:

   ```bash
   gcloud projects get-iam-policy [PROJECT_ID]
   ```

3. Verify you have required roles:
   - Cloud Run Admin
   - Artifact Registry Writer
   - Cloud Build Editor

---

### Error: "SECRET_KEY not set"

**Symptoms:**

- Django fails to start
- Error about SECRET_KEY

**Solutions:**

1. Generate new SECRET_KEY:

   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

2. Set in environment:

   ```bash
   export SECRET_KEY="your-generated-key"
   ```

3. For Cloud Run:
   ```bash
   gcloud run services update matrixcalc-backend \
     --set-env-vars SECRET_KEY="your-key" \
     --region us-central1
   ```

---

## Frontend Issues

### Error: "Network Error" in Statistics

**Symptoms:**

- Frontend loads but API calls fail
- Statistics page shows error
- Console shows CORS or network errors

**Solutions:**

1. Verify backend is running:

   ```bash
   curl https://[BACKEND-URL]/api/stats/
   ```

2. Check VITE_API_URL in frontend:

   ```bash
   cat frontend/.env.production
   ```

   Should be: `VITE_API_URL=https://[BACKEND-URL]/api`

3. Rebuild frontend with correct URL:

   ```bash
   echo "VITE_API_URL=https://[BACKEND-URL]/api" > frontend/.env.production
   npm run build
   ```

4. Verify CORS configuration in Django:
   ```python
   # settings.py
   CORS_ALLOWED_ORIGINS = [
       "https://[FRONTEND-URL]",
   ]
   ```

---

### Error: "Page Not Found" on Routes

**Symptoms:**

- Direct navigation to /about or /docs returns 404
- Refresh on any route except / fails

**Solutions:**

1. Check nginx configuration:

   ```nginx
   location / {
       try_files $uri $uri/ /index.html;
   }
   ```

2. Verify Vue Router is in history mode:

   ```typescript
   // router/index.ts
   const router = createRouter({
     history: createWebHistory(),
     routes: [...]
   })
   ```

3. For Cloud Run, check Dockerfile.frontend:
   ```dockerfile
   COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
   ```

---

### Dark Mode Not Persisting

**Symptoms:**

- Dark mode resets on page reload
- Theme doesn't save

**Solutions:**

1. Check localStorage is enabled:
   - Open DevTools → Application → Local Storage
   - Verify `theme` key exists

2. Incognito mode limitation:
   - localStorage doesn't persist in incognito
   - This is expected browser behavior

3. Verify useTheme composable:
   ```typescript
   // Should save to localStorage
   localStorage.setItem("theme", theme.value);
   ```

---

## Database Issues

### Error: "Connection Refused"

**Symptoms:**

- Cannot connect to database
- Backend fails to start

**Solutions:**

1. Verify database is running:

   ```bash
   # For local PostgreSQL
   sudo systemctl status postgresql

   # For Docker
   docker-compose ps db
   ```

2. Check database host is accessible:

   ```bash
   ping db.xxx.supabase.co
   telnet db.xxx.supabase.co 5432
   ```

3. Verify firewall rules:
   - Supabase: Check IP whitelist
   - Cloud SQL: Check authorized networks

---

### Error: "Too Many Connections"

**Symptoms:**

- Intermittent database errors
- "remaining connection slots are reserved"

**Solutions:**

1. Check connection pool settings:

   ```python
   # settings.py
   DATABASES = {
       'default': {
           'CONN_MAX_AGE': 60,  # Reuse connections
       }
   }
   ```

2. Reduce max instances in Cloud Run:

   ```bash
   gcloud run services update matrixcalc-backend \
     --max-instances 5 \
     --region us-central1
   ```

3. Upgrade database plan (if using free tier)

---

## Docker Issues

### Error: "Build Failed"

**Symptoms:**

- Docker build fails
- Out of disk space

**Solutions:**

1. Clean Docker cache:

   ```bash
   docker system prune -a
   docker volume prune
   ```

2. Check disk space:

   ```bash
   df -h
   ```

3. Verify .dockerignore exists:
   ```
   node_modules
   __pycache__
   *.pyc
   .git
   .env
   ```

---

### Error: "Cannot Connect to Docker Daemon"

**Symptoms:**

- Docker commands fail
- "Cannot connect to the Docker daemon"

**Solutions:**

1. Start Docker:

   ```bash
   sudo systemctl start docker
   ```

2. Add user to docker group:

   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. Verify Docker is running:
   ```bash
   docker ps
   ```

---

## Cloud Run Issues

### Error: "Service Unavailable"

**Symptoms:**

- 503 errors
- Service not responding

**Solutions:**

1. Check service status:

   ```bash
   gcloud run services describe matrixcalc-backend \
     --region us-central1
   ```

2. View logs:

   ```bash
   gcloud logging read \
     "resource.labels.service_name=matrixcalc-backend" \
     --limit 50
   ```

3. Increase memory/CPU:
   ```bash
   gcloud run services update matrixcalc-backend \
     --memory 1Gi \
     --cpu 2 \
     --region us-central1
   ```

---

### Build Very Slow

**Symptoms:**

- Cloud Build takes 10+ minutes
- Timeout errors

**Solutions:**

1. Use .dockerignore:

   ```
   node_modules
   .git
   *.md
   ```

2. Use multi-stage builds:

   ```dockerfile
   FROM node:20 AS builder
   # Build stage

   FROM nginx:alpine
   # Runtime stage
   ```

3. Enable concurrent steps in cloudbuild.yaml:
   ```yaml
   options:
     machineType: "E2_HIGHCPU_8"
   ```

---

## CORS Issues

### Error: "CORS Policy Blocked"

**Symptoms:**

- Browser console shows CORS error
- API calls fail from frontend

**Solutions:**

1. Add frontend URL to CORS whitelist:

   ```python
   # settings.py
   CORS_ALLOWED_ORIGINS = [
       "https://matrixcalc-frontend-xxx.run.app",
       "http://localhost:5173",  # For development
   ]
   ```

2. Allow credentials if needed:

   ```python
   CORS_ALLOW_CREDENTIALS = True
   ```

3. For development, allow all origins (NOT for production):

   ```python
   CORS_ALLOW_ALL_ORIGINS = True  # Development only!
   ```

4. Verify CORS middleware is installed:

   ```python
   INSTALLED_APPS = [
       'corsheaders',
       ...
   ]

   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]
   ```

---

## General Debugging

### Enable Debug Logging

**Backend:**

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**Frontend:**

```typescript
// main.ts
if (import.meta.env.DEV) {
  console.log("API URL:", import.meta.env.VITE_API_URL);
}
```

---

### Check Environment Variables

**Cloud Run:**

```bash
gcloud run services describe matrixcalc-backend \
  --region us-central1 \
  --format 'value(spec.template.spec.containers[0].env)'
```

**Docker Compose:**

```bash
docker-compose config
```

---

## Still Having Issues?

1. **Check logs** - Most issues are visible in logs
2. **Search existing issues** - GitHub issues
3. **Create new issue** - Include:
   - Error message
   - Steps to reproduce
   - Environment (Cloud Run/Docker/Local)
   - Logs

---

**Last updated:** January 19, 2026
