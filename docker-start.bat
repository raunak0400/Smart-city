@echo off
setlocal enabledelayedexpansion

REM Smart City Management Platform - Docker Startup Script for Windows
REM This script provides easy commands to manage the Docker environment

set "command=%~1"
if "%command%"=="" set "command=start"

echo [INFO] Smart City Management Platform - Docker Management

REM Function to check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    exit /b 1
)
echo [SUCCESS] Docker is running

REM Function to check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker Compose is not available. Please install Docker Compose.
        exit /b 1
    )
)
echo [SUCCESS] Docker Compose is available
goto :eof

REM Function to create directories
:create_directories
echo [INFO] Creating necessary directories...
if not exist "backend\logs" mkdir "backend\logs"
if not exist "nginx\ssl" mkdir "nginx\ssl"
echo [SUCCESS] Directories created
goto :eof

REM Function to setup environment
:setup_environment
echo [INFO] Setting up environment files...

if not exist "backend\.env" (
    copy "backend\.env.example" "backend\.env" >nul
    echo [WARNING] Created backend\.env from example. Please update with your settings.
)

if not exist "frontend\.env" (
    copy "frontend\.env.example" "frontend\.env" >nul
    echo [WARNING] Created frontend\.env from example. Please update with your settings.
)

echo [SUCCESS] Environment setup complete
goto :eof

REM Function to start services
:start_services
echo [INFO] Building and starting Smart City Management Platform...

docker-compose up --build -d mongodb backend frontend

echo [INFO] Waiting for services to be healthy...

REM Wait for MongoDB
echo [INFO] Waiting for MongoDB to be ready...
set /a timeout=30
:wait_mongo
timeout /t 2 /nobreak >nul
docker-compose exec -T mongodb mongosh --eval "db.adminCommand('ping')" >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] MongoDB is ready
    goto :wait_backend
)
set /a timeout-=1
if %timeout% gtr 0 goto :wait_mongo
echo [ERROR] MongoDB failed to start within 60 seconds
exit /b 1

:wait_backend
REM Wait for Backend
echo [INFO] Waiting for Backend to be ready...
set /a timeout=40
:wait_backend_loop
timeout /t 3 /nobreak >nul
curl -f http://localhost:5000/api/health >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Backend is ready
    goto :wait_frontend
)
set /a timeout-=1
if %timeout% gtr 0 goto :wait_backend_loop
echo [ERROR] Backend failed to start within 120 seconds
docker-compose logs backend
exit /b 1

:wait_frontend
REM Wait for Frontend
echo [INFO] Waiting for Frontend to be ready...
set /a timeout=30
:wait_frontend_loop
timeout /t 2 /nobreak >nul
curl -f http://localhost:3000/health >nul 2>&1
if not errorlevel 1 (
    echo [SUCCESS] Frontend is ready
    goto :services_ready
)
set /a timeout-=1
if %timeout% gtr 0 goto :wait_frontend_loop
echo [ERROR] Frontend failed to start within 60 seconds
docker-compose logs frontend
exit /b 1

:services_ready
echo [SUCCESS] All services are running!
echo [INFO] Access the application at:
echo [INFO]   Frontend: http://localhost:3000
echo [INFO]   Backend API: http://localhost:5000/api
echo [INFO]   MongoDB: localhost:27017
goto :eof

REM Function to start production
:start_production
echo [INFO] Starting Smart City Management Platform in production mode...
docker-compose --profile production up --build -d

echo [INFO] Waiting for all services including Nginx...
timeout /t 30 /nobreak >nul

echo [SUCCESS] Production environment is running!
echo [INFO] Access the application at:
echo [INFO]   Main URL: http://localhost
echo [INFO]   Direct Frontend: http://localhost:3000
echo [INFO]   Direct Backend: http://localhost:5000/api
goto :eof

REM Function to stop services
:stop_services
echo [INFO] Stopping Smart City Management Platform...
docker-compose down
echo [SUCCESS] Services stopped
goto :eof

REM Function to restart services
:restart_services
echo [INFO] Restarting Smart City Management Platform...
docker-compose restart
echo [SUCCESS] Services restarted
goto :eof

REM Function to show status
:show_status
echo [INFO] Smart City Management Platform Status:
docker-compose ps
goto :eof

REM Function to view logs
:view_logs
if "%~2"=="" (
    echo [INFO] Showing logs for all services...
    docker-compose logs -f
) else (
    echo [INFO] Showing logs for %~2...
    docker-compose logs -f %~2
)
goto :eof

REM Function to cleanup
:cleanup
echo [INFO] Cleaning up Docker resources...
docker-compose down -v --remove-orphans
docker system prune -f
echo [SUCCESS] Cleanup complete
goto :eof

REM Function to show help
:show_help
echo Smart City Management Platform - Docker Management Script
echo.
echo Usage: %~nx0 [COMMAND]
echo.
echo Commands:
echo   start       Start the platform (development mode)
echo   start-prod  Start the platform with nginx (production mode)
echo   stop        Stop all services
echo   restart     Restart all services
echo   status      Show service status
echo   logs        Show logs for all services
echo   logs ^<svc^>  Show logs for specific service (mongodb^|backend^|frontend^|nginx)
echo   cleanup     Stop services and clean up Docker resources
echo   help        Show this help message
echo.
echo Examples:
echo   %~nx0 start                 # Start in development mode
echo   %~nx0 start-prod           # Start in production mode with nginx
echo   %~nx0 logs backend         # Show backend logs
echo   %~nx0 cleanup              # Clean up everything
goto :eof

REM Main script logic
if "%command%"=="start" (
    call :check_docker
    call :create_directories
    call :setup_environment
    call :start_services
) else if "%command%"=="start-prod" (
    call :check_docker
    call :create_directories
    call :setup_environment
    call :start_production
) else if "%command%"=="stop" (
    call :stop_services
) else if "%command%"=="restart" (
    call :restart_services
) else if "%command%"=="status" (
    call :show_status
) else if "%command%"=="logs" (
    call :view_logs %*
) else if "%command%"=="cleanup" (
    call :cleanup
) else if "%command%"=="help" (
    call :show_help
) else if "%command%"=="-h" (
    call :show_help
) else if "%command%"=="--help" (
    call :show_help
) else (
    echo [ERROR] Unknown command: %command%
    call :show_help
    exit /b 1
)

endlocal
