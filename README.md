# HealthLake AI Assistant - HASH5 Hackathon

AI-powered healthcare assistant using AWS Bedrock Agent and HealthLake to query patient health data through natural language.

## 🏥 Features

- **Complete FHIR Coverage**: Access all 10 HealthLake resource types
- **Natural Language Queries**: Ask questions in plain English
- **Bedrock Agent Integration**: Powered by Claude 3 Sonnet
- **Interactive UI**: Streamlit-based chat interface
- **Comprehensive Data**: Patients, conditions, medications, procedures, allergies, immunizations, lab reports, and more

## 📋 Prerequisites

- Python 3.12+
- AWS Account with access to:
  - AWS Bedrock (Claude 3 Sonnet model access)
  - AWS HealthLake
  - AWS Lambda
  - IAM permissions
- UV package manager (or pip)
- Git

## 🚀 Setup Instructions

### Step 1: Clone the Repository

```bash
git clone https://github.com/harshavadlamudi/HASH5_hackathon.git
cd HASH5_hackathon
```

### Step 2: Create Python Virtual Environment

**Using UV (Recommended):**
```bash
uv venv
```

**Using Python venv:**
```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

**Using UV:**
```bash
uv pip install -r requirements.txt
```

**Using pip:**
```bash
pip install -r requirements.txt
```

### Step 5: Configure AWS Credentials

Create a `.env` file in the project root:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=your_session_token_here
AWS_REGION=us-west-2
BEDROCK_AGENT_ROLE_ARN=arn:aws:iam::YOUR_ACCOUNT:role/BedrockAgentRole
```

**To get AWS credentials:**
1. Go to AWS Console
2. Click your username → "Command line or programmatic access"
3. Copy the credentials for your OS
4. Paste into `.env` file

### Step 6: Set Up AWS HealthLake

**Check if HealthLake exists:**
```bash
python -c "import boto3; from dotenv import load_dotenv; load_dotenv(); client = boto3.client('healthlake', region_name='us-west-2'); print(client.list_fhir_datastores())"
```

**If no datastore exists, create one:**
- Go to AWS Console → HealthLake
- Create a new datastore (FHIR R4)
- Enable SYNTHEA preload data
- Note the Datastore ID

**Update the Datastore ID in these files:**
- `explore_healthlake.py` (line 7)
- `lambda_function.py` (line 7)
- `analyze_schema.py` (line 9)

### Step 7: Deploy Lambda Function

```bash
python deploy_agent.py
```

This will:
- Create IAM roles
- Deploy Lambda function
- Create Bedrock Agent
- Set up action groups

**Note the Agent ID and Alias ID from the output.**

### Step 8: Update Agent Configuration

Update `app.py` and `test_agent.py` with your Agent ID and Alias ID:

```python
AGENT_ID = 'YOUR_AGENT_ID'
AGENT_ALIAS_ID = 'YOUR_ALIAS_ID'
```

### Step 9: Grant Lambda Permissions

```bash
python fix_permissions.py
```

### Step 10: Test the Agent

```bash
python test_all_resources.py
```

You should see successful responses for all 10 resource types.

### Step 11: Run the Streamlit UI

```bash
streamlit run app.py
```

Or use the batch file (Windows):
```bash
run_app.bat
```

The app will open in your browser at `http://localhost:8501`

## 📊 Available Resources

The agent can query these 10 FHIR resource types:

1. **Patient** - Demographics, contact info
2. **Condition** - Medical diagnoses
3. **Observation** - Vital signs, lab results
4. **MedicationRequest** - Prescriptions
5. **Encounter** - Healthcare visits
6. **Procedure** - Medical procedures
7. **AllergyIntolerance** - Patient allergies
8. **Immunization** - Vaccination records
9. **DiagnosticReport** - Lab reports
10. **CarePlan** - Treatment plans

## 💬 Example Queries

```
- "Show me a list of patients"
- "What medical conditions are in the system?"
- "Show me medication prescriptions"
- "List healthcare visits"
- "What allergies do patients have?"
- "Show me vaccination records"
- "Display lab reports"
- "What treatment plans exist?"
- "Find patients with COVID-19"
- "Show me vital signs for patient X"
```

## 🗂️ Project Structure

```
HASH5_hackathon/
├── app.py                          # Streamlit UI
├── bedrock_client.py               # Bedrock API client
├── bedrock_agent.py                # Agent management
├── lambda_function.py              # Lambda handler for HealthLake queries
├── agent_schema.json               # OpenAPI schema for agent
├── explore_healthlake.py           # HealthLake data explorer
├── visualize_healthlake.py         # Data visualization
├── analyze_schema.py               # Schema analysis
├── deploy_agent.py                 # Deployment script
├── test_all_resources.py           # Test all resources
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔧 Troubleshooting

### Issue: "Unable to locate credentials"
**Solution:** Make sure `.env` file exists and contains valid AWS credentials.

### Issue: "Access denied to Bedrock"
**Solution:** Enable Claude 3 Sonnet model access in AWS Console → Bedrock → Model access.

### Issue: "Lambda function not found"
**Solution:** Run `python deploy_agent.py` to create the Lambda function.

### Issue: "Agent returns empty responses"
**Solution:** 
1. Check Lambda CloudWatch logs for errors
2. Verify HealthLake datastore has data
3. Run `python fix_permissions.py`

### Issue: "HealthLake datastore not found"
**Solution:** Update the `DATASTORE_ID` in the Python files with your actual datastore ID.

## 📚 Additional Scripts

### Explore HealthLake Data
```bash
python explore_healthlake.py
```

### Visualize Data
```bash
python visualize_healthlake.py
```

### Analyze Schema
```bash
python analyze_schema.py
python schema_report.py
```

### Import Additional Data
```bash
python import_data.py
python process_and_import.py
```

## 🔐 Security Notes

- Never commit `.env` file to Git
- Rotate AWS credentials regularly
- Use IAM roles with least privilege
- Enable CloudTrail for audit logging
- Review Lambda execution logs

## 📖 Documentation

- `HEALTHLAKE_SCHEMA_SUMMARY.md` - Complete FHIR schema reference
- `agent_capabilities.md` - Agent capabilities overview
- `AGENT_EXPANSION_COMPLETE.md` - Expansion details
- `data_summary.md` - Data import summary

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for the HASH5 Hackathon.

## 👥 Team

HASH5 - Healthcare Hackathon 2025

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review AWS CloudWatch logs
3. Check HealthLake datastore status
4. Verify IAM permissions

## 🚀 AWS Deployment (NEW!)

### Deploy to AWS with CDK

We now have a **React + FastAPI** version that can be deployed to AWS!

**Quick Deploy:**
```bash
cd infrastructure
deploy.bat  # Windows
# or
./deploy.sh  # Mac/Linux
```

**What gets deployed:**
- ✅ React frontend (S3 + CloudFront)
- ✅ FastAPI backend (Lambda + API Gateway)
- ✅ DynamoDB (Q&A history)
- ✅ S3 (Reports storage)

**Documentation:**
- `AWS_DEPLOYMENT_COMPLETE.md` - Full deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `DEPLOYMENT_SUMMARY.md` - Quick summary
- `infrastructure/README.md` - CDK infrastructure docs

### Docker Deployment (Local)

**Run locally with Docker:**
```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

See `DEPLOYMENT.md` for details.

## 🎯 Next Steps

1. ✅ Basic setup complete
2. ✅ Agent deployed
3. ✅ All resources accessible
4. ✅ React + FastAPI migration complete
5. ✅ Docker deployment ready
6. ✅ AWS CDK infrastructure ready
7. 🔄 Deploy to AWS (follow AWS_DEPLOYMENT_COMPLETE.md)

---

**Built with AWS Bedrock, HealthLake, Lambda, React, and FastAPI**
