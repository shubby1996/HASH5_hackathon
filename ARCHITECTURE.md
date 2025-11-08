# HealthLake AI Assistant - Architecture

## 🏗️ AWS Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USERS                                  │
│                    (Web Browsers)                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
                ┌────────▼────────┐
                │   CloudFront    │ ← CDN (Global Edge Locations)
                │  Distribution   │   - HTTPS enforced
                └────────┬────────┘   - Caching enabled
                         │            - DDoS protection
                         │
                    ┌────▼─────┐
                    │ S3 Bucket│ ← React Frontend (Static)
                    │ (Private)│   - index.html
                    └──────────┘   - JS/CSS bundles
                                   - Images

┌─────────────────────────────────────────────────────────────────┐
│                      API REQUESTS                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         │
                ┌────────▼────────┐
                │  API Gateway    │ ← REST API
                │   (Regional)    │   - CORS enabled
                └────────┬────────┘   - Request validation
                         │            - Throttling
                         │
                    ┌────▼─────┐
                    │  Lambda  │ ← FastAPI Backend (Docker)
                    │ Function │   - 15 min timeout
                    └─────┬────┘   - 1024 MB memory
                          │        - IAM role attached
                          │
        ┌─────────────────┼─────────────────┬──────────────┐
        │                 │                 │              │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐   ┌────▼────┐
   │HealthLake│      │ Bedrock │      │DynamoDB │   │ S3      │
   │Datastore│      │ Agents  │      │ Table   │   │ Bucket  │
   │         │      │         │      │         │   │         │
   │(Existing)│      │(Existing)│      │(New)    │   │(New)    │
   │         │      │         │      │         │   │         │
   │- FHIR R4│      │- 5 Agents│      │- Q&A    │   │- Reports│
   │- SYNTHEA│      │- Claude  │      │- History│   │- Storage│
   └─────────┘      └─────────┘      └─────────┘   └─────────┘
```

---

## 📦 Components

### Frontend (React)
- **Hosting**: S3 + CloudFront
- **Framework**: React 18
- **UI Library**: Material-UI
- **State**: Zustand
- **Charts**: Recharts
- **Build**: Static files (HTML/JS/CSS)

### Backend (FastAPI)
- **Compute**: AWS Lambda (Docker container)
- **Framework**: FastAPI
- **Runtime**: Python 3.12
- **API**: REST via API Gateway
- **Wrapper**: Mangum (ASGI to Lambda)

### Storage
- **DynamoDB**: Q&A conversation history
- **S3**: Generated reports (PDF/text)
- **HealthLake**: Patient FHIR data (existing)

### AI/ML
- **Bedrock Agents**: 5 specialized agents
  1. Orchestrator Agent
  2. Cardiologist Agent
  3. Radiologist Agent
  4. Endocrinologist Agent
  5. Q&A Agent
- **Model**: Claude 3 Sonnet

---

## 🔄 Data Flow

### 1. User Selects Patient
```
User → CloudFront → S3 (React App)
React → API Gateway → Lambda → HealthLake
HealthLake → Lambda → API Gateway → React
React displays patient data
```

### 2. Generate Report
```
User clicks "Generate Report"
React → API Gateway → Lambda
Lambda invokes 4 Bedrock Agents in parallel:
  - Cardiologist Agent
  - Radiologist Agent
  - Endocrinologist Agent
  - Orchestrator Agent (combines results)
Lambda saves report to S3
Lambda returns report to React
React displays report in tabs
```

### 3. Ask Question (Q&A)
```
User types question
React → API Gateway → Lambda
Lambda retrieves cached report from S3
Lambda invokes Q&A Agent with context
Lambda saves conversation to DynamoDB
Lambda returns answer to React
React displays answer with formatting
```

---

## 🔐 Security

### Network Security
- ✅ All traffic over HTTPS
- ✅ S3 buckets are private (no public access)
- ✅ CloudFront OAI for S3 access
- ✅ API Gateway with CORS

### IAM Permissions
- ✅ Lambda execution role with minimal permissions:
  - HealthLake: Read-only
  - Bedrock: InvokeAgent only
  - DynamoDB: Read/Write on specific table
  - S3: Read/Write on specific bucket
  - CloudWatch: Logs only

### Data Security
- ✅ DynamoDB encryption at rest
- ✅ S3 encryption (SSE-S3)
- ✅ S3 versioning enabled
- ✅ No credentials in code (IAM roles)

---

## 💰 Cost Breakdown

### Monthly Costs (Estimated)

| Service | Usage | Cost |
|---------|-------|------|
| **CloudFront** | 10 GB data transfer | $1-2 |
| **S3 (Frontend)** | 1 GB storage | $0.02 |
| **Lambda** | 10,000 invocations, 30s avg | $5-10 |
| **API Gateway** | 10,000 requests | $0.04 |
| **DynamoDB** | On-demand, 1000 reads/writes | $1-2 |
| **S3 (Reports)** | 5 GB storage | $0.12 |
| **HealthLake** | Existing | $0 |
| **Bedrock** | Existing | $0 |
| **Total** | | **$7-15/month** |

**Note**: Costs scale with usage. Free tier covers most development usage.

---

## 📊 Performance

### Latency
- **Frontend Load**: < 2 seconds (CloudFront cache)
- **API Calls**: < 500ms (except report generation)
- **Report Generation**: 20-25 seconds (parallel agents)
- **Q&A Response**: 3-5 seconds

### Scalability
- **CloudFront**: Global CDN, auto-scales
- **Lambda**: Auto-scales to 1000 concurrent executions
- **API Gateway**: 10,000 requests/second
- **DynamoDB**: On-demand, auto-scales
- **S3**: Unlimited storage

### Availability
- **CloudFront**: 99.9% SLA
- **Lambda**: 99.95% SLA
- **API Gateway**: 99.95% SLA
- **DynamoDB**: 99.99% SLA
- **S3**: 99.99% SLA

---

## 🔄 CI/CD (Future)

```
GitHub → GitHub Actions → CDK Deploy → AWS

Steps:
1. Push code to GitHub
2. GitHub Actions runs tests
3. Build frontend (npm run build)
4. CDK deploy (cdk deploy --all)
5. Smoke tests
6. Notify team
```

---

## 📈 Monitoring

### CloudWatch Metrics
- Lambda invocations
- Lambda errors
- Lambda duration
- API Gateway requests
- API Gateway 4xx/5xx errors
- DynamoDB read/write capacity

### CloudWatch Logs
- Lambda execution logs
- API Gateway access logs
- CloudFront access logs

### Alarms (Recommended)
- Lambda error rate > 5%
- API Gateway 5xx errors > 10
- Lambda duration > 60s
- DynamoDB throttling

---

## 🧪 Testing Strategy

### Local Testing
```bash
# Backend
cd backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm start
```

### Docker Testing
```bash
docker-compose up --build
```

### AWS Testing
```bash
# Deploy to staging
cdk deploy --all --context env=staging

# Run smoke tests
npm run test:e2e

# Deploy to production
cdk deploy --all --context env=production
```

---

## 🔧 Maintenance

### Regular Tasks
- [ ] Rotate AWS credentials (monthly)
- [ ] Review CloudWatch logs (weekly)
- [ ] Check costs (weekly)
- [ ] Update dependencies (monthly)
- [ ] Review IAM permissions (quarterly)

### Backup Strategy
- ✅ S3 versioning enabled (reports)
- ✅ DynamoDB point-in-time recovery
- ✅ CloudFormation stacks (infrastructure as code)

### Disaster Recovery
- **RTO**: 1 hour (redeploy from CDK)
- **RPO**: 5 minutes (DynamoDB PITR)

---

## 📚 Documentation

- `README.md` - Main documentation
- `AWS_DEPLOYMENT_COMPLETE.md` - Deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `DEPLOYMENT_SUMMARY.md` - Quick summary
- `QUICK_START_AWS.md` - 5-step quick start
- `infrastructure/README.md` - CDK documentation
- `ARCHITECTURE.md` - This file

---

## 🎯 Future Enhancements

### Short Term
- [ ] Custom domain (Route 53)
- [ ] SSL certificate (ACM)
- [ ] CloudWatch dashboards
- [ ] Cost alerts

### Medium Term
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Staging environment
- [ ] E2E tests (Cypress)
- [ ] Load testing (Locust)

### Long Term
- [ ] Multi-region deployment
- [ ] WAF (Web Application Firewall)
- [ ] Cognito authentication
- [ ] API rate limiting per user

---

**Architecture Version**: 1.0
**Last Updated**: January 2025
**Status**: Production Ready ✅
