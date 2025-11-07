import boto3
import json
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
REGION = 'us-west-2'

def update_agent_action_group():
    """Update agent action group with new schema"""
    bedrock = boto3.client('bedrock-agent', region_name=REGION)
    
    # Get existing action group
    action_groups = bedrock.list_agent_action_groups(
        agentId=AGENT_ID,
        agentVersion='DRAFT'
    )
    
    action_group_id = action_groups['actionGroupSummaries'][0]['actionGroupId']
    
    # Load new schema
    with open('agent_schema.json', 'r') as f:
        schema = json.load(f)
    
    # Update action group
    lambda_arn = 'arn:aws:lambda:us-west-2:891450252216:function:HealthLakeQueryFunction'
    
    response = bedrock.update_agent_action_group(
        agentId=AGENT_ID,
        agentVersion='DRAFT',
        actionGroupId=action_group_id,
        actionGroupName='HealthLakeActions',
        actionGroupExecutor={'lambda': lambda_arn},
        apiSchema={'payload': json.dumps(schema)},
        description='Query all patient health data from HealthLake - 10 resource types'
    )
    
    print(f"Updated action group: {action_group_id}")
    return response

def prepare_agent():
    """Prepare agent with updated actions"""
    bedrock = boto3.client('bedrock-agent', region_name=REGION)
    
    print("Preparing agent...")
    bedrock.prepare_agent(agentId=AGENT_ID)
    print("Agent prepared successfully!")

if __name__ == "__main__":
    print("Updating agent with all 10 HealthLake resources...")
    update_agent_action_group()
    prepare_agent()
    print("\nAgent now has access to:")
    print("1. Patient")
    print("2. Condition")
    print("3. Observation")
    print("4. MedicationRequest")
    print("5. Encounter")
    print("6. Procedure")
    print("7. AllergyIntolerance")
    print("8. Immunization")
    print("9. DiagnosticReport")
    print("10. CarePlan")
