import boto3
import json
from dotenv import load_dotenv

load_dotenv()

def create_agent_role():
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "bedrock.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        response = iam.create_role(
            RoleName='BedrockAgentRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for Bedrock Agent'
        )
        
        iam.attach_role_policy(
            RoleName='BedrockAgentRole',
            PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
        )
        
        print(f"Role created: {response['Role']['Arn']}")
        return response['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName='BedrockAgentRole')
        print(f"Role already exists: {role['Role']['Arn']}")
        return role['Role']['Arn']

if __name__ == "__main__":
    role_arn = create_agent_role()
    print(f"\nAdd this to your .env file:")
    print(f"BEDROCK_AGENT_ROLE_ARN={role_arn}")
