@echo off
echo [INFO] Smart City Management Platform - Health Check

echo [INFO] Checking Docker Compose configuration...
docker-compose config >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose configuration is invalid
    exit /b 1
) else (
    echo [SUCCESS] Docker Compose configuration is valid
)

echo [INFO] Checking if services are running...
docker-compose ps

echo [INFO] Checking service health...
for /f "tokens=*" %%i in ('docker-compose ps -q') do (
    for /f "tokens=*" %%j in ('docker inspect %%i --format="{{.Name}} - {{.State.Health.Status}}"') do (
        echo [HEALTH] %%j
    )
)

echo [INFO] Health check complete!
