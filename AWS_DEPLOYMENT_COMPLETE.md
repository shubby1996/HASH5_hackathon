# AWS Deployment Guide - Complete

## 🎯 Overview

This guide will deploy your HealthLake AI Assistant to AWS using CDK.

**What gets deployed:**
- ✅ S3 + CloudFront (React frontend)
- ✅ Lambda + API Gateway (FastAPI backend)
- ✅ DynamoDB (Q&A history)
- ✅ S3 (Reports storage)

**What's already deployed:**
- ✅ AWS Bedrock Agents (5 agents)
- ✅ AWS HealthLake (datastore)
- ✅ IAM roles

---

## 📋 Prerequisites

### 1. Install AWS CDK CLI

```bash
npm install -g aws-cdk
```

Verify installation:
```bash
cdk --version
```

### 2. Install Infrastructure Dependencies

```bash
cd infrastructure
pip install -r requirements.txt
```

### 3. Configure AWS Credentials

Your `.env` file already has credentials. CDK will use them automatically.

### 4. Bootstrap CDK (First Time Only)

Get your AWS account ID:
```bash
aws sts get-caller-identity --query Account --output text
```

Bootstrap CDK:
```bash
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-west-2
```

Replace `YOUR_ACCOUNT_ID` with your actual account ID (e.g., 891450252216).

---

## 🚀 Deployment Steps

### Step 1: Build Frontend

```bash
cd frontend
npm install
npm run build
```

This creates `frontend/build/` directory with production React app.

### Step 2: Synthesize CDK (Optional - Test)

```bash
cd ../infrastructure
cdk synth
```

This generates CloudFormation templates. Check for errors.

### Step 3: Deploy All Stacks

**Option A: Deploy All at Once (Recommended)**

```bash
cdk deploy --all
```

**Option B: Deploy One by One**

```bash
# 1. Storage (DynamoDB + S3)
cdk deploy HealthLakeStorageStack

# 2. Backend (Lambda + API Gateway)
cdk deploy HealthLakeBackendStack

# 3. Frontend (S3 + CloudFront)
cdk deploy HealthLakeFrontendStack
```

### Step 4: Note the Outputs

After deployment, you'll see outputs like:

```
HealthLakeBackendStack.ApiUrl = https://abc123.execute-api.us-west-2.amazonaws.com/prod/
HealthLakeFrontendStack.FrontendUrl = https://d1234567890.cloudfront.net
```

**Save these URLs!**

### Step 5: Update Frontend API URL

1. Edit `frontend/.env.production`:

```bash
REACT_APP_API_URL=https://YOUR_API_GATEWAY_URL
```

Replace with your actual API Gateway URL from Step 4.

2. Rebuild frontend:

```bash
cd ../frontend
npm run build
```

3. Redeploy frontend:

```bash
cd ../infrastructure
cdk deploy HealthLakeFrontendStack
```

### Step 6: Test Your Deployment

Open the CloudFront URL in your browser:

```
https://d1234567890.cloudfront.net
```

You should see the HealthLake AI Assistant!

---

## 🎉 Quick Deploy Script

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

---

## 🔧 Troubleshooting

### Issue: "CDK not found"

**Solution:**
```bash
npm install -g aws-cdk
```

### Issue: "Docker not running"

**Solution:** Start Docker Desktop before deploying.

### Issue: "Bootstrap required"

**Solution:**
```bash
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-west-2
```

### Issue: "Frontend build fails"

**Solution:**
```bash
cd frontend
rm -rf node_modules
npm install
npm run build
```

### Issue: "Lambda timeout"

**Solution:** Lambda timeout is set to 900s (15 min). If still timing out, check CloudWatch logs:

```bash
aws logs tail /aws/lambda/HealthLakeBackendStack-BackendFunction --follow
```

### Issue: "CORS errors"

**Solution:** Backend already configured for CORS. If issues persist, check API Gateway CORS settings in AWS Console.

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Users                            │
└────────────────────────┬────────────────────────────────┘
                         │
                ┌────────▼────────┐
                │   CloudFront    │ (CDN)
                └────────┬────────┘
                         │
                    ┌────▼─────┐
                    │ S3 Bucket│ (React App)
                    └──────────┘

┌─────────────────────────────────────────────────────────┐
│                     API Requests                        │
└────────────────────────┬────────────────────────────────┘
                         │
                ┌────────▼────────┐
                │  API Gateway    │
                └────────┬────────┘
                         │
                    ┌────▼─────┐
                    │  Lambda  │ (FastAPI)
                    └─────┬────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │HealthLake│      │ Bedrock │      │DynamoDB │
   │          │      │ Agents  │      │   +S3   │
   └──────────┘      └─────────┘      └─────────┘
```

---

## 💰 Cost Estimate

| Service | Monthly Cost |
|---------|--------------|
| S3 (Frontend) | $1-2 |
| CloudFront | $1-5 |
| Lambda | $5-20 |
| API Gateway | $3-10 |
| DynamoDB | $1-5 |
| S3 (Reports) | $1-3 |
| **Total** | **$12-45** |

**Note:** HealthLake and Bedrock costs are separate (already incurred).

---

## 🔐 Security

- ✅ S3 buckets are private (no public access)
- ✅ CloudFront uses HTTPS
- ✅ API Gateway uses HTTPS
- ✅ Lambda has minimal IAM permissions
- ✅ DynamoDB encryption at rest
- ✅ S3 versioning enabled

---

## 📝 Useful Commands

```bash
# List all stacks
cdk ls

# Show differences
cdk diff

# Deploy specific stack
cdk deploy HealthLakeBackendStack

# Destroy all stacks
cdk destroy --all

# View CloudFormation template
cdk synth HealthLakeBackendStack

# Check Lambda logs
aws logs tail /aws/lambda/HealthLakeBackendStack-BackendFunction --follow
```

---

## 🧹 Cleanup

To delete all AWS resources:

```bash
cd infrastructure
cdk destroy --all
```

**Note:** S3 buckets and DynamoDB tables have `RETAIN` policy. Delete manually if needed:

```bash
aws s3 rb s3://healthlake-reports-YOUR_ACCOUNT_ID --force
aws s3 rb s3://healthlake-frontend-YOUR_ACCOUNT_ID --force
aws dynamodb delete-table --table-name healthlake-qa-history
```

---

## 🎯 Next Steps After Deployment

1. ✅ Test all features (patient selection, reports, Q&A)
2. ✅ Monitor CloudWatch logs for errors
3. ✅ Set up CloudWatch alarms for Lambda errors
4. ✅ Configure custom domain (optional)
5. ✅ Set up CI/CD pipeline (optional)

---

## 📞 Support

If deployment fails:

1. Check CloudWatch logs
2. Verify AWS credentials
3. Ensure Docker is running
4. Check CDK version: `cdk --version`
5. Bootstrap CDK if needed

---

## ✅ Deployment Checklist

- [ ] AWS CDK CLI installed
- [ ] Infrastructure dependencies installed
- [ ] AWS credentials configured
- [ ] CDK bootstrapped
- [ ] Frontend built successfully
- [ ] CDK synth runs without errors
- [ ] All stacks deployed
- [ ] API URL noted
- [ ] Frontend URL noted
- [ ] Frontend .env.production updated
- [ ] Frontend redeployed
- [ ] Application tested and working

---

**Ready to deploy? Run:**

```bash
cd infrastructure
deploy.bat  # Windows
# or
./deploy.sh  # Mac/Linux
```

**Good luck! 🚀**
