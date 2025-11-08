import boto3
import json
import uuid
from app.core.config import settings

class QAService:
    def __init__(self):
        self.runtime = boto3.client(
            'bedrock-agent-runtime',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION
        )
        
        with open('agent_config.json', 'r') as f:
            self.config = json.load(f)
    
    def ask_question(self, question: str, cached_reports: dict) -> dict:
        """Ask Q&A agent about cached reports"""
        agent_id = self.config['qa_agent']['agent_id']
        alias_id = self.config['qa_agent']['alias_id']
        
        # Format context for Q&A agent
        context = self._format_context(cached_reports)
        
        prompt = f"""
{context}

USER QUESTION: {question}

Provide a clear, detailed answer in plain text. Do NOT use JSON format. Write in structured paragraphs with bullet points if needed. Be conversational and easy to understand.
"""
        
        response = self.runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId=str(uuid.uuid4()),
            inputText=prompt
        )
        
        completion = ""
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    completion += chunk['bytes'].decode('utf-8')
        
        # Remove apology lines
        lines = completion.split('\n')
        filtered_lines = [line for line in lines if not line.strip().lower().startswith('i apologize')]
        completion = '\n'.join(filtered_lines).strip()
        
        # Return plain text response
        return {
            'question': question,
            'answer': completion,
            'ui_type': 'text',
            'data': {},
            'sources': ['comprehensive'],
            'confidence': 'high'
        }
    
    def _format_context(self, cached_reports: dict) -> str:
        """Format cached reports as context"""
        patient_summary = cached_reports.get('patient_summary', {})
        
        context = f"""
PATIENT INFORMATION:
Name: {patient_summary.get('name', 'Unknown')}
Gender: {patient_summary.get('gender', 'Unknown')}
Birth Date: {patient_summary.get('birthDate', 'Unknown')}

CARDIOLOGY REPORT:
{cached_reports.get('cardiology', 'Not available')}

RADIOLOGY REPORT:
{cached_reports.get('radiology', 'Not available')}

ENDOCRINOLOGY REPORT:
{cached_reports.get('endocrinology', 'Not available')}

COMPREHENSIVE ANALYSIS:
{cached_reports.get('comprehensive', 'Not available')}
"""
        return context

qa_service = QAService()
