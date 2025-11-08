@echo off
echo ========================================
echo Simple AWS Deployment (No CDK)
echo ========================================
echo.
echo This will deploy using AWS CLI instead of CDK
echo.

echo Step 1: Building Frontend...
cd frontend
call npm install
call npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed!
    exit /b 1
)
echo.

echo Step 2: Package Backend...
cd ..\backend
docker build -t healthlake-backend .
if %errorlevel% neq 0 (
    echo Docker build failed! Make sure Docker is running.
    exit /b 1
)
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Due to IAM restrictions in your AWS account,
echo you cannot use CDK bootstrap.
echo.
echo Options:
echo 1. Use Docker locally: docker-compose up
echo 2. Contact AWS admin to grant IAM permissions
echo 3. Use a different AWS account without restrictions
echo.
pause
