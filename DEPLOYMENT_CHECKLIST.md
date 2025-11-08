# AWS Deployment Checklist

## ✅ Pre-Deployment (Complete)

- [x] Backend API built (FastAPI)
- [x] Frontend built (React)
- [x] Docker setup working
- [x] AWS Bedrock agents deployed
- [x] AWS HealthLake configured
- [x] Lambda handler created
- [x] CDK infrastructure code created

## 📋 Deployment Steps (To Do)

### 1. Install Prerequisites

- [ ] Install AWS CDK CLI: `npm install -g aws-cdk`
- [ ] Verify CDK: `cdk --version`
- [ ] Install infrastructure dependencies: `cd infrastructure && pip install -r requirements.txt`

### 2. Bootstrap CDK (First Time Only)

- [ ] Get AWS account ID: `aws sts get-caller-identity --query Account --output text`
- [ ] Bootstrap: `cdk bootstrap aws://YOUR_ACCOUNT_ID/us-west-2`

### 3. Build Frontend

- [ ] `cd frontend`
- [ ] `npm install`
- [ ] `npm run build`
- [ ] Verify `frontend/build/` directory exists

### 4. Test CDK Synthesis

- [ ] `cd ../infrastructure`
- [ ] `cdk synth`
- [ ] Check for errors

### 5. Deploy to AWS

- [ ] `cdk deploy --all`
- [ ] Wait for deployment (10-15 minutes)
- [ ] Note the outputs:
  - [ ] ApiUrl: ___________________________________
  - [ ] FrontendUrl: ___________________________________

### 6. Update Frontend Configuration

- [ ] Edit `frontend/.env.production`
- [ ] Set `REACT_APP_API_URL=YOUR_API_GATEWAY_URL`
- [ ] Rebuild: `cd ../frontend && npm run build`
- [ ] Redeploy: `cd ../infrastructure && cdk deploy HealthLakeFrontendStack`

### 7. Test Deployment

- [ ] Open CloudFront URL in browser
- [ ] Test patient selection
- [ ] Test report generation
- [ ] Test Q&A system
- [ ] Test visualizations

### 8. Monitor & Verify

- [ ] Check CloudWatch logs for errors
- [ ] Verify all API endpoints working
- [ ] Test from different browsers
- [ ] Test on mobile devices

## 🎯 Quick Deploy (Alternative)

Instead of manual steps, use the deploy script:

**Windows:**
```bash
cd infrastructure
deploy.bat
```

**Mac/Linux:**
```bash
cd infrastructure
chmod +x deploy.sh
./deploy.sh
```

## 📊 Deployment Status

| Stack | Status | URL/Output |
|-------|--------|------------|
| Storage (DynamoDB + S3) | ⏳ Pending | - |
| Backend (Lambda + API Gateway) | ⏳ Pending | - |
| Frontend (S3 + CloudFront) | ⏳ Pending | - |

## 🔧 Troubleshooting

If deployment fails, check:

- [ ] Docker is running
- [ ] AWS credentials are valid (not expired)
- [ ] CDK is bootstrapped
- [ ] Frontend build succeeded
- [ ] No port conflicts

## 📝 Notes

Write any issues or observations here:

---

## ✅ Post-Deployment

- [ ] Update README with production URLs
- [ ] Document any configuration changes
- [ ] Set up monitoring/alerts (optional)
- [ ] Configure custom domain (optional)
- [ ] Set up CI/CD (optional)

---

**Current Status:** Ready to deploy! 🚀

**Next Action:** Install CDK CLI and run deployment script
