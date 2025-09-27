# Smart City Management Platform - Setup Guide

This comprehensive guide will walk you through setting up the Smart City Management Platform from scratch, including all prerequisites, configuration, and deployment options.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Detailed Setup](#detailed-setup)
5. [Configuration](#configuration)
6. [Database Setup](#database-setup)
7. [Frontend Setup](#frontend-setup)
8. [Backend Setup](#backend-setup)
9. [Docker Deployment](#docker-deployment)
10. [Production Setup](#production-setup)
11. [Environment Variables](#environment-variables)
12. [Troubleshooting](#troubleshooting)
13. [Testing](#testing)
14. [Monitoring](#monitoring)

## 📦 Prerequisites

### Required Software

#### 1. **Python 3.8+**
```bash
# Windows (using Chocolatey)
choco install python

# macOS (using Homebrew)
brew install python@3.11

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify installation
python --version
pip --version
```

#### 2. **Node.js 16+**
```bash
# Windows (using Chocolatey)
choco install nodejs

# macOS (using Homebrew)
brew install node

# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

#### 3. **MongoDB 6.0+**
```bash
# Windows (using Chocolatey)
choco install mongodb

# macOS (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
mongosh --version
```

#### 4. **Docker (Optional but Recommended)**
```bash
# Windows - Download Docker Desktop from https://docker.com
# macOS - Download Docker Desktop from https://docker.com

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
docker --version
docker-compose --version
```

#### 5. **Git**
```bash
# Windows (using Chocolatey)
choco install git

# macOS (using Homebrew)
brew install git

# Ubuntu/Debian
sudo apt install git

# Verify installation
git --version
```

### Optional Tools

- **VS Code**: Recommended IDE with extensions for Python, JavaScript, Docker
- **MongoDB Compass**: GUI for MongoDB management
- **Postman**: API testing and development
- **curl**: Command-line HTTP client for testing

## 🖥️ System Requirements

### Minimum Requirements
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### Recommended Requirements
- **CPU**: 4 cores, 2.5 GHz
- **RAM**: 8 GB
- **Storage**: 20 GB free space (SSD preferred)
- **Network**: Stable internet connection for dependencies

### Production Requirements
- **CPU**: 8+ cores, 3.0 GHz
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **Network**: High-speed internet with static IP
- **Load Balancer**: For high availability

## 🚀 Quick Start

### Option 1: Automated Full-Stack Deployment (Recommended)
```bash
# Clone the repository
git clone https://github.com/prathamupadhyay341/smart-city-management.git
cd smart-city-management

# Run the automated deployment script
python deploy-full-stack.py
```

### Option 2: Development Mode
```bash
# Clone the repository
git clone https://github.com/prathamupadhyay341/smart-city-management.git
cd smart-city-management

# Backend setup
cd backend
python setup.py
python start.py

# Frontend setup (in a new terminal)
cd ../frontend
npm install
node start.js
```

### Option 3: Docker Deployment
```bash
# Clone the repository
git clone https://github.com/prathamupadhyay341/smart-city-management.git
cd smart-city-management

# Deploy with Docker Compose
docker-compose up -d
```

## 🔧 Detailed Setup

### 1. Project Clone and Structure
```bash
# Clone the repository
git clone https://github.com/prathamupadhyay341/smart-city-management.git
cd smart-city-management

# Verify project structure
ls -la
# Should show: backend/, frontend/, README.md, SETUP.md, etc.
```

### 2. Backend Setup

#### Step 1: Navigate to Backend Directory
```bash
cd backend
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv smart_city_env

# Activate virtual environment
# Windows
smart_city_env\Scripts\activate
# macOS/Linux
source smart_city_env/bin/activate

# Verify activation (should show virtual environment name)
which python
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

#### Step 4: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables (use your preferred editor)
nano .env
# or
code .env
```

#### Step 5: Database Initialization
```bash
# Start MongoDB (if not already running)
sudo systemctl start mongod

# Initialize database with sample data
python -c "
from src.utils.db_init import init_database
init_database()
print('Database initialized successfully!')
"
```

#### Step 6: Test Backend
```bash
# Run backend server
python start.py

# In another terminal, test API
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", ...}
```

### 3. Frontend Setup

#### Step 1: Navigate to Frontend Directory
```bash
cd ../frontend
```

#### Step 2: Install Dependencies
```bash
# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0
```

#### Step 3: Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
# or
code .env
```

#### Step 4: Build and Test Frontend
```bash
# Start development server
npm run dev

# In another terminal, test frontend
curl http://localhost:3000
# Should return HTML content
```

## ⚙️ Configuration

### Backend Configuration (`backend/.env`)
```bash
# Flask Configuration
FLASK_ENV=development
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production

# Database Configuration
MONGO_URI=mongodb://localhost:27017/smart_city_db
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=smartcity123

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-256-bits-minimum
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# API Configuration
API_TITLE=Smart City Management API
API_VERSION=1.0.0
API_DESCRIPTION=Comprehensive city management platform

# External APIs (Optional)
WEATHER_API_KEY=your-weather-api-key
MAPS_API_KEY=your-google-maps-api-key

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

### Frontend Configuration (`frontend/.env`)
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:5000

# Application Configuration
VITE_APP_NAME=Smart City Management Platform
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_DARK_MODE=true

# External Services (Optional)
VITE_GOOGLE_MAPS_API_KEY=your-google-maps-api-key
VITE_SENTRY_DSN=your-sentry-dsn

# Development Settings
VITE_DEBUG=false
VITE_LOG_LEVEL=info
```

## 🗄️ Database Setup

### MongoDB Configuration

#### 1. Create Database User
```bash
# Connect to MongoDB
mongosh

# Switch to admin database
use admin

# Create admin user
db.createUser({
  user: "admin",
  pwd: "smartcity123",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
})

# Create application database
use smart_city_db

# Create application user
db.createUser({
  user: "smart_city_user",
  pwd: "smart_city_password",
  roles: ["readWrite"]
})

# Exit MongoDB shell
exit
```

#### 2. Initialize Sample Data
```bash
# Run database initialization script
cd backend
python -c "
from src.utils.db_init import init_database
init_database()
"
```

#### 3. Verify Database Setup
```bash
# Connect to database
mongosh "mongodb://admin:smartcity123@localhost:27017/smart_city_db?authSource=admin"

# List collections
show collections

# Check sample data
db.users.find().limit(5)
db.traffic_data.find().limit(5)

# Exit
exit
```

### Database Indexes (Performance Optimization)
```bash
# Create performance indexes
mongosh "mongodb://admin:smartcity123@localhost:27017/smart_city_db?authSource=admin" --eval "
db.users.createIndex({ email: 1 }, { unique: true });
db.alerts.createIndex({ created_at: -1 });
db.alerts.createIndex({ status: 1, severity: 1 });
db.traffic_data.createIndex({ timestamp: -1 });
db.environment_data.createIndex({ timestamp: -1, sensor_id: 1 });
db.waste_bins.createIndex({ location: '2dsphere' });
db.energy_data.createIndex({ timestamp: -1, grid_id: 1 });
"
```

## 🐳 Docker Deployment

### Single Service Deployment

#### Backend Only
```bash
cd backend
docker build -t smart-city-backend .
docker run -d \
  --name smart-city-backend \
  -p 5000:5000 \
  -e MONGO_URI=mongodb://host.docker.internal:27017/smart_city_db \
  smart-city-backend
```

#### Frontend Only
```bash
cd frontend
docker build -t smart-city-frontend .
docker run -d \
  --name smart-city-frontend \
  -p 3000:80 \
  -e VITE_API_BASE_URL=http://localhost:5000/api \
  smart-city-frontend
```

### Full Stack Deployment
```bash
# Deploy entire stack
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Scale services
docker-compose up -d --scale backend=3

# Stop services
docker-compose down
```

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    container_name: smart_city_mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: smartcity123
      MONGO_INITDB_DATABASE: smart_city_db
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - ./backend/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - smart_city_network

  backend:
    build: ./backend
    container_name: smart_city_backend
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - MONGO_URI=mongodb://admin:smartcity123@mongodb:27017/smart_city_db?authSource=admin
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    networks:
      - smart_city_network

  frontend:
    build: ./frontend
    container_name: smart_city_frontend
    restart: unless-stopped
    environment:
      - VITE_API_BASE_URL=http://localhost:5000/api
      - VITE_WS_URL=http://localhost:5000
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - smart_city_network

volumes:
  mongodb_data:

networks:
  smart_city_network:
    driver: bridge
```

## 🏭 Production Setup

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash smartcity
sudo usermod -aG sudo smartcity
```

### 2. SSL Certificate Setup
```bash
# Install SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test certificate renewal
sudo certbot renew --dry-run

# Setup auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Nginx Configuration
```nginx
# /etc/nginx/sites-available/smart-city
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket
    location /socket.io/ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4. Process Management with Systemd
```bash
# Backend service
sudo tee /etc/systemd/system/smart-city-backend.service > /dev/null <<EOF
[Unit]
Description=Smart City Backend
After=network.target

[Service]
Type=simple
User=smartcity
WorkingDirectory=/home/smartcity/smart-city-management/backend
Environment=PATH=/home/smartcity/smart-city-management/backend/smart_city_env/bin
ExecStart=/home/smartcity/smart-city-management/backend/smart_city_env/bin/python start.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable smart-city-backend
sudo systemctl start smart-city-backend
```

### 5. Database Backup Strategy
```bash
# Create backup script
sudo tee /usr/local/bin/backup-smart-city.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/backups/smart-city"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# MongoDB backup
mongodump --uri="mongodb://admin:smartcity123@localhost:27017/smart_city_db?authSource=admin" --out="$BACKUP_DIR/mongodb_$DATE"

# Compress backup
tar -czf "$BACKUP_DIR/smart_city_backup_$DATE.tar.gz" -C "$BACKUP_DIR" "mongodb_$DATE"
rm -rf "$BACKUP_DIR/mongodb_$DATE"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: smart_city_backup_$DATE.tar.gz"
EOF

# Make executable
sudo chmod +x /usr/local/bin/backup-smart-city.sh

# Schedule daily backups
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-smart-city.sh
```

## 🔧 Environment Variables

### Complete Environment Variables Reference

#### Backend Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Flask environment | `development` | Yes |
| `DEBUG` | Debug mode | `True` | No |
| `SECRET_KEY` | Flask secret key | - | Yes |
| `MONGO_URI` | MongoDB connection string | - | Yes |
| `JWT_SECRET_KEY` | JWT signing key | - | Yes |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token expiry (seconds) | `3600` | No |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token expiry (seconds) | `2592000` | No |
| `WEATHER_API_KEY` | Weather service API key | - | No |
| `MAPS_API_KEY` | Maps service API key | - | No |
| `MAIL_SERVER` | SMTP server | - | No |
| `MAIL_PORT` | SMTP port | `587` | No |
| `MAIL_USE_TLS` | Use TLS for email | `True` | No |
| `MAIL_USERNAME` | Email username | - | No |
| `MAIL_PASSWORD` | Email password | - | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `LOG_FILE` | Log file path | `logs/app.log` | No |

#### Frontend Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:5000/api` | Yes |
| `VITE_WS_URL` | WebSocket URL | `http://localhost:5000` | Yes |
| `VITE_APP_NAME` | Application name | `Smart City Management Platform` | No |
| `VITE_APP_VERSION` | Application version | `1.0.0` | No |
| `VITE_ENABLE_ANALYTICS` | Enable analytics | `true` | No |
| `VITE_ENABLE_NOTIFICATIONS` | Enable notifications | `true` | No |
| `VITE_ENABLE_DARK_MODE` | Enable dark mode | `true` | No |
| `VITE_GOOGLE_MAPS_API_KEY` | Google Maps API key | - | No |
| `VITE_SENTRY_DSN` | Sentry DSN for error tracking | - | No |
| `VITE_DEBUG` | Debug mode | `false` | No |
| `VITE_LOG_LEVEL` | Logging level | `info` | No |

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. MongoDB Connection Issues
```bash
# Check MongoDB status
sudo systemctl status mongod

# Check MongoDB logs
sudo journalctl -u mongod -f

# Restart MongoDB
sudo systemctl restart mongod

# Test connection
mongosh "mongodb://localhost:27017/smart_city_db"
```

#### 2. Port Already in Use
```bash
# Find process using port
lsof -i :5000
netstat -tulpn | grep :5000

# Kill process
kill -9 <PID>

# Or use different port
export PORT=5001
python start.py
```

#### 3. Python Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf smart_city_env
python -m venv smart_city_env
source smart_city_env/bin/activate
pip install -r requirements.txt
```

#### 4. Node.js Dependencies Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use specific Node.js version
nvm install 18
nvm use 18
```

#### 5. Docker Issues
```bash
# Check Docker status
docker --version
docker-compose --version

# View container logs
docker-compose logs backend
docker-compose logs frontend

# Restart containers
docker-compose restart

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

#### 6. Permission Issues
```bash
# Fix file permissions
chmod +x setup.py start.py
chmod +x frontend/start.js

# Fix directory permissions
chown -R $USER:$USER .
```

#### 7. Frontend Build Issues
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev -- --force

# Check for TypeScript errors
npm run type-check

# Build for production
npm run build
npm run preview
```

### Debug Mode Setup
```bash
# Backend debug mode
export FLASK_ENV=development
export DEBUG=True
python start.py

# Frontend debug mode
export VITE_DEBUG=true
npm run dev
```

### Log Analysis
```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f --tail=100

# System logs
sudo journalctl -f -u smart-city-backend
```

## 🧪 Testing

### Backend Testing
```bash
cd backend

# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Frontend Testing
```bash
cd frontend

# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test
npm test -- Button.test.tsx
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test authentication
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@smartcity.com","password":"admin123"}'

# Test protected endpoint
curl -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/dashboard/overview
```

### Load Testing
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test API performance
ab -n 1000 -c 10 http://localhost:5000/api/health

# Test with authentication
ab -n 100 -c 5 -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/dashboard/overview
```

## 📊 Monitoring

### Application Monitoring
```bash
# Install monitoring tools
pip install prometheus-client
npm install @sentry/react @sentry/tracing

# Setup Prometheus metrics endpoint
# Add to backend/app.py:
from prometheus_client import generate_latest, Counter, Histogram
```

### System Monitoring
```bash
# Install system monitoring
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs

# Monitor disk usage
df -h
du -sh *
```

### Database Monitoring
```bash
# MongoDB monitoring
mongosh --eval "db.runCommand({serverStatus: 1})"

# Monitor database size
mongosh --eval "db.stats()"

# Monitor collections
mongosh --eval "db.runCommand({collStats: 'users'})"
```

### Log Monitoring
```bash
# Setup log rotation
sudo tee /etc/logrotate.d/smart-city > /dev/null <<EOF
/home/smartcity/smart-city-management/backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 smartcity smartcity
    postrotate
        systemctl reload smart-city-backend
    endscript
}
EOF
```

## 🎯 Next Steps

After successful setup:

1. **Customize Configuration**: Update environment variables for your specific needs
2. **Setup Monitoring**: Implement comprehensive monitoring and alerting
3. **Security Hardening**: Follow the security guidelines in [SECURITY.md](./SECURITY.md)
4. **Performance Optimization**: Tune database indexes and caching strategies
5. **Backup Strategy**: Implement regular backups and disaster recovery
6. **CI/CD Pipeline**: Setup automated testing and deployment
7. **Documentation**: Create user guides and API documentation
8. **Training**: Train users on the platform features and workflows

## 📞 Support

If you encounter any issues during setup:

- **Email**: [prathamu341@gmail.com](mailto:prathamu341@gmail.com)
- **Issues**: Create an issue in the repository
- **Documentation**: Check [README.md](./README.md) and [SECURITY.md](./SECURITY.md)

---

**Setup Guide by Pratham Upadhyay** - Last Updated: September 2024
