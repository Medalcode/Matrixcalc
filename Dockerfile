# Frontend Dockerfile - Multi-stage build
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files from frontend folder
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code from frontend folder
COPY frontend/ ./

# Build for production (skip type checking to speed up)
RUN npm run build-only

# Production stage
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Create nginx config for Cloud Run (port 8080)
RUN echo 'server { \
    listen 8080; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    gzip on; \
    gzip_vary on; \
    gzip_min_length 1024; \
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json; \
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ { \
    expires 1y; \
    add_header Cache-Control "public, immutable"; \
    } \
    location / { \
    try_files $uri $uri/ /index.html; \
    } \
    }' > /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
