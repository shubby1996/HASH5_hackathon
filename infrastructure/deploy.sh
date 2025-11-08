#!/bin/bash

echo "========================================"
echo "HealthLake AI Assistant - AWS Deployment"
echo "========================================"
echo ""

echo "Step 1: Building Frontend..."
cd ../frontend
npm install
npm run build
if [ $? -ne 0 ]; then
    echo "Frontend build failed!"
    exit 1
fi
echo "Frontend build complete!"
echo ""

echo "Step 2: Deploying to AWS..."
cd ../infrastructure
cdk deploy --all --require-approval never
if [ $? -ne 0 ]; then
    echo "Deployment failed!"
    exit 1
fi

echo ""
echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo ""
echo "Check the outputs above for:"
echo "- ApiUrl: Your backend API endpoint"
echo "- FrontendUrl: Your CloudFront URL"
echo ""
echo "Next steps:"
echo "1. Update frontend/.env.production with ApiUrl"
echo "2. Rebuild frontend: npm run build"
echo "3. Redeploy frontend: cdk deploy HealthLakeFrontendStack"
echo ""
