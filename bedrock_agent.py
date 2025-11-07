import boto3
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

class BedrockAgent:
    def __init__(self, region_name='us-west-2'):
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=region_name)
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region_name)
        self.iam = boto3.client('iam', region_name=region_name)
    
    def create_agent(self, agent_name, instruction, role_arn=None):
        """Create a Bedrock Agent"""
        if not role_arn:
            role_arn = os.getenv('BEDROCK_AGENT_ROLE_ARN')
        
        response = self.bedrock_agent.create_agent(
            agentName=agent_name,
            agentResourceRoleArn=role_arn,
            foundationModel='anthropic.claude-3-sonnet-20240229-v1:0',
            instruction=instruction
        )
        return response['agent']
    
    def prepare_agent(self, agent_id):
        """Prepare agent for use"""
        response = self.bedrock_agent.prepare_agent(agentId=agent_id)
        
        # Wait for agent to be prepared
        while True:
            status = self.bedrock_agent.get_agent(agentId=agent_id)
            if status['agent']['agentStatus'] == 'PREPARED':
                break
            time.sleep(2)
        
        return response
    
    def invoke_agent(self, agent_id, agent_alias_id, session_id, prompt):
        """Invoke the agent with a prompt"""
        response = self.bedrock_agent_runtime.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=prompt
        )
        
        completion = ""
        for event in response.get("completion"):
            chunk = event.get("chunk")
            if chunk:
                completion += chunk.get("bytes").decode()
        
        return completion

if __name__ == "__main__":
    agent = BedrockAgent()
    
    # Example: Create agent
    print("Creating Bedrock Agent...")
    agent_config = agent.create_agent(
        agent_name="healthcare-assistant",
        instruction="You are a helpful healthcare assistant that provides information about medical topics."
    )
    print(f"Agent created: {agent_config['agentId']}")
