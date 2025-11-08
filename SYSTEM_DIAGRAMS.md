# HealthLake AI Assistant - System Diagrams

Visual representations of the system architecture.

---

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                          END USERS                                  │
│                    (Doctors, Healthcare Staff)                      │
│                                                                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                             │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    React Frontend (SPA)                       │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬─────────────┐ │  │
│  │  │Dashboard │ Patient  │ Report   │   Q&A    │Medical Data │ │  │
│  │  │          │  List    │  Viewer  │Interface │    View     │ │  │
│  │  └──────────┴──────────┴──────────┴──────────┴─────────────┘ │  │
│  │                                                               │  │
│  │  State Management: Zustand                                   │  │
│  │  UI Library: Material-UI                                     │  │
│  │  Charts: Recharts                                            │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             │ REST API (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   FastAPI Backend                             │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬─────────────┐ │  │
│  │  │ Health   │ Patients │ Reports  │   Q&A    │Medical Data │ │  │
│  │  │ Routes   │  Routes  │  Routes  │  Routes  │   Routes    │ │  │
│  │  └──────────┴──────────┴──────────┴──────────┴─────────────┘ │  │
│  │                           ↕                                   │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬─────────────┐ │  │
│  │  │ Bedrock  │HealthLake│   Q&A    │ Storage  │   Config    │ │  │
│  │  │ Service  │ Service  │ Service  │ Service  │   Service   │ │  │
│  │  └──────────┴──────────┴──────────┴──────────┴─────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             │ AWS SDK (Boto3)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         AI/ML LAYER                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                   AWS Bedrock Agents                          │  │
│  │                   (Claude 3 Sonnet)                           │  │
│  │                                                               │  │
│  │  ┌──────────────┬──────────────┬──────────────┬───────────┐ │  │
│  │  │ Cardiologist │ Radiologist  │Endocrinologist│Orchestrator│ │  │
│  │  │    Agent     │    Agent     │    Agent      │   Agent    │ │  │
│  │  │ CDMSLUEUFQ   │ K0MU8VCNSK   │ 0GRU0APJFO    │C5XRILWF9L │ │  │
│  │  └──────────────┴──────────────┴──────────────┴───────────┘ │  │
│  │                                                               │  │
│  │  ┌──────────────┬──────────────────────────────────────────┐ │  │
│  │  │  Q&A Agent   │  Data Retrieval Agent                    │ │  │
│  │  │ N8ZIMQYPVS   │  HSSKM4JAUB                              │ │  │
│  │  └──────────────┴──────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             │ FHIR API (HTTPS)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │              AWS HealthLake (FHIR R4 Datastore)               │  │
│  │                                                               │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬───────────┐  │  │
│  │  │ Patient  │Condition │Observation│Medication│ Encounter │  │  │
│  │  │  (120+)  │  (500+)  │  (2000+)  │  (300+)  │   (800+)  │  │  │
│  │  └──────────┴──────────┴──────────┴──────────┴───────────┘  │  │
│  │                                                               │  │
│  │  ┌──────────┬──────────┬──────────┬──────────┬───────────┐  │  │
│  │  │Procedure │ Allergy  │Immunization│Diagnostic│ CarePlan │  │  │
│  │  │  (400+)  │  (150+)  │   (600+)  │  (200+)  │  (100+)  │  │  │
│  │  └──────────┴──────────┴──────────┴──────────┴───────────┘  │  │
│  │                                                               │  │
│  │  Data Source: SYNTHEA Synthetic Patient Data                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Agent Report Generation Flow

```
┌──────────────┐
│     User     │
│ Clicks       │
│ "Generate    │
│  Report"     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│              React Frontend                              │
│  reportService.generateReport(patientId)                 │
└──────┬───────────────────────────────────────────────────┘
       │
       │ POST /api/reports/generate
       ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
│  reports.py → bedrock_service.py                         │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Get patient summary from HealthLake
       ▼
┌──────────────────────────────────────────────────────────┐
│              AWS HealthLake                              │
│  Returns: Demographics, conditions, meds, etc.           │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Prepare data for specialists
       ▼
┌──────────────────────────────────────────────────────────┐
│         Parallel Agent Invocation (ThreadPool)           │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │Cardiologist │  │ Radiologist │  │Endocrinologist│    │
│  │   Agent     │  │   Agent     │  │    Agent      │    │
│  │             │  │             │  │               │    │
│  │ Analyzes:   │  │ Analyzes:   │  │ Analyzes:     │    │
│  │ - ECG       │  │ - MRI       │  │ - Labs        │    │
│  │ - BP        │  │ - CT        │  │ - Glucose     │    │
│  │ - Cardiac   │  │ - X-ray     │  │ - Hormones    │    │
│  │   conditions│  │ - Reports   │  │ - Metabolic   │    │
│  │             │  │             │  │   data        │    │
│  │ Time: 5-8s  │  │ Time: 5-8s  │  │ Time: 5-8s    │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬────────┘    │
│         │                │                 │             │
│         └────────────────┼─────────────────┘             │
│                          │                               │
└──────────────────────────┼───────────────────────────────┘
                           │
                           │ All reports ready
                           ▼
┌──────────────────────────────────────────────────────────┐
│              Orchestrator Agent                          │
│  C5XRILWF9L                                              │
│                                                          │
│  Receives:                                               │
│  - Cardiology report                                     │
│  - Radiology report                                      │
│  - Endocrinology report                                  │
│                                                          │
│  Generates:                                              │
│  - Executive summary                                     │
│  - Critical findings                                     │
│  - Integrated assessment                                 │
│  - Action plan                                           │
│  - Consolidated recommendations                          │
│                                                          │
│  Time: 5-8s                                              │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Return comprehensive report
       ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
│  Returns JSON with 4 sections:                           │
│  - comprehensive                                         │
│  - cardiology                                            │
│  - radiology                                             │
│  - endocrinology                                         │
└──────┬───────────────────────────────────────────────────┘
       │
       │ HTTP Response
       ▼
┌──────────────────────────────────────────────────────────┐
│              React Frontend                              │
│  Display in tabs:                                        │
│  [Comprehensive] [Cardiology] [Radiology] [Endocrinology]│
│                                                          │
│  Total Time: 20-25 seconds                               │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Q&A Interaction Flow

```
┌──────────────┐
│     User     │
│ Types        │
│ Question     │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│              React Frontend                              │
│  qaService.askQuestion(patientId, question)              │
└──────┬───────────────────────────────────────────────────┘
       │
       │ POST /api/qa/ask
       │ { patientId, question, conversationHistory }
       ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
│  qa.py → qa_service.py                                   │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Check for cached report
       ▼
┌──────────────────────────────────────────────────────────┐
│         In-Memory Report Cache                           │
│  If report exists: Use as context                        │
│  If not: Generate summary from HealthLake                │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Prepare context + question
       ▼
┌──────────────────────────────────────────────────────────┐
│              Q&A Agent (N8ZIMQYPVS)                      │
│                                                          │
│  Input:                                                  │
│  - Patient context (demographics, conditions, meds)      │
│  - Previous conversation history                         │
│  - Current question                                      │
│                                                          │
│  Processing:                                             │
│  - Understand question intent                            │
│  - Extract relevant information from context             │
│  - Generate natural language answer                      │
│  - Format with markdown                                  │
│                                                          │
│  Time: 3-5 seconds                                       │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Return formatted answer
       ▼
┌──────────────────────────────────────────────────────────┐
│              FastAPI Backend                             │
│  Returns: { answer, timestamp }                          │
└──────┬───────────────────────────────────────────────────┘
       │
       │ HTTP Response
       ▼
┌──────────────────────────────────────────────────────────┐
│              React Frontend                              │
│  Display in chat interface:                              │
│                                                          │
│  User: "What medications is the patient taking?"         │
│  AI:   "The patient is currently taking..."              │
│                                                          │
│  Store in conversation history                           │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Data Retrieval Agent Flow

```
┌──────────────────────────────────────────────────────────┐
│         Any Agent (Cardiologist, Radiologist, etc.)      │
│  Needs patient data                                      │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Invoke Data Retrieval Agent
       ▼
┌──────────────────────────────────────────────────────────┐
│         Data Retrieval Agent (HSSKM4JAUB)                │
│                                                          │
│  Capabilities:                                           │
│  - /search-patients                                      │
│  - /search-conditions                                    │
│  - /search-observations                                  │
│  - /search-medications                                   │
│  - /search-encounters                                    │
│  - /search-procedures                                    │
│  - /search-allergies                                     │
│  - /search-immunizations                                 │
│  - /search-diagnostic-reports                            │
│  - /search-care-plans                                    │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Invoke Lambda function
       ▼
┌──────────────────────────────────────────────────────────┐
│         Lambda Function (HealthLake Query)               │
│  lambda_function.py                                      │
│                                                          │
│  Handlers:                                               │
│  - search_patients_handler()                             │
│  - search_conditions_handler()                           │
│  - search_observations_handler()                         │
│  - ... (10 total handlers)                               │
└──────┬───────────────────────────────────────────────────┘
       │
       │ FHIR API Query
       ▼
┌──────────────────────────────────────────────────────────┐
│         AWS HealthLake                                   │
│  FHIR R4 Datastore                                       │
│                                                          │
│  Query: GET /Patient?_id=xxx                             │
│  Response: FHIR Bundle with resources                    │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Return FHIR data
       ▼
┌──────────────────────────────────────────────────────────┐
│         Lambda Function                                  │
│  Parse and format FHIR data                              │
│  Return structured JSON                                  │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Return to agent
       ▼
┌──────────────────────────────────────────────────────────┐
│         Data Retrieval Agent                             │
│  Returns formatted data to calling agent                 │
└──────┬───────────────────────────────────────────────────┘
       │
       │ Use data for analysis
       ▼
┌──────────────────────────────────────────────────────────┐
│         Specialist Agent                                 │
│  Analyzes data and generates report                      │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Components                         │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Dashboard │  │ Patient  │  │ Report   │  │   Q&A    │       │
│  │          │  │  List    │  │  Viewer  │  │Interface │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │              │             │
│       └─────────────┼──────────────┼──────────────┘             │
│                     │              │                            │
│                     ▼              ▼                            │
│              ┌─────────────────────────┐                        │
│              │   Zustand Store         │                        │
│              │  - selectedPatient      │                        │
│              │  - patients             │                        │
│              │  - reports              │                        │
│              │  - qaHistory            │                        │
│              └──────────┬──────────────┘                        │
│                         │                                       │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Services                                 │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │patientService│  │reportService │  │  qaService   │         │
│  │              │  │              │  │              │         │
│  │ - getAll()   │  │ - generate() │  │ - ask()      │         │
│  │ - getById()  │  │ - getById()  │  │ - getHistory()│        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │                 │
│         └─────────────────┼──────────────────┘                 │
│                           │                                    │
│                           ▼                                    │
│                    ┌─────────────┐                             │
│                    │    Axios    │                             │
│                    │ HTTP Client │                             │
│                    └──────┬──────┘                             │
│                           │                                    │
└───────────────────────────┼────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Routes                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ health.py│  │patients.py│  │reports.py│  │  qa.py   │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │              │             │
│       └─────────────┼──────────────┼──────────────┘             │
│                     │              │                            │
│                     ▼              ▼                            │
│              ┌─────────────────────────┐                        │
│              │   Service Layer         │                        │
│              │  - bedrock_service      │                        │
│              │  - healthlake_service   │                        │
│              │  - qa_service           │                        │
│              └──────────┬──────────────┘                        │
│                         │                                       │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AWS Services                                │
│                                                                 │
│  ┌──────────────┐                  ┌──────────────┐            │
│  │AWS Bedrock   │                  │AWS HealthLake│            │
│  │  (6 Agents)  │                  │ (FHIR Data)  │            │
│  └──────────────┘                  └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Deployment Architecture (Docker)

```
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Host                                │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              docker-compose.yml                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────┐  ┌─────────────────────────────┐ │
│  │  Frontend Container     │  │  Backend Container          │ │
│  │  ┌───────────────────┐  │  │  ┌───────────────────────┐ │ │
│  │  │  Node.js 18       │  │  │  │  Python 3.12          │ │ │
│  │  │  React App        │  │  │  │  FastAPI              │ │ │
│  │  │  Port: 3000       │  │  │  │  Uvicorn              │ │ │
│  │  │                   │  │  │  │  Port: 8000           │ │ │
│  │  └───────────────────┘  │  │  └───────────────────────┘ │ │
│  └─────────────────────────┘  └─────────────────────────────┘ │
│              │                              │                  │
│              │                              │                  │
│              └──────────────┬───────────────┘                  │
│                             │                                  │
└─────────────────────────────┼──────────────────────────────────┘
                              │
                              │ Network: healthlake-network
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS Cloud                                  │
│                                                                 │
│  ┌──────────────┐                  ┌──────────────┐            │
│  │AWS Bedrock   │                  │AWS HealthLake│            │
│  │  (Agents)    │                  │ (FHIR Data)  │            │
│  └──────────────┘                  └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Future AWS Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Users                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CloudFront (CDN)                             │
│  - Global edge locations                                        │
│  - HTTPS enforcement                                            │
│  - Caching                                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    S3 Bucket (Frontend)                         │
│  - Static website hosting                                       │
│  - React build files                                            │
│  - Private bucket (OAI access)                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          Users                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS (API Calls)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway (REST)                           │
│  - CORS enabled                                                 │
│  - Request validation                                           │
│  - Throttling                                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Lambda Function                              │
│  - Docker container (FastAPI)                                   │
│  - 15-minute timeout                                            │
│  - 1024 MB memory                                               │
│  - IAM role attached                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┬────────────────┐
        │                │                │                │
        ▼                ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│AWS Bedrock   │  │AWS HealthLake│  │  DynamoDB    │  │     S3       │
│  (Agents)    │  │ (FHIR Data)  │  │ (Q&A History)│  │  (Reports)   │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

**Document Version**: 1.0  
**Created**: January 2025  
**Purpose**: Visual system architecture reference
