#!/bin/bash
set -e

echo "🚀 MatrixCalc Backend - Starting..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Run migrations
echo "📦 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "👤 Creating superuser (if not exists)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
END

echo "✅ Setup completed!"
echo "🎯 Starting application..."

# Execute the main command
exec "$@"
