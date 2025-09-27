# Multi-stage build for React frontend
FROM node:18-alpine as build

# Build arguments for environment variables
ARG VITE_API_BASE_URL=http://localhost:5000/api
ARG VITE_WS_URL=http://localhost:5000
ARG VITE_APP_NAME=Smart City Management Platform
ARG VITE_APP_VERSION=1.0.0
ARG VITE_ENABLE_ANALYTICS=true
ARG VITE_ENABLE_NOTIFICATIONS=true
ARG VITE_ENABLE_DARK_MODE=true
ARG VITE_DEBUG=false
ARG VITE_LOG_LEVEL=info

# Set environment variables from build args
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_WS_URL=$VITE_WS_URL
ENV VITE_APP_NAME=$VITE_APP_NAME
ENV VITE_APP_VERSION=$VITE_APP_VERSION
ENV VITE_ENABLE_ANALYTICS=$VITE_ENABLE_ANALYTICS
ENV VITE_ENABLE_NOTIFICATIONS=$VITE_ENABLE_NOTIFICATIONS
ENV VITE_ENABLE_DARK_MODE=$VITE_ENABLE_DARK_MODE
ENV VITE_DEBUG=$VITE_DEBUG
ENV VITE_LOG_LEVEL=$VITE_LOG_LEVEL

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm ci --silent

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Create nginx cache directories with proper permissions
RUN mkdir -p /var/cache/nginx/client_temp \
    && mkdir -p /var/cache/nginx/proxy_temp \
    && mkdir -p /var/cache/nginx/fastcgi_temp \
    && mkdir -p /var/cache/nginx/uwsgi_temp \
    && mkdir -p /var/cache/nginx/scgi_temp \
    && mkdir -p /var/log/nginx \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /usr/share/nginx/html \
    && chown -R nginx:nginx /var/log/nginx \
    && chmod -R 755 /usr/share/nginx/html

# Create a simple health check endpoint
RUN echo '<!DOCTYPE html><html><head><title>Health Check</title></head><body><h1>OK</h1></body></html>' > /usr/share/nginx/html/health

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
