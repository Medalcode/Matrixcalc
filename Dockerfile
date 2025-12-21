# Backend Dockerfile - Multi-stage build
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-web.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements-web.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p backups calculator/static

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["gunicorn", "matrixcalc_web.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
