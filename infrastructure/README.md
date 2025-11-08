# AWS CDK Infrastructure

This directory contains AWS CDK code to deploy the HealthLake AI Assistant to AWS.

## Prerequisites

1. **AWS CLI** installed and configured
2. **Node.js** (for CDK CLI)
3. **Python 3.12+**
4. **Docker** (for Lambda container builds)

## Setup

### 1. Install AWS CDK CLI

```bash
npm install -g aws-cdk
```

### 2. Install Python Dependencies

```bash
cd infrastructure
pip install -r requirements.txt
```

### 3. Bootstrap CDK (First time only)

```bash
cdk bootstrap aws://YOUR_ACCOUNT_ID/us-west-2
```

Replace `YOUR_ACCOUNT_ID` with your AWS account ID.

## Deployment Steps

### Step 1: Build Frontend

```bash
cd ../frontend
npm install
npm run build
cd ../infrastructure
```

### Step 2: Synthesize CloudFormation

```bash
cdk synth
```

This generates CloudFormation templates.

### Step 3: Deploy All Stacks

```bash
cdk deploy --all
```

Or deploy individually:

```bash
# Deploy storage first
cdk deploy HealthLakeStorageStack

# Deploy backend
cdk deploy HealthLakeBackendStack

# Deploy frontend
cdk deploy HealthLakeFrontendStack
```

### Step 4: Get Outputs

After deployment, note the outputs:
- **ApiUrl**: Backend API endpoint
- **FrontendUrl**: CloudFront URL for the app

## Update Frontend API URL

After backend deployment, update frontend to use the API URL:

1. Edit `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://YOUR_API_GATEWAY_URL
```

2. Rebuild and redeploy frontend:
```bash
cd ../frontend
npm run build
cd ../infrastructure
cdk deploy HealthLakeFrontendStack
```

## Useful Commands

- `cdk ls` - List all stacks
- `cdk synth` - Synthesize CloudFormation
- `cdk diff` - Compare deployed vs local
- `cdk deploy` - Deploy stacks
- `cdk destroy` - Delete stacks

## Architecture

```
┌─────────────────┐
│   CloudFront    │ ← Users access here
└────────┬────────┘
         │
    ┌────▼─────┐
    │ S3 (Web) │ ← React frontend
    └──────────┘

┌──────────────────┐
│  API Gateway     │ ← API endpoint
└────────┬─────────┘
         │
    ┌────▼────────┐
    │   Lambda    │ ← FastAPI backend
    └─────┬───────┘
          │
    ┌─────▼──────┬──────────┬────────────┐
    │ HealthLake │ Bedrock  │ DynamoDB   │
    │            │ Agents   │ + S3       │
    └────────────┴──────────┴────────────┘
```

## Cost Estimate

- **S3**: ~$1-5/month
- **CloudFront**: ~$1-10/month
- **Lambda**: ~$5-20/month (depends on usage)
- **API Gateway**: ~$3-10/month
- **DynamoDB**: ~$1-5/month (on-demand)
- **HealthLake**: Existing
- **Bedrock**: Existing

**Total**: ~$15-50/month

## Cleanup

To delete all resources:

```bash
cdk destroy --all
```

**Note**: S3 buckets and DynamoDB tables have `RETAIN` policy and won't be deleted automatically.
