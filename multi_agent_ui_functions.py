import boto3
import json
import uuid

REGION = 'us-west-2'

# Load agent config
with open('agent_config.json', 'r') as f:
    AGENT_CONFIG = json.load(f)

def invoke_specialist_agent(agent_type, patient_data):
    """Invoke a specialist agent"""
    runtime = boto3.client('bedrock-agent-runtime', region_name=REGION)
    
    agent_id = AGENT_CONFIG[f'{agent_type}_agent']['agent_id']
    alias_id = AGENT_CONFIG[f'{agent_type}_agent']['alias_id']
    
    response = runtime.invoke_agent(
        agentId=agent_id,
        agentAliasId=alias_id,
        sessionId=str(uuid.uuid4()),
        inputText=patient_data
    )
    
    completion = ""
    for event in response.get('completion', []):
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                completion += chunk['bytes'].decode('utf-8')
    
    return completion

def generate_comprehensive_report(patient_id, patient_name, patient_summary, progress_callback=None):
    """Generate comprehensive medical report using multi-agent system"""
    
    # Prepare data for each specialist
    cardiac_data = f"""
Patient: {patient_name}
Patient ID: {patient_id}

CARDIAC DATA:
- Conditions: {', '.join(patient_summary.get('conditions', ['None']))}
- Has ECG: {'Yes' if patient_summary.get('has_ecg') else 'No'}

Analyze cardiac health.
"""
    
    imaging_data = f"""
Patient: {patient_name}
Patient ID: {patient_id}

IMAGING DATA:
- MRI Reports: {len(patient_summary.get('mri_reports', []))}
- MRI Images: {len(patient_summary.get('mri_images', []))}

Analyze imaging findings.
"""
    
    metabolic_data = f"""
Patient: {patient_name}
Patient ID: {patient_id}

METABOLIC DATA:
- Medications: {', '.join(patient_summary.get('medications', ['None']))}
- Allergies: {', '.join(patient_summary.get('allergies', ['None']))}

Analyze metabolic health.
"""
    
    # Invoke specialists
    if progress_callback:
        progress_callback("Step 1/4: Consulting Cardiologist...")
    cardio_report = invoke_specialist_agent('cardiologist', cardiac_data)
    
    if progress_callback:
        progress_callback("Step 2/4: Consulting Radiologist...")
    radio_report = invoke_specialist_agent('radiologist', imaging_data)
    
    if progress_callback:
        progress_callback("Step 3/4: Consulting Endocrinologist...")
    endo_report = invoke_specialist_agent('endocrinologist', metabolic_data)
    
    # Invoke orchestrator
    if progress_callback:
        progress_callback("Step 4/4: Generating Comprehensive Report...")
    orchestrator_input = f"""
Patient: {patient_name} (ID: {patient_id})

CARDIOLOGY SUMMARY:
{cardio_report[:500]}...

RADIOLOGY SUMMARY:
{radio_report[:500]}...

ENDOCRINOLOGY SUMMARY:
{endo_report[:500]}...

Generate comprehensive integrated report.
"""
    
    final_report = invoke_specialist_agent('orchestrator', orchestrator_input)
    
    return {
        'cardiology': cardio_report,
        'radiology': radio_report,
        'endocrinology': endo_report,
        'comprehensive': final_report
    }
