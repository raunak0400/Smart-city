#!/usr/bin/env python3
"""
Full-stack deployment script for Smart City Management Platform
Deploys both backend and frontend with Docker Compose
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_command(command, description, cwd=None, check=True):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True, cwd=cwd)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False, e.stderr

def check_prerequisites():
    """Check if required software is installed."""
    print("🔍 Checking prerequisites...")
    
    requirements = {
        'docker': 'docker --version',
        'docker-compose': 'docker-compose --version',
        'python': 'python --version',
        'node': 'node --version',
        'npm': 'npm --version'
    }
    
    missing = []
    for name, command in requirements.items():
        success, output = run_command(command, f'Checking {name}', check=False)
        if success:
            version = output.strip().split('\n')[0]
            print(f"✅ {name}: {version}")
        else:
            print(f"❌ {name} is not installed")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing requirements: {', '.join(missing)}")
        print("Please install the missing software before continuing.")
        return False
    
    return True

def setup_environment():
    """Set up environment files for both backend and frontend."""
    print("🔧 Setting up environment configuration...")
    
    # Backend environment
    backend_env = Path('backend/.env')
    backend_env_example = Path('backend/.env.example')
    
    if not backend_env.exists() and backend_env_example.exists():
        with open(backend_env_example, 'r') as f:
            content = f.read()
        
        with open(backend_env, 'w') as f:
            f.write(content)
        
        print("✅ Created backend .env file")
    
    # Frontend environment
    frontend_env = Path('frontend/.env')
    frontend_env_example = Path('frontend/.env.example')
    
    if not frontend_env.exists() and frontend_env_example.exists():
        with open(frontend_env_example, 'r') as f:
            content = f.read()
        
        with open(frontend_env, 'w') as f:
            f.write(content)
        
        print("✅ Created frontend .env file")
    
    return True

def create_docker_compose():
    """Create a comprehensive docker-compose.yml for the full stack."""
    print("🐳 Creating full-stack docker-compose configuration...")
    
    docker_compose_content = """version: '3.8'

services:
  # MongoDB Database
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
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.runCommand({ping: 1})"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Flask Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: smart_city_backend
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - MONGO_URI=mongodb://admin:smartcity123@mongodb:27017/smart_city_db?authSource=admin
      - JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
      - SECRET_KEY=your-flask-secret-key-change-in-production
    ports:
      - "5000:5000"
    depends_on:
      mongodb:
        condition: service_healthy
    volumes:
      - ./backend/logs:/app/logs
    networks:
      - smart_city_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: smart_city_frontend
    restart: unless-stopped
    environment:
      - VITE_API_BASE_URL=http://localhost:5000/api
      - VITE_WS_URL=http://localhost:5000
    ports:
      - "3000:80"
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - smart_city_network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Nginx Reverse Proxy (Optional)
  nginx:
    image: nginx:alpine
    container_name: smart_city_nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - smart_city_network
    profiles:
      - production

volumes:
  mongodb_data:

networks:
  smart_city_network:
    driver: bridge
"""
    
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose_content)
    
    print("✅ Created docker-compose.yml")
    return True

def build_and_deploy():
    """Build and deploy the full stack."""
    print("🚀 Building and deploying the full stack...")
    
    # Build images
    success, output = run_command(
        'docker-compose build --no-cache',
        'Building Docker images'
    )
    if not success:
        return False
    
    # Start services
    success, output = run_command(
        'docker-compose up -d',
        'Starting services'
    )
    if not success:
        return False
    
    return True

def wait_for_services():
    """Wait for all services to be healthy."""
    print("⏳ Waiting for services to be ready...")
    
    import time
    max_retries = 60  # 5 minutes
    retry_count = 0
    
    while retry_count < max_retries:
        success, output = run_command(
            'docker-compose ps --format json',
            'Checking service status',
            check=False
        )
        
        if success:
            try:
                services = [json.loads(line) for line in output.strip().split('\n') if line]
                all_healthy = all(
                    service.get('Health', 'healthy') == 'healthy' 
                    for service in services
                )
                
                if all_healthy:
                    print("✅ All services are healthy")
                    return True
                    
            except (json.JSONDecodeError, KeyError):
                pass
        
        retry_count += 1
        print(f"⏳ Waiting... ({retry_count}/{max_retries})")
        time.sleep(5)
    
    print("❌ Services failed to become healthy within timeout")
    return False

def show_deployment_info():
    """Show deployment information and next steps."""
    print("\n" + "="*70)
    print("🎉 SMART CITY PLATFORM DEPLOYED SUCCESSFULLY!")
    print("="*70)
    
    print("\n🌐 Access URLs:")
    print("- Frontend (React):     http://localhost:3000")
    print("- Backend API:          http://localhost:5000")
    print("- API Health Check:     http://localhost:5000/api/health")
    print("- MongoDB:              mongodb://localhost:27017")
    
    print("\n🔐 Default Credentials:")
    print("- Admin:                admin@smartcity.com / admin123")
    print("- Traffic Officer:      traffic@smartcity.com / traffic123")
    print("- Environment Officer:  env@smartcity.com / env123")
    
    print("\n📊 Available Features:")
    print("- Real-time Dashboard with KPIs")
    print("- Traffic Management & Optimization")
    print("- Environmental Monitoring")
    print("- Waste Management & Route Planning")
    print("- Energy Grid Management")
    print("- Emergency Response System")
    print("- Analytics & Reporting")
    print("- Alert Management System")
    
    print("\n🔧 Management Commands:")
    print("- View logs:            docker-compose logs -f")
    print("- Stop services:        docker-compose down")
    print("- Restart services:     docker-compose restart")
    print("- View status:          docker-compose ps")
    print("- Scale backend:        docker-compose up -d --scale backend=3")
    
    print("\n📚 Documentation:")
    print("- Backend API:          ./backend/README.md")
    print("- Frontend Guide:       ./frontend/README.md")
    print("- Project Overview:     ./README.md")
    
    print("\n⚠️  Production Checklist:")
    print("- [ ] Change default passwords")
    print("- [ ] Update JWT secret keys")
    print("- [ ] Configure SSL certificates")
    print("- [ ] Set up monitoring and logging")
    print("- [ ] Configure backup strategies")
    print("- [ ] Review security settings")

def create_backup():
    """Create a backup before deployment."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(f'backups/backup_{timestamp}')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Creating backup in {backup_dir}...")
    
    # Backup configuration files
    config_files = [
        'docker-compose.yml',
        'backend/.env',
        'frontend/.env',
        'backend/config.py'
    ]
    
    for file_path in config_files:
        if Path(file_path).exists():
            run_command(
                f'cp {file_path} {backup_dir}/',
                f'Backing up {file_path}',
                check=False
            )
    
    print(f"✅ Backup created in {backup_dir}")
    return True

def main():
    """Main deployment function."""
    print("🚀 Smart City Management Platform - Full Stack Deployment")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not Path('backend').exists() or not Path('frontend').exists():
        print("❌ Backend or frontend directory not found.")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Deployment steps
    steps = [
        ("Checking prerequisites", check_prerequisites),
        ("Creating backup", create_backup),
        ("Setting up environment", setup_environment),
        ("Creating Docker Compose configuration", create_docker_compose),
        ("Building and deploying services", build_and_deploy),
        ("Waiting for services to be ready", wait_for_services)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_function():
            failed_steps.append(step_name)
            response = input(f"❌ {step_name} failed. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Deployment aborted.")
                print("\nTo clean up, run: docker-compose down --volumes")
                sys.exit(1)
    
    if failed_steps:
        print(f"\n⚠️  Deployment completed with warnings. Failed steps: {', '.join(failed_steps)}")
    else:
        show_deployment_info()

if __name__ == '__main__':
    main()
