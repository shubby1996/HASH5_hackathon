# HealthLake AI Assistant - Quick Reference

One-page reference for the entire system.

---

## 🎯 What Is This?

AI-powered healthcare assistant that generates comprehensive medical reports using 5 specialized AI agents analyzing patient data from AWS HealthLake.

---

## 📊 System Stats

| Metric | Value |
|--------|-------|
| **Frontend** | React 18 + Material-UI |
| **Backend** | FastAPI + Python 3.12 |
| **AI Agents** | 5 (Bedrock Claude 3 Sonnet) |
| **Data Source** | AWS HealthLake (FHIR R4) |
| **Patients** | 120+ with complete medical history |
| **FHIR Resources** | 10 types (5000+ total records) |
| **Report Time** | 20-25 seconds |
| **Q&A Response** | 3-5 seconds |

---

## 🤖 The 5 AI Agents

| Agent | ID | Purpose | Time |
|-------|-----|---------|------|
| **Cardiologist** | CDMSLUEUFQ | Cardiac health analysis | 5-8s |
| **Radiologist** | K0MU8VCNSK | Medical imaging interpretation | 5-8s |
| **Endocrinologist** | 0GRU0APJFO | Metabolic/endocrine health | 5-8s |
| **Orchestrator** | C5XRILWF9L | Coordinates & synthesizes | 5-8s |
| **Q&A** | N8ZIMQYPVS | Answers questions | 3-5s |
| **Data Retrieval** | HSSKM4JAUB | Fetches FHIR data | 1-2s |

---

## 📁 Project Structure

```
Healthcare Hackathon 2k25/
├── frontend/              # React app
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── services/      # API clients
│   │   └── store/         # State management
│   └── package.json
│
├── backend/               # FastAPI app
│   ├── app/
│   │   ├── api/routes/    # API endpoints
│   │   ├── services/      # Business logic
│   │   └── models/        # Data models
│   └── requirements.txt
│
├── infrastructure/        # AWS CDK (deployment)
│   ├── stacks/            # CDK stacks
│   └── app.py
│
├── agent_config.json      # Agent IDs
├── docker-compose.yml     # Local deployment
└── README.md
```

---

## 🚀 Quick Start

### Local Development (Docker)
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### AWS Deployment (Blocked by IAM)
```bash
cd infrastructure
cdk deploy --all
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/patients` | GET | List patients |
| `/api/patients/{id}` | GET | Patient details |
| `/api/patients/{id}/summary` | GET | Patient summary |
| `/api/reports/generate` | POST | Generate report |
| `/api/qa/ask` | POST | Ask question |
| `/api/medical-data/{id}` | GET | Medical data |

---

## 📊 FHIR Resources (10 Types)

| Resource | Count | What It Contains |
|----------|-------|------------------|
| Patient | 120+ | Demographics, contact |
| Condition | 500+ | Diagnoses, diseases |
| Observation | 2000+ | Vital signs, labs |
| MedicationRequest | 300+ | Prescriptions |
| Encounter | 800+ | Healthcare visits |
| Procedure | 400+ | Medical procedures |
| AllergyIntolerance | 150+ | Allergies |
| Immunization | 600+ | Vaccinations |
| DiagnosticReport | 200+ | Lab reports |
| CarePlan | 100+ | Treatment plans |

---

## 🔄 Report Generation Flow

```
User clicks "Generate Report"
    ↓
FastAPI Backend
    ↓
Get patient data from HealthLake
    ↓
Invoke 3 specialists in parallel:
    - Cardiologist (5-8s)
    - Radiologist (5-8s)
    - Endocrinologist (5-8s)
    ↓
Invoke Orchestrator (5-8s)
    ↓
Return comprehensive report
    ↓
Display in 4 tabs:
    - Comprehensive
    - Cardiology
    - Radiology
    - Endocrinology

Total: 20-25 seconds
```

---

## 💬 Q&A Flow

```
User types question
    ↓
FastAPI Backend
    ↓
Check for cached report
    ↓
Invoke Q&A Agent with context
    ↓
Return formatted answer (3-5s)
    ↓
Display in chat interface
```

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `agent_config.json` | All agent IDs |
| `docker-compose.yml` | Local deployment |
| `.env` | AWS credentials |
| `frontend/src/App.js` | React root |
| `backend/app/main.py` | FastAPI root |
| `backend/app/services/bedrock_service.py` | Agent invocation |
| `backend/app/services/healthlake_service.py` | FHIR queries |

---

## 🛠️ Tech Stack

### Frontend
- React 18.2.0
- Material-UI 5.15.0
- Zustand 4.4.7
- Recharts 2.10.3
- Axios 1.6.2

### Backend
- FastAPI 0.109.0
- Pydantic 2.5.3
- Boto3 1.34.34
- Uvicorn 0.27.0

### AWS
- Bedrock (Claude 3 Sonnet)
- HealthLake (FHIR R4)
- Lambda (future)
- API Gateway (future)
- S3 (future)
- DynamoDB (future)

---

## 📝 Common Commands

### Development
```bash
# Start Docker
docker-compose up --build

# Stop Docker
docker-compose down

# Rebuild frontend
cd frontend && npm run build

# Run backend locally
cd backend && uvicorn app.main:app --reload

# Run frontend locally
cd frontend && npm start
```

### Testing
```bash
# Test all agents
python test_multi_agent_system.py

# Test specific agent
python test_cardiologist_agent.py

# Test API
curl http://localhost:8000/api/health
```

### Deployment
```bash
# AWS CDK
cd infrastructure
cdk synth
cdk deploy --all

# Docker
docker-compose up --build
```

---

## 🔐 Environment Variables

```bash
# .env file
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_SESSION_TOKEN=xxx
AWS_REGION=us-west-2
HEALTHLAKE_DATASTORE_ID=xxx
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview |
| `COMPLETE_SYSTEM_ARCHITECTURE.md` | Full architecture |
| `SYSTEM_DIAGRAMS.md` | Visual diagrams |
| `MULTI_AGENTIC_SYSTEM_DESIGN.md` | Multi-agent design |
| `AWS_DEPLOYMENT_COMPLETE.md` | AWS deployment |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |

---

## 🎯 Key Features

✅ **Multi-Agent Reports**: 4 specialist agents  
✅ **Natural Language Q&A**: Context-aware responses  
✅ **Medical Visualizations**: ECG, MRI, charts  
✅ **Complete FHIR Coverage**: 10 resource types  
✅ **Real-time Updates**: Progress indicators  
✅ **Responsive Design**: Works on all devices  

---

## ⚡ Performance

| Operation | Time |
|-----------|------|
| Patient list | < 1s |
| Patient details | < 2s |
| Report generation | 20-25s |
| Q&A response | 3-5s |
| Medical data | 2-3s |

---

## 💰 Cost (AWS Deployment)

| Service | Monthly |
|---------|---------|
| Bedrock | $10-20 |
| Lambda | $5-10 |
| API Gateway | $3-5 |
| S3 | $1-2 |
| DynamoDB | $1-2 |
| CloudFront | $1-5 |
| **Total** | **$22-46** |

---

## 🐛 Troubleshooting

### Frontend not loading
```bash
cd frontend
rm -rf node_modules
npm install
npm start
```

### Backend not responding
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker issues
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### AWS credentials expired
Get new credentials from AWS Console → Command line access

---

## 📞 Quick Links

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **GitHub**: (your repo URL)

---

## ✅ Status

| Component | Status |
|-----------|--------|
| Frontend | ✅ Working |
| Backend | ✅ Working |
| Docker | ✅ Working |
| 5 AI Agents | ✅ Deployed |
| HealthLake | ✅ Configured |
| AWS Deployment | ⏳ Ready (IAM blocked) |

---

**Version**: 2.0  
**Last Updated**: January 2025  
**Status**: Production Ready (Local)
