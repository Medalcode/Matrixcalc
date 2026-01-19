# MatrixCalc Deployment Guide

Complete guide for deploying MatrixCalc to production environments.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
  - [Google Cloud Run (Recommended)](#google-cloud-run-recommended)
  - [Docker Compose](#docker-compose)
  - [Traditional Server](#traditional-server)
- [Post-Deployment](#post-deployment)
- [Troubleshooting](#troubleshooting)
- [Monitoring](#monitoring)

---

## Overview

MatrixCalc can be deployed in multiple ways:

- **Google Cloud Run** - Serverless, auto-scaling (recommended for production)
- **Docker Compose** - Simple containerized deployment
- **Traditional Server** - Manual setup on VPS/dedicated server

**Tech Stack:**

- Backend: Django 4.2 + PostgreSQL
- Frontend: Vue.js 3 + Nginx
- Containerization: Docker

---

## Prerequisites

### Required:

- **Git** - Version control
- **Docker** - Container runtime (20.10+)
- **Docker Compose** - Multi-container orchestration (2.0+)

### For Cloud Run:

- **Google Cloud Account** with billing enabled
- **gcloud CLI** - [Installation guide](https://cloud.google.com/sdk/docs/install)
- **Supabase Account** (or PostgreSQL database)

### For Local/Traditional:

- **Python 3.11+**
- **Node.js 20+**
- **PostgreSQL 15+**

---

## Deployment Options

### Google Cloud Run (Recommended)

Complete serverless deployment with auto-scaling and zero maintenance.

#### Step 1: Setup Supabase Database

1. Create account at [supabase.com](https://supabase.com)
2. Create new project:
   - Name: `matrixcalc-db`
   - Region: Choose closest (e.g., São Paulo)
   - Save database password

3. Get connection string:
   - Go to **Settings** → **Database**
   - Copy **Connection string** → **URI**
   - Format: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`

4. Run migrations:

```bash
# Connect to Supabase
psql "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"

# Or use Django
python manage.py migrate
```

#### Step 2: Configure Google Cloud

```bash
# Login to GCP
gcloud auth login

# Create project
gcloud projects create matrixcalc-prod --name="MatrixCalc Production"

# Set active project
gcloud config set project matrixcalc-prod

# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com
```

#### Step 3: Create Artifact Registry

```bash
# Create Docker repository
gcloud artifacts repositories create matrixcalc \
  --repository-format=docker \
  --location=us-central1 \
  --description="MatrixCalc container images"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev
```

#### Step 4: Configure Environment Variables

```bash
# Generate Django SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Create production environment file (DO NOT COMMIT)
cat > .env.production << EOF
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
SECRET_KEY=[YOUR_GENERATED_SECRET_KEY]
ALLOWED_HOSTS=*
DEBUG=False
MAX_DIMENSION=100
RETENTION_DAYS=30
EOF
```

#### Step 5: Deploy Backend

```bash
# Build and push backend image
docker build -f Dockerfile.backend \
  -t us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/backend:latest .

docker push us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/backend:latest

# Deploy to Cloud Run
gcloud run deploy matrixcalc-backend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/backend:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="[YOUR_DATABASE_URL]" \
  --set-env-vars SECRET_KEY="[YOUR_SECRET_KEY]" \
  --set-env-vars DEBUG=False \
  --set-env-vars ALLOWED_HOSTS="*" \
  --max-instances 10 \
  --min-instances 0 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 60

# Get backend URL
gcloud run services describe matrixcalc-backend \
  --region us-central1 \
  --format 'value(status.url)'
```

#### Step 6: Deploy Frontend

```bash
# Configure frontend to use backend URL
cat > frontend/.env.production << EOF
VITE_API_URL=https://[BACKEND-URL]/api
EOF

# Build and push frontend image
docker build -f Dockerfile.frontend \
  -t us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/frontend:latest .

docker push us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/frontend:latest

# Deploy to Cloud Run
gcloud run deploy matrixcalc-frontend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/frontend:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --max-instances 5 \
  --min-instances 0 \
  --memory 256Mi \
  --cpu 1

# Get frontend URL
gcloud run services describe matrixcalc-frontend \
  --region us-central1 \
  --format 'value(status.url)'
```

#### Step 7: Setup CI/CD (Optional)

```bash
# Create Cloud Build trigger
gcloud builds triggers create github \
  --name="matrixcalc-deploy" \
  --repo-name="Matrixcalc" \
  --repo-owner="[YOUR_GITHUB_USERNAME]" \
  --branch-pattern="^main$" \
  --build-config="cloudbuild.yaml"
```

Configure substitution variables in Cloud Build console:

- `_DATABASE_URL`: Your Supabase URL
- `_SECRET_KEY`: Your Django SECRET_KEY
- `_REGION`: `us-central1`
- `_REPOSITORY`: `matrixcalc`

---

### Docker Compose

Simple deployment using Docker Compose for development or small production.

#### Step 1: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

Required variables:

```env
DATABASE_URL=postgresql://postgres:password@db:5432/matrixcalc
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Step 2: Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

#### Step 3: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Admin: http://localhost:8000/admin

---

### Traditional Server

Manual deployment on VPS or dedicated server.

#### Backend Setup

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv postgresql nginx

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements-web.txt

# Configure database
sudo -u postgres createdb matrixcalc
sudo -u postgres createuser matrixcalc_user

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start with Gunicorn
gunicorn matrixcalc_web.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --daemon
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Serve with Nginx
sudo cp -r dist/* /var/www/matrixcalc/
```

Configure Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/matrixcalc;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Post-Deployment

### Verification

#### Backend Health Check

```bash
curl https://[BACKEND-URL]/api/stats/
```

Expected response: JSON with statistics

#### Frontend Access

```bash
# Open in browser
open https://[FRONTEND-URL]
```

Verify:

- ✅ Homepage loads
- ✅ Dark mode toggle works
- ✅ Can create/list matrices
- ✅ Statistics page loads
- ✅ API calls succeed

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Setup CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Configure rate limiting

---

## Troubleshooting

See [troubleshooting.md](./troubleshooting.md) for detailed solutions.

### Common Issues

**"Network Error" in Statistics**

- Verify backend is running
- Check CORS configuration
- Verify VITE_API_URL is correct

**"Page Not Found" on routes**

- Check nginx configuration has `try_files`
- Verify Vue Router is configured

**Database connection errors**

- Verify DATABASE_URL format
- Check database is accessible
- Test connection with psql

**Build failures**

- Check Docker daemon is running
- Verify .dockerignore excludes node_modules
- Check disk space

---

## Monitoring

### View Logs (Cloud Run)

```bash
# Backend logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=matrixcalc-backend" \
  --limit 50

# Frontend logs
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=matrixcalc-frontend" \
  --limit 50
```

### View Logs (Docker Compose)

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Metrics

**Cloud Run Console:**

- https://console.cloud.google.com/run

**Key Metrics to Monitor:**

- Request count
- Response time (p50, p95, p99)
- Error rate
- Memory usage
- CPU utilization

---

## Useful Commands

### Update Backend Only

```bash
gcloud run deploy matrixcalc-backend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/backend:latest \
  --region us-central1
```

### Update Frontend Only

```bash
gcloud run deploy matrixcalc-frontend \
  --image us-central1-docker.pkg.dev/matrixcalc-prod/matrixcalc/frontend:latest \
  --region us-central1
```

### Rollback to Previous Version

```bash
# List revisions
gcloud run revisions list --service matrixcalc-backend --region us-central1

# Rollback
gcloud run services update-traffic matrixcalc-backend \
  --to-revisions [REVISION_NAME]=100 \
  --region us-central1
```

### Scale Services

```bash
# Increase max instances
gcloud run services update matrixcalc-backend \
  --max-instances 20 \
  --region us-central1

# Set minimum instances (always-on, costs money)
gcloud run services update matrixcalc-backend \
  --min-instances 1 \
  --region us-central1
```

---

## Cost Estimates

### Google Cloud (Free Tier)

- **Cloud Run**: 2M requests/month, 360,000 GB-seconds/month
- **Cloud Build**: 120 builds/day
- **Artifact Registry**: 0.5GB storage

### Supabase (Free Tier)

- **PostgreSQL**: 500MB storage
- **Bandwidth**: 2GB/month
- **Queries**: Unlimited

**Estimated Cost: $0/month** within free tier limits

For production traffic, expect **$5-20/month** depending on usage.

---

## Next Steps

1. **Custom Domain** - Configure your domain in Cloud Run
2. **HTTPS** - Cloud Run includes automatic HTTPS
3. **Monitoring** - Setup alerts in Cloud Monitoring
4. **Backups** - Automate database backups
5. **CDN** - Use Cloud CDN for frontend (optional)

---

**Need help?** Create an issue in the repository.

**Last updated:** January 19, 2026
