#!/bin/bash

# Smart City Management Platform - Docker Startup Script
# This script provides easy commands to manage the Docker environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1 && ! docker compose version > /dev/null 2>&1; then
        print_error "Docker Compose is not available. Please install Docker Compose."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    mkdir -p backend/logs
    mkdir -p nginx/ssl
    print_success "Directories created"
}

# Function to copy environment files
setup_environment() {
    print_status "Setting up environment files..."
    
    # Backend environment
    if [ ! -f "backend/.env" ]; then
        cp backend/.env.example backend/.env
        print_warning "Created backend/.env from example. Please update with your settings."
    fi
    
    # Frontend environment
    if [ ! -f "frontend/.env" ]; then
        cp frontend/.env.example frontend/.env
        print_warning "Created frontend/.env from example. Please update with your settings."
    fi
    
    print_success "Environment setup complete"
}

# Function to build and start services
start_services() {
    print_status "Building and starting Smart City Management Platform..."
    
    # Build and start core services (without nginx)
    docker-compose up --build -d mongodb backend frontend
    
    print_status "Waiting for services to be healthy..."
    
    # Wait for MongoDB
    print_status "Waiting for MongoDB to be ready..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
            print_success "MongoDB is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "MongoDB failed to start within 60 seconds"
        exit 1
    fi
    
    # Wait for Backend
    print_status "Waiting for Backend to be ready..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
            print_success "Backend is ready"
            break
        fi
        sleep 3
        timeout=$((timeout-3))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Backend failed to start within 120 seconds"
        docker-compose logs backend
        exit 1
    fi
    
    # Wait for Frontend
    print_status "Waiting for Frontend to be ready..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -f http://localhost:3000/health > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Frontend failed to start within 60 seconds"
        docker-compose logs frontend
        exit 1
    fi
    
    print_success "All services are running!"
    print_status "Access the application at:"
    print_status "  Frontend: http://localhost:3000"
    print_status "  Backend API: http://localhost:5000/api"
    print_status "  MongoDB: localhost:27017"
}

# Function to start with production nginx
start_production() {
    print_status "Starting Smart City Management Platform in production mode..."
    docker-compose --profile production up --build -d
    
    print_status "Waiting for all services including Nginx..."
    sleep 30
    
    print_success "Production environment is running!"
    print_status "Access the application at:"
    print_status "  Main URL: http://localhost"
    print_status "  Direct Frontend: http://localhost:3000"
    print_status "  Direct Backend: http://localhost:5000/api"
}

# Function to stop services
stop_services() {
    print_status "Stopping Smart City Management Platform..."
    docker-compose down
    print_success "Services stopped"
}

# Function to restart services
restart_services() {
    print_status "Restarting Smart City Management Platform..."
    docker-compose restart
    print_success "Services restarted"
}

# Function to view logs
view_logs() {
    service=${1:-""}
    if [ -z "$service" ]; then
        print_status "Showing logs for all services..."
        docker-compose logs -f
    else
        print_status "Showing logs for $service..."
        docker-compose logs -f "$service"
    fi
}

# Function to clean up
cleanup() {
    print_status "Cleaning up Docker resources..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    print_success "Cleanup complete"
}

# Function to show status
show_status() {
    print_status "Smart City Management Platform Status:"
    docker-compose ps
}

# Function to show help
show_help() {
    echo "Smart City Management Platform - Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start the platform (development mode)"
    echo "  start-prod  Start the platform with nginx (production mode)"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  status      Show service status"
    echo "  logs        Show logs for all services"
    echo "  logs <svc>  Show logs for specific service (mongodb|backend|frontend|nginx)"
    echo "  cleanup     Stop services and clean up Docker resources"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                 # Start in development mode"
    echo "  $0 start-prod           # Start in production mode with nginx"
    echo "  $0 logs backend         # Show backend logs"
    echo "  $0 cleanup              # Clean up everything"
}

# Main script logic
case "${1:-start}" in
    "start")
        check_docker
        check_docker_compose
        create_directories
        setup_environment
        start_services
        ;;
    "start-prod")
        check_docker
        check_docker_compose
        create_directories
        setup_environment
        start_production
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "status")
        show_status
        ;;
    "logs")
        view_logs "$2"
        ;;
    "cleanup")
        cleanup
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
