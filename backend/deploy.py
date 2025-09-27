#!/usr/bin/env python3
"""
Production deployment script for Smart City Management Platform Backend
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True, result.stdout
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False, e.stderr

def check_docker():
    """Check if Docker is installed and running."""
    print("🐳 Checking Docker...")
    
    success, output = run_command('docker --version', 'Checking Docker installation', check=False)
    if not success:
        print("❌ Docker is not installed. Please install Docker first.")
        return False
    
    success, output = run_command('docker-compose --version', 'Checking Docker Compose', check=False)
    if not success:
        print("❌ Docker Compose is not installed. Please install Docker Compose first.")
        return False
    
    success, output = run_command('docker info', 'Checking Docker daemon', check=False)
    if not success:
        print("❌ Docker daemon is not running. Please start Docker first.")
        return False
    
    return True

def check_environment():
    """Check environment configuration."""
    print("🔧 Checking environment configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found. Please create one from .env.example")
        return False
    
    # Check required environment variables
    required_vars = [
        'MONGO_URI',
        'JWT_SECRET_KEY',
        'SECRET_KEY'
    ]
    
    missing_vars = []
    with open(env_file, 'r') as f:
        env_content = f.read()
        for var in required_vars:
            if f'{var}=' not in env_content or f'{var}=your-' in env_content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or default values for: {', '.join(missing_vars)}")
        print("Please update your .env file with proper values.")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def build_images():
    """Build Docker images."""
    return run_command('docker-compose build', 'Building Docker images')[0]

def deploy_services():
    """Deploy services with Docker Compose."""
    return run_command('docker-compose up -d', 'Deploying services')[0]

def wait_for_services():
    """Wait for services to be healthy."""
    print("⏳ Waiting for services to be ready...")
    
    import time
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        success, output = run_command('curl -f http://localhost:5000/api/health', 
                                     'Checking backend health', check=False)
        if success:
            print("✅ Backend is healthy")
            return True
        
        retry_count += 1
        print(f"⏳ Waiting... ({retry_count}/{max_retries})")
        time.sleep(10)
    
    print("❌ Services failed to become healthy within timeout")
    return False

def run_database_migrations():
    """Run database migrations/initialization."""
    print("🗄️ Initializing database...")
    
    # Check if database is already initialized
    success, output = run_command(
        'docker-compose exec -T mongodb mongosh smart_city_db --eval "db.users.countDocuments()"',
        'Checking database initialization', check=False
    )
    
    if success and '0' not in output:
        print("✅ Database already initialized")
        return True
    
    # Run initialization script
    return run_command(
        'docker-compose exec -T mongodb mongosh smart_city_db < mongo-init.js',
        'Initializing database with sample data'
    )[0]

def setup_nginx():
    """Set up Nginx configuration."""
    print("🌐 Setting up Nginx...")
    
    # Check if Nginx container is running
    success, output = run_command(
        'docker-compose ps nginx',
        'Checking Nginx status', check=False
    )
    
    if 'Up' in output:
        print("✅ Nginx is running")
        return True
    else:
        print("⚠️ Nginx is not running. Check docker-compose.yml configuration.")
        return False

def create_backup():
    """Create a backup of the current deployment."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(f'backups/backup_{timestamp}')
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"💾 Creating backup in {backup_dir}...")
    
    # Backup database
    success, output = run_command(
        f'docker-compose exec -T mongodb mongodump --db smart_city_db --out /tmp/backup',
        'Creating database backup', check=False
    )
    
    if success:
        run_command(
            f'docker cp $(docker-compose ps -q mongodb):/tmp/backup {backup_dir}/mongodb',
            'Copying database backup'
        )
    
    # Backup logs
    logs_dir = Path('logs')
    if logs_dir.exists():
        run_command(f'cp -r logs {backup_dir}/', 'Backing up logs', check=False)
    
    print(f"✅ Backup created in {backup_dir}")
    return True

def show_deployment_info():
    """Show deployment information."""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📋 Service Information:")
    print("- Backend API: http://localhost:5000")
    print("- Health Check: http://localhost:5000/api/health")
    print("- Database: MongoDB on port 27017")
    print("- Cache: Redis on port 6379")
    print("- Web Server: Nginx on port 80")
    
    print("\n🔐 Default Admin Account:")
    print("- Email: admin@smartcity.com")
    print("- Password: admin123")
    print("- Role: Administrator")
    
    print("\n📊 Useful Commands:")
    print("- View logs: docker-compose logs -f")
    print("- Stop services: docker-compose down")
    print("- Restart services: docker-compose restart")
    print("- Scale backend: docker-compose up -d --scale backend=3")
    
    print("\n🔍 Monitoring:")
    print("- Check service status: docker-compose ps")
    print("- View resource usage: docker stats")
    print("- Backend logs: docker-compose logs backend")
    
    print("\n⚠️ Security Reminders:")
    print("- Change default admin password")
    print("- Update JWT secret keys in production")
    print("- Configure SSL certificates for HTTPS")
    print("- Set up firewall rules")
    print("- Enable log rotation")

def main():
    """Main deployment function."""
    print("🚀 Smart City Management Platform - Production Deployment")
    print("=" * 60)
    
    # Pre-deployment checks
    if not check_docker():
        sys.exit(1)
    
    if not check_environment():
        sys.exit(1)
    
    # Create backup before deployment
    create_backup()
    
    # Deployment steps
    steps = [
        ("Building Docker images", build_images),
        ("Deploying services", deploy_services),
        ("Waiting for services", wait_for_services),
        ("Initializing database", run_database_migrations),
        ("Setting up Nginx", setup_nginx)
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        if not step_function():
            failed_steps.append(step_name)
            response = input(f"❌ {step_name} failed. Continue anyway? (y/N): ")
            if response.lower() != 'y':
                print("Deployment aborted.")
                sys.exit(1)
    
    if failed_steps:
        print(f"\n⚠️ Deployment completed with warnings. Failed steps: {', '.join(failed_steps)}")
    else:
        show_deployment_info()

if __name__ == '__main__':
    main()
