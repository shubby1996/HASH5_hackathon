@echo off
echo ========================================
echo HealthLake AI Assistant - AWS Deployment
echo ========================================
echo.

echo Step 1: Building Frontend...
cd ..\frontend
call npm install
call npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed!
    exit /b 1
)
echo Frontend build complete!
echo.

echo Step 2: Deploying to AWS...
cd ..\infrastructure
cdk deploy --all --require-approval never
if %errorlevel% neq 0 (
    echo Deployment failed!
    exit /b 1
)

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Check the outputs above for:
echo - ApiUrl: Your backend API endpoint
echo - FrontendUrl: Your CloudFront URL
echo.
echo Next steps:
echo 1. Update frontend/.env.production with ApiUrl
echo 2. Rebuild frontend: npm run build
echo 3. Redeploy frontend: cdk deploy HealthLakeFrontendStack
echo.
pause
