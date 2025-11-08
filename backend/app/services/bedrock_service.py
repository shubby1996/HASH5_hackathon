import boto3
import json
import uuid
from app.core.config import settings

class BedrockService:
    def __init__(self):
        self.runtime = boto3.client(
            'bedrock-agent-runtime',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION
        )
        
        # Load agent config
        with open('agent_config.json', 'r') as f:
            self.config = json.load(f)
    
    def invoke_agent(self, agent_type: str, input_text: str) -> str:
        """Invoke a Bedrock agent"""
        agent_id = self.config[f'{agent_type}_agent']['agent_id']
        alias_id = self.config[f'{agent_type}_agent']['alias_id']
        
        response = self.runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId=str(uuid.uuid4()),
            inputText=input_text
        )
        
        completion = ""
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    completion += chunk['bytes'].decode('utf-8')
        
        return completion
    
    def generate_comprehensive_report(self, patient_id: str, patient_summary: dict, progress_callback=None) -> dict:
        """Generate comprehensive report using all specialist agents"""
        
        # Prepare data for each specialist
        cardiac_data = f"""
Patient: {patient_summary.get('name')}
Patient ID: {patient_id}

CARDIAC DATA:
- Conditions: {', '.join(patient_summary.get('conditions', ['None']))}
- Has ECG: {'Yes' if patient_summary.get('has_ecg') else 'No'}

Analyze cardiac health.
"""
        
        imaging_data = f"""
Patient: {patient_summary.get('name')}
Patient ID: {patient_id}

IMAGING DATA:
- MRI Reports: {patient_summary.get('mri_reports_count', 0)}

Analyze imaging findings.
"""
        
        metabolic_data = f"""
Patient: {patient_summary.get('name')}
Patient ID: {patient_id}

METABOLIC DATA:
- Medications: {', '.join(patient_summary.get('medications', ['None']))}
- Allergies: {', '.join(patient_summary.get('allergies', ['None']))}

Analyze metabolic health.
"""
        
        # Invoke specialists
        if progress_callback:
            progress_callback("Step 1/4: Consulting Cardiologist...")
        cardio_report = self.invoke_agent('cardiologist', cardiac_data)
        
        if progress_callback:
            progress_callback("Step 2/4: Consulting Radiologist...")
        radio_report = self.invoke_agent('radiologist', imaging_data)
        
        if progress_callback:
            progress_callback("Step 3/4: Consulting Endocrinologist...")
        endo_report = self.invoke_agent('endocrinologist', metabolic_data)
        
        # Invoke orchestrator
        if progress_callback:
            progress_callback("Step 4/4: Generating Comprehensive Report...")
        
        orchestrator_input = f"""
Patient: {patient_summary.get('name')} (ID: {patient_id})

CARDIOLOGY SUMMARY:
{cardio_report[:500]}...

RADIOLOGY SUMMARY:
{radio_report[:500]}...

ENDOCRINOLOGY SUMMARY:
{endo_report[:500]}...

Generate comprehensive integrated report.
"""
        
        final_report = self.invoke_agent('orchestrator', orchestrator_input)
        
        return {
            'cardiology': cardio_report,
            'radiology': radio_report,
            'endocrinology': endo_report,
            'comprehensive': final_report
        }

bedrock_service = BedrockService()
