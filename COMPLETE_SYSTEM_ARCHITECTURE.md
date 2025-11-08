# HealthLake AI Assistant - Complete System Architecture

**Project**: HASH5 Healthcare Hackathon 2025  
**Version**: 2.0 (React + FastAPI Migration)  
**Last Updated**: January 2025

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Multi-Agent System](#multi-agent-system)
6. [Technology Stack](#technology-stack)
7. [Deployment Options](#deployment-options)
8. [Security & Compliance](#security--compliance)

---

## 🎯 System Overview

### Purpose
AI-powered healthcare assistant that enables doctors to:
- Query patient health data using natural language
- Generate comprehensive medical reports from 4 specialist AI agents
- Ask questions about patient data with context-aware responses
- Visualize medical data (ECG, MRI, vital signs)

### Key Features
- ✅ **10 FHIR Resource Types**: Complete HealthLake coverage
- ✅ **5 AI Agents**: Specialized medical analysis
- ✅ **Natural Language**: Plain English queries
- ✅ **Multi-Agent Reports**: Cardiologist, Radiologist, Endocrinologist, Orchestrator
- ✅ **Interactive Q&A**: Context-aware conversation
- ✅ **Medical Visualizations**: ECG waveforms, MRI images, charts

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (SPA)                        │  │
│  │  - Material-UI components                                │  │
│  │  - Zustand state management                              │  │
│  │  - Recharts visualizations                               │  │
│  │  - Axios HTTP client                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend (REST API)                  │  │
│  │  - Pydantic models                                       │  │
│  │  - Async endpoints                                       │  │
│  │  - CORS middleware                                       │  │
│  │  - Service layer pattern                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕ AWS SDK
┌─────────────────────────────────────────────────────────────────┐
│                     AI/ML LAYER                                 │
│                                                                 │
│  ┌──────────────┬──────────────┬──────────────┬─────────────┐  │
│  │ Cardiologist │ Radiologist  │Endocrinologist│Orchestrator │  │
│  │    Agent     │    Agent     │    Agent      │   Agent     │  │
│  │ (CDMSLUEUFQ) │ (K0MU8VCNSK) │ (0GRU0APJFO)  │(C5XRILWF9L) │  │
│  └──────────────┴──────────────┴──────────────┴─────────────┘  │
│  ┌──────────────┬──────────────────────────────────────────┐   │
│  │  Q&A Agent   │  Data Retrieval Agent                    │   │
│  │ (N8ZIMQYPVS) │  (HSSKM4JAUB)                            │   │
│  └──────────────┴──────────────────────────────────────────┘   │
│                                                                 │
│  All powered by: AWS Bedrock (Claude 3 Sonnet)                 │
└─────────────────────────────────────────────────────────────────┘
                              ↕ FHIR API
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           AWS HealthLake (FHIR R4 Datastore)             │  │
│  │  - 10 FHIR Resource Types                                │  │
│  │  - SYNTHEA synthetic patient data                        │  │
│  │  - 120+ patients with complete medical history           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Storage (Future/Optional)                      │  │
│  │  - DynamoDB: Q&A conversation history                    │  │
│  │  - S3: Generated reports, ECG images, MRI files          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Component Details

### 1. Frontend (React)

**Location**: `frontend/`

**Structure**:
```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.js          # Patient statistics & charts
│   │   ├── PatientList.js        # Patient selection
│   │   ├── PatientDetails.js     # Patient demographics
│   │   ├── ReportViewer.js       # Multi-agent reports
│   │   ├── QAInterface.js        # Q&A chat
│   │   └── MedicalDataView.js    # Visualizations
│   ├── pages/
│   │   └── Home.js               # Main application page
│   ├── services/
│   │   ├── patientService.js     # Patient API calls
│   │   ├── reportService.js      # Report generation
│   │   └── qaService.js          # Q&A API calls
│   ├── store/
│   │   └── useStore.js           # Zustand global state
│   ├── App.js                    # Root component
│   └── index.js                  # Entry point
├── public/
│   └── index.html
└── package.json
```

**Key Technologies**:
- React 18.2.0
- Material-UI 5.15.0
- Zustand 4.4.7 (state management)
- Recharts 2.10.3 (charts)
- Axios 1.6.2 (HTTP)
- React Router 6.20.0

**Features**:
- Responsive design
- Real-time updates
- Progress indicators
- Error handling
- Tab-based navigation

---

### 2. Backend (FastAPI)

**Location**: `backend/`

**Structure**:
```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── health.py         # Health check
│   │       ├── patients.py       # Patient endpoints
│   │       ├── reports.py        # Report generation
│   │       ├── qa.py             # Q&A endpoints
│   │       └── medical_data.py   # Medical data endpoints
│   ├── core/
│   │   └── config.py             # Configuration
│   ├── models/
│   │   ├── patient.py            # Patient models
│   │   ├── report.py             # Report models
│   │   └── qa.py                 # Q&A models
│   ├── services/
│   │   ├── bedrock_service.py    # Bedrock agent invocation
│   │   ├── healthlake_service.py # HealthLake queries
│   │   ├── qa_service.py         # Q&A logic
│   │   └── storage_service.py    # S3/DynamoDB (future)
│   └── main.py                   # FastAPI app
├── lambda_handler.py             # AWS Lambda wrapper
├── Dockerfile
└── requirements.txt
```

**Key Technologies**:
- FastAPI 0.109.0
- Pydantic 2.5.3 (validation)
- Boto3 1.34.34 (AWS SDK)
- Uvicorn 0.27.0 (ASGI server)
- Mangum 0.17.0 (Lambda adapter)

**API Endpoints**:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/patients` | GET | List all patients |
| `/api/patients/{id}` | GET | Get patient details |
| `/api/patients/{id}/summary` | GET | Patient summary |
| `/api/reports/generate` | POST | Generate multi-agent report |
| `/api/qa/ask` | POST | Ask question about patient |
| `/api/qa/history/{patient_id}` | GET | Get Q&A history |
| `/api/medical-data/{patient_id}` | GET | Get medical data |

---

### 3. Multi-Agent System (AWS Bedrock)

**5 Specialized AI Agents**:

#### Agent 1: Data Retrieval Agent
- **ID**: HSSKM4JAUB
- **Purpose**: Fetch FHIR data from HealthLake
- **Capabilities**: 
  - Search patients
  - Search conditions
  - Search observations
  - Search medications
  - Search encounters
  - Search procedures
  - Search allergies
  - Search immunizations
  - Search diagnostic reports
  - Search care plans

#### Agent 2: Cardiologist Agent
- **ID**: CDMSLUEUFQ
- **Purpose**: Cardiac health analysis
- **Analyzes**:
  - ECG waveforms
  - Blood pressure
  - Cardiac conditions (AFib, MI, heart failure)
  - Cardiac medications
  - Cardiac MRI/imaging
  - Heart rate variability
- **Output**: Cardiac assessment with risk stratification

#### Agent 3: Radiologist Agent
- **ID**: K0MU8VCNSK
- **Purpose**: Medical imaging interpretation
- **Analyzes**:
  - MRI images and reports
  - DiagnosticReport resources
  - Imaging findings
  - Anatomical abnormalities
- **Output**: Radiology report with findings

#### Agent 4: Endocrinologist Agent
- **ID**: 0GRU0APJFO
- **Purpose**: Metabolic/endocrine health
- **Analyzes**:
  - Lab results (glucose, HbA1c, thyroid)
  - Diabetes conditions
  - Metabolic observations
  - Endocrine medications
  - Hormone levels
- **Output**: Metabolic health assessment

#### Agent 5: Orchestrator Agent
- **ID**: C5XRILWF9L
- **Purpose**: Coordinate specialists & generate final report
- **Process**:
  1. Receives specialist reports
  2. Identifies critical findings
  3. Generates executive summary
  4. Creates action plan
  5. Consolidates recommendations
- **Output**: Comprehensive integrated report

#### Agent 6: Q&A Agent
- **ID**: N8ZIMQYPVS
- **Purpose**: Answer questions about patient data
- **Features**:
  - Context-aware responses
  - Uses cached reports
  - Conversational interface
  - Medical terminology

---

### 4. Data Layer (AWS HealthLake)

**FHIR R4 Datastore**:
- **Datastore ID**: (configured in .env)
- **Region**: us-west-2
- **Data Source**: SYNTHEA synthetic data

**10 FHIR Resource Types**:

| Resource | Count | Description |
|----------|-------|-------------|
| Patient | 120+ | Demographics, contact info |
| Condition | 500+ | Medical diagnoses |
| Observation | 2000+ | Vital signs, lab results |
| MedicationRequest | 300+ | Prescriptions |
| Encounter | 800+ | Healthcare visits |
| Procedure | 400+ | Medical procedures |
| AllergyIntolerance | 150+ | Patient allergies |
| Immunization | 600+ | Vaccination records |
| DiagnosticReport | 200+ | Lab reports |
| CarePlan | 100+ | Treatment plans |

**Special Patients**:
- **Sarah Johnson** (6df562fc-25a7-4e72-8753-9583e3259572)
  - Atrial fibrillation
  - ECG waveform data
  - Cardiac MRI
  - Complete medical history

---

## 🔄 Data Flow

### Flow 1: Patient Selection
```
User clicks patient
    ↓
React: useStore.setSelectedPatient()
    ↓
API: GET /api/patients/{id}
    ↓
FastAPI: patients.py → healthlake_service.py
    ↓
HealthLake: FHIR API query
    ↓
Response: Patient demographics
    ↓
React: Display patient details
```

### Flow 2: Report Generation
```
User clicks "Generate Report"
    ↓
React: reportService.generateReport(patientId)
    ↓
API: POST /api/reports/generate
    ↓
FastAPI: reports.py → bedrock_service.py
    ↓
Bedrock: Invoke 4 agents in parallel
    ├─→ Cardiologist Agent (5-8s)
    ├─→ Radiologist Agent (5-8s)
    └─→ Endocrinologist Agent (5-8s)
    ↓
Wait for all agents to complete
    ↓
Bedrock: Invoke Orchestrator Agent (5-8s)
    ↓
Orchestrator: Aggregate & synthesize
    ↓
Response: Comprehensive report (JSON)
    ↓
React: Display in tabs
    - Comprehensive
    - Cardiology
    - Radiology
    - Endocrinology
```

**Total Time**: 20-25 seconds

### Flow 3: Q&A Interaction
```
User types question
    ↓
React: qaService.askQuestion(patientId, question)
    ↓
API: POST /api/qa/ask
    ↓
FastAPI: qa.py → qa_service.py
    ↓
Check for cached report (in-memory)
    ↓
Bedrock: Invoke Q&A Agent with context
    ↓
Q&A Agent: Generate answer (3-5s)
    ↓
Response: Answer with formatting
    ↓
React: Display in chat interface
    ↓
Store in conversation history
```

### Flow 4: Medical Data Visualization
```
User clicks "Medical Data" tab
    ↓
React: medicalDataService.getMedicalData(patientId)
    ↓
API: GET /api/medical-data/{patient_id}
    ↓
FastAPI: medical_data.py → healthlake_service.py
    ↓
HealthLake: Query multiple resources
    ├─→ Observations (vital signs)
    ├─→ Conditions (diagnoses)
    ├─→ Medications
    └─→ DiagnosticReports
    ↓
Response: Aggregated medical data
    ↓
React: Render visualizations
    ├─→ Recharts: Line charts (vital signs)
    ├─→ Recharts: Bar charts (conditions)
    ├─→ Tables: Medications, allergies
    └─→ Images: ECG, MRI
```

---

## 💻 Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework |
| Material-UI | 5.15.0 | Component library |
| Zustand | 4.4.7 | State management |
| Recharts | 2.10.3 | Data visualization |
| Axios | 1.6.2 | HTTP client |
| React Router | 6.20.0 | Routing |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.109.0 | Web framework |
| Pydantic | 2.5.3 | Data validation |
| Boto3 | 1.34.34 | AWS SDK |
| Uvicorn | 0.27.0 | ASGI server |
| Mangum | 0.17.0 | Lambda adapter |

### AWS Services
| Service | Purpose |
|---------|---------|
| AWS Bedrock | AI agents (Claude 3 Sonnet) |
| AWS HealthLake | FHIR data storage |
| AWS Lambda | Serverless compute (future) |
| AWS API Gateway | REST API (future) |
| AWS S3 | Report storage (future) |
| AWS DynamoDB | Q&A history (future) |
| AWS CloudFront | CDN (future) |

### Development Tools
| Tool | Purpose |
|------|---------|
| Docker | Containerization |
| Docker Compose | Local orchestration |
| Git | Version control |
| Python 3.12 | Backend language |
| Node.js 18+ | Frontend tooling |
| npm | Package management |

---

## 🚀 Deployment Options

### Option 1: Local Development (Docker)
**Status**: ✅ Working

```bash
docker-compose up --build
```

**Access**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Pros**:
- Fast development
- No AWS costs
- Full control

**Cons**:
- Not publicly accessible
- Requires Docker running
- Computer must stay on

---

### Option 2: AWS Deployment (CDK)
**Status**: ⏳ Ready (IAM restrictions prevent deployment)

**Architecture**:
```
CloudFront → S3 (Frontend)
API Gateway → Lambda (Backend)
DynamoDB (Q&A history)
S3 (Reports)
```

**Deployment**:
```bash
cd infrastructure
cdk deploy --all
```

**Pros**:
- Publicly accessible
- Auto-scaling
- High availability
- Pay-per-use

**Cons**:
- Requires full AWS permissions
- Monthly costs ($12-45)
- More complex

**Blocked By**: IAM restrictions (WSParticipantRole)

---

### Option 3: Hybrid (Frontend Public, Backend Local)

**Deploy frontend to Netlify/Vercel**:
```bash
cd frontend
npm run build
netlify deploy --prod
```

**Expose backend with ngrok**:
```bash
ngrok http 8000
```

**Update frontend config**:
```bash
REACT_APP_API_URL=https://your-ngrok-url.ngrok.io
```

**Pros**:
- Frontend publicly accessible
- Works with restricted AWS account
- Low cost

**Cons**:
- Backend must stay running locally
- ngrok URL changes on restart

---

## 🔐 Security & Compliance

### Authentication & Authorization
- **Current**: No authentication (demo/hackathon)
- **Future**: AWS Cognito for user management

### Data Encryption
- ✅ **In Transit**: HTTPS/TLS
- ✅ **At Rest**: S3 encryption, DynamoDB encryption
- ✅ **HealthLake**: HIPAA-compliant storage

### IAM Permissions
**Backend Lambda Role** (future):
- HealthLake: Read-only
- Bedrock: InvokeAgent only
- DynamoDB: Read/Write on specific table
- S3: Read/Write on specific bucket
- CloudWatch: Logs only

### HIPAA Compliance
- ✅ AWS HealthLake is HIPAA-eligible
- ✅ AWS Bedrock is HIPAA-eligible
- ⚠️ Need BAA (Business Associate Agreement)
- ⚠️ Need audit logging (CloudTrail)
- ⚠️ Need access controls

### Data Privacy
- No PHI stored in frontend
- No PHI in logs
- Session-based data only
- No persistent storage (currently)

---

## 📊 Performance Metrics

### Response Times
| Operation | Time | Notes |
|-----------|------|-------|
| Patient list | < 1s | Cached in frontend |
| Patient details | < 2s | HealthLake query |
| Report generation | 20-25s | 4 agents in parallel |
| Q&A response | 3-5s | Single agent |
| Medical data | 2-3s | Multiple HealthLake queries |

### Scalability
- **Current**: Single user (local)
- **AWS**: 1000+ concurrent users
- **Bottleneck**: Bedrock agent invocations

### Cost (AWS Deployment)
| Service | Monthly Cost |
|---------|--------------|
| Bedrock | $0.003/1K tokens (~$10-20) |
| HealthLake | Existing |
| Lambda | $5-10 |
| API Gateway | $3-5 |
| S3 | $1-2 |
| DynamoDB | $1-2 |
| CloudFront | $1-5 |
| **Total** | **$22-46/month** |

---

## 🎯 Key Design Decisions

### Why Multi-Agent System?
- **Specialization**: Each agent focuses on one domain
- **Accuracy**: Domain-specific prompts reduce hallucinations
- **Modularity**: Easy to add/remove specialists
- **Parallel Processing**: Faster than sequential

### Why FastAPI?
- **Performance**: Async support, fast
- **Developer Experience**: Auto docs, type hints
- **Modern**: Python 3.12 features
- **AWS Compatible**: Works with Lambda (Mangum)

### Why React?
- **Component-Based**: Reusable UI components
- **Ecosystem**: Rich library ecosystem
- **Performance**: Virtual DOM, efficient updates
- **Developer Experience**: Hot reload, debugging

### Why HealthLake?
- **FHIR Standard**: Interoperable
- **HIPAA Compliant**: Healthcare-ready
- **Managed Service**: No infrastructure
- **AWS Integration**: Works with Bedrock

---

## 📈 Future Enhancements

### Short Term
- [ ] Add authentication (Cognito)
- [ ] Persist Q&A history (DynamoDB)
- [ ] Store reports (S3)
- [ ] PDF export
- [ ] Email notifications

### Medium Term
- [ ] More specialists (Neurologist, Oncologist)
- [ ] Real-time collaboration
- [ ] Mobile app
- [ ] Voice interface
- [ ] Integration with EHR systems

### Long Term
- [ ] Predictive analytics
- [ ] Clinical decision support
- [ ] Population health management
- [ ] Research data export
- [ ] Multi-language support

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview & setup |
| `COMPLETE_SYSTEM_ARCHITECTURE.md` | This document |
| `MULTI_AGENTIC_SYSTEM_DESIGN.md` | Multi-agent design |
| `MULTI_AGENT_IMPLEMENTATION_SUMMARY.md` | Agent implementation |
| `AWS_DEPLOYMENT_COMPLETE.md` | AWS deployment guide |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |
| `ARCHITECTURE.md` | AWS architecture |
| `HEALTHLAKE_SCHEMA_SUMMARY.md` | FHIR schema reference |
| `agent_capabilities.md` | Agent capabilities |

---

## 🔗 Quick Links

- **Frontend Code**: `frontend/src/`
- **Backend Code**: `backend/app/`
- **Agent Config**: `agent_config.json`
- **Docker Compose**: `docker-compose.yml`
- **CDK Infrastructure**: `infrastructure/`

---

**Document Version**: 1.0  
**Created**: January 2025  
**Status**: Production Ready (Local), AWS Ready (Blocked by IAM)
