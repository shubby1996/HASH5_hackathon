import json
import boto3

def lambda_handler(event, context):
    """Lambda function to invoke Bedrock agents"""
    
    agent_id = event['agentId']
    alias_id = event['aliasId']
    session_id = event['sessionId']
    input_text = event['inputText']
    
    runtime = boto3.client('bedrock-agent-runtime', region_name='us-west-2')
    
    try:
        response = runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=alias_id,
            sessionId=session_id,
            inputText=input_text
        )
        
        completion = ""
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    completion += chunk['bytes'].decode('utf-8')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'completion': completion,
                'agentId': agent_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
