# Smart City Management Platform - Docker Setup

This document provides comprehensive instructions for running the Smart City Management Platform using Docker with complete isolation and proper orchestration.

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0 or higher
- **Git** (for cloning the repository)
- At least **4GB RAM** available for Docker
- **Ports 3000, 5000, 27017** available on your system

### One-Command Startup

**Windows:**
```cmd
docker-start.bat start
```

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh start
```

**Or using Docker Compose directly:**
```bash
docker-compose up --build
```

## 📋 Architecture Overview

The platform consists of 4 main services running in isolated containers:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    MongoDB      │    │     Nginx       │
│   (React)       │    │    (Flask)      │    │   (Database)    │    │ (Reverse Proxy) │
│   Port: 3000    │    │   Port: 5000    │    │  Port: 27017    │    │   Port: 80      │
│                 │    │                 │    │                 │    │   (Optional)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         └───────────────────────┼───────────────────────┼───────────────────────┘
                                 │                       │
                        ┌─────────────────┐    ┌─────────────────┐
                        │ Docker Network  │    │  Shared Volumes │
                        │smart_city_network│    │  mongodb_data   │
                        └─────────────────┘    └─────────────────┘
```

## 🛠️ Service Details

### 1. MongoDB Database
- **Image:** `mongo:6.0`
- **Port:** `27017`
- **Volume:** Persistent data storage
- **Health Check:** MongoDB ping command
- **Startup Time:** ~30 seconds

### 2. Flask Backend
- **Build:** Custom Dockerfile with multi-stage build
- **Port:** `5000`
- **Dependencies:** MongoDB (waits for health check)
- **Health Check:** `/api/health` endpoint
- **Startup Time:** ~60 seconds

### 3. React Frontend
- **Build:** Multi-stage build (Node.js → Nginx)
- **Port:** `3000` (mapped to container port 80)
- **Dependencies:** Backend (waits for health check)
- **Health Check:** `/health` endpoint
- **Startup Time:** ~40 seconds

### 4. Nginx Reverse Proxy (Optional)
- **Image:** `nginx:alpine`
- **Port:** `80`, `443`
- **Profile:** `production` (only starts in production mode)
- **Features:** Load balancing, SSL termination, rate limiting

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
# Database
MONGO_URI=mongodb://admin:smartcity123@mongodb:27017/smart_city_db?authSource=admin
MONGO_DB_NAME=smart_city_db

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
SECRET_KEY=your-flask-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask
FLASK_ENV=production
GUNICORN_WORKERS=4
GUNICORN_BIND=0.0.0.0:5000
```

**Frontend (.env):**
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:5000

# Application
VITE_APP_NAME=Smart City Management Platform
VITE_APP_VERSION=1.0.0

# Features
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_DARK_MODE=true
```

## 📝 Available Commands

### Using Helper Scripts

**Windows (docker-start.bat):**
```cmd
docker-start.bat start          # Start development environment
docker-start.bat start-prod     # Start with nginx (production)
docker-start.bat stop           # Stop all services
docker-start.bat restart        # Restart all services
docker-start.bat status         # Show service status
docker-start.bat logs           # Show all logs
docker-start.bat logs backend   # Show specific service logs
docker-start.bat cleanup        # Clean up Docker resources
docker-start.bat help           # Show help
```

**Linux/Mac (docker-start.sh):**
```bash
./docker-start.sh start          # Start development environment
./docker-start.sh start-prod     # Start with nginx (production)
./docker-start.sh stop           # Stop all services
./docker-start.sh restart        # Restart all services
./docker-start.sh status         # Show service status
./docker-start.sh logs           # Show all logs
./docker-start.sh logs backend   # Show specific service logs
./docker-start.sh cleanup        # Clean up Docker resources
./docker-start.sh help           # Show help
```

### Using Docker Compose Directly

```bash
# Start all services
docker-compose up -d

# Start with build
docker-compose up --build -d

# Start production (with nginx)
docker-compose --profile production up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
docker-compose logs -f backend

# Scale services
docker-compose up -d --scale backend=2

# Remove everything including volumes
docker-compose down -v --remove-orphans
```

## 🌐 Access URLs

### Development Mode
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000/api
- **API Documentation:** http://localhost:5000/api/docs
- **MongoDB:** localhost:27017

### Production Mode (with Nginx)
- **Main Application:** http://localhost
- **API (via proxy):** http://localhost/api
- **Direct Frontend:** http://localhost:3000
- **Direct Backend:** http://localhost:5000/api

## 🔍 Health Checks & Monitoring

All services include comprehensive health checks:

```bash
# Check service health
docker-compose ps

# View health check logs
docker inspect smart_city_backend --format='{{.State.Health.Status}}'
docker inspect smart_city_frontend --format='{{.State.Health.Status}}'
docker inspect smart_city_mongodb --format='{{.State.Health.Status}}'

# Manual health checks
curl http://localhost:5000/api/health    # Backend
curl http://localhost:3000/health        # Frontend
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using the port
netstat -ano | findstr :3000    # Windows
lsof -i :3000                   # Linux/Mac

# Kill the process or change ports in docker-compose.yml
```

**2. MongoDB Connection Issues**
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Connect to MongoDB directly
docker-compose exec mongodb mongosh -u admin -p smartcity123
```

**3. Backend Not Starting**
```bash
# Check backend logs
docker-compose logs backend

# Check if MongoDB is ready
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

**4. Frontend Build Issues**
```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild frontend only
docker-compose build frontend
docker-compose up -d frontend
```

**5. Permission Issues (Linux/Mac)**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
chmod +x docker-start.sh
```

### Debug Mode

Enable debug logging:

```bash
# Set debug environment
export COMPOSE_LOG_LEVEL=DEBUG

# Run with verbose output
docker-compose up --build
```

### Performance Issues

**Increase Docker Resources:**
- Memory: At least 4GB
- CPU: At least 2 cores
- Disk: At least 10GB free space

**Optimize Build:**
```bash
# Use BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Build with no cache
docker-compose build --no-cache
```

## 🔒 Security Considerations

### Production Deployment

1. **Change Default Passwords:**
   ```env
   MONGO_INITDB_ROOT_PASSWORD=your-secure-password
   JWT_SECRET_KEY=your-256-bit-secret-key
   SECRET_KEY=your-flask-secret-key
   ```

2. **Use SSL/TLS:**
   - Place SSL certificates in `nginx/ssl/`
   - Update nginx configuration for HTTPS

3. **Network Security:**
   - Use Docker secrets for sensitive data
   - Implement proper firewall rules
   - Use non-root users in containers

4. **Regular Updates:**
   ```bash
   # Update base images
   docker-compose pull
   docker-compose up -d
   ```

### Environment Isolation

Each service runs in its own container with:
- Separate file systems
- Isolated network namespace
- Resource limits
- Non-root user execution
- Read-only root filesystem where possible

## 📊 Performance Monitoring

### Resource Usage

```bash
# Monitor resource usage
docker stats

# Check container resource limits
docker inspect smart_city_backend --format='{{.HostConfig.Memory}}'
```

### Logs Management

```bash
# Rotate logs
docker-compose logs --tail=100 backend

# Export logs
docker-compose logs backend > backend.log
```

## 🚀 Deployment Options

### Local Development
```bash
./docker-start.sh start
```

### Production with Load Balancer
```bash
./docker-start.sh start-prod
```

### Cloud Deployment
- Use `docker-compose.yml` with cloud providers
- Configure external databases and storage
- Set up proper monitoring and alerting

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker and application logs
3. Ensure all prerequisites are met
4. Check port availability and Docker resources

## 🔄 Updates and Maintenance

### Updating the Platform
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Database Backup
```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out /data/backup

# Restore MongoDB
docker-compose exec mongodb mongorestore /data/backup
```

---

**Happy Coding! 🎉**

The Smart City Management Platform is now fully containerized and ready for development and production use.
