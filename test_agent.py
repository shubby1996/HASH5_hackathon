import boto3
import json
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
REGION = 'us-west-2'

def prepare_agent():
    """Prepare the agent for use"""
    bedrock = boto3.client('bedrock-agent', region_name=REGION)
    
    print("Preparing agent...")
    bedrock.prepare_agent(agentId=AGENT_ID)
    
    # Wait for preparation
    while True:
        response = bedrock.get_agent(agentId=AGENT_ID)
        status = response['agent']['agentStatus']
        print(f"Status: {status}")
        
        if status in ['PREPARED', 'FAILED']:
            break
        time.sleep(3)
    
    return status == 'PREPARED'

def create_agent_alias():
    """Create an alias for the agent"""
    bedrock = boto3.client('bedrock-agent', region_name=REGION)
    
    try:
        response = bedrock.create_agent_alias(
            agentId=AGENT_ID,
            agentAliasName='prod',
            description='Production alias'
        )
        alias_id = response['agentAlias']['agentAliasId']
        print(f"Created alias: {alias_id}")
        
        # Wait for alias to be ready
        time.sleep(5)
        return alias_id
    except bedrock.exceptions.ConflictException:
        aliases = bedrock.list_agent_aliases(agentId=AGENT_ID)
        alias_id = aliases['agentAliasSummaries'][0]['agentAliasId']
        print(f"Using existing alias: {alias_id}")
        return alias_id

def invoke_agent(prompt, alias_id):
    """Invoke the agent with a prompt"""
    runtime = boto3.client('bedrock-agent-runtime', region_name=REGION)
    
    session_id = str(uuid.uuid4())
    
    response = runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=alias_id,
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
    print("=" * 60)
    print("TESTING BEDROCK AGENT WITH HEALTHLAKE")
    print("=" * 60)
    
    # Step 1: Prepare agent
    print("\nStep 1: Preparing agent...")
    if prepare_agent():
        print("Agent prepared successfully!")
    else:
        print("Agent preparation failed!")
        exit(1)
    
    # Step 2: Create alias
    print("\nStep 2: Creating agent alias...")
    alias_id = create_agent_alias()
    
    # Step 3: Test queries
    print("\n" + "=" * 60)
    print("TESTING QUERIES")
    print("=" * 60)
    
    test_queries = [
        "Show me a list of patients",
        "What medical conditions are in the system?",
        "What are the vital signs and observations available?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 60)
        result = invoke_agent(query, alias_id)
        print(f"Response: {result}")
    
    print("\n" + "=" * 60)
    print("Agent is ready! You can now query HealthLake data.")
    print("=" * 60)
