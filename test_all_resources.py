import boto3
import uuid
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
AGENT_ALIAS_ID = 'TSTALIASID'
REGION = 'us-west-2'

def invoke_agent(prompt):
    """Invoke Bedrock Agent"""
    runtime = boto3.client('bedrock-agent-runtime', region_name=REGION)
    session_id = str(uuid.uuid4())
    
    response = runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=prompt
    )
    
    completion = ""
    for event in response.get('completion', []):
        if 'chunk' in event:
            chunk = event['chunk']
            if 'bytes' in chunk:
                completion += chunk['bytes'].decode('utf-8')
    
    return completion

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING EXPANDED AGENT - ALL 10 HEALTHLAKE RESOURCES")
    print("=" * 80)
    
    test_queries = [
        ("Patients", "Show me a list of patients"),
        ("Conditions", "What medical conditions are in the system?"),
        ("Observations", "What vital signs are available?"),
        ("Medications", "Show me medication prescriptions"),
        ("Encounters", "List healthcare visits"),
        ("Procedures", "What medical procedures are recorded?"),
        ("Allergies", "Show me patient allergies"),
        ("Immunizations", "What vaccination records are available?"),
        ("Diagnostic Reports", "Show me lab reports"),
        ("Care Plans", "What treatment plans are in the system?")
    ]
    
    for resource, query in test_queries:
        print(f"\n{'='*80}")
        print(f"Testing: {resource}")
        print(f"Query: {query}")
        print("-" * 80)
        
        try:
            result = invoke_agent(query)
            print(result[:500] + "..." if len(result) > 500 else result)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("TESTING COMPLETE!")
    print("=" * 80)
