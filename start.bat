@echo off
echo Starting HealthLake AI Assistant...
echo.

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting services with Docker Compose...
docker-compose up --build

pause
