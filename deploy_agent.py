import boto3
import json
import zipfile
import os
import time
from dotenv import load_dotenv

load_dotenv()

def create_lambda_package():
    """Create Lambda deployment package"""
    with zipfile.ZipFile('lambda_package.zip', 'w') as zipf:
        zipf.write('lambda_function.py')
    return 'lambda_package.zip'

def create_lambda_role():
    """Create IAM role for Lambda"""
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        role = iam.create_role(
            RoleName='HealthLakeLambdaRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        
        iam.attach_role_policy(
            RoleName='HealthLakeLambdaRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        iam.attach_role_policy(
            RoleName='HealthLakeLambdaRole',
            PolicyArn='arn:aws:iam::aws:policy/AmazonHealthLakeReadOnlyAccess'
        )
        
        print(f"Created Lambda role: {role['Role']['Arn']}")
        return role['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName='HealthLakeLambdaRole')
        print(f"Using existing Lambda role: {role['Role']['Arn']}")
        return role['Role']['Arn']

def deploy_lambda(role_arn):
    """Deploy Lambda function"""
    lambda_client = boto3.client('lambda', region_name='us-west-2')
    
    package_path = create_lambda_package()
    
    with open(package_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        response = lambda_client.create_function(
            FunctionName='HealthLakeQueryFunction',
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Timeout=30,
            MemorySize=256
        )
        print(f"Created Lambda: {response['FunctionArn']}")
        return response['FunctionArn']
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.get_function(FunctionName='HealthLakeQueryFunction')
        print(f"Using existing Lambda: {response['Configuration']['FunctionArn']}")
        return response['Configuration']['FunctionArn']

def setup_agent_action_group(agent_id, lambda_arn):
    """Add action group to agent"""
    bedrock = boto3.client('bedrock-agent', region_name='us-west-2')
    
    with open('agent_schema.json', 'r') as f:
        schema = json.load(f)
    
    try:
        response = bedrock.create_agent_action_group(
            agentId=agent_id,
            agentVersion='DRAFT',
            actionGroupName='HealthLakeActions',
            actionGroupExecutor={'lambda': lambda_arn},
            apiSchema={'payload': json.dumps(schema)},
            description='Query patient health data from HealthLake'
        )
        print(f"Created action group: {response['agentActionGroup']['actionGroupId']}")
        return response
    except Exception as e:
        print(f"Error creating action group: {str(e)}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("DEPLOYING BEDROCK AGENT WITH HEALTHLAKE")
    print("=" * 60)
    
    print("\nStep 1: Creating Lambda role...")
    lambda_role = create_lambda_role()
    
    print("\nStep 2: Waiting for role propagation...")
    time.sleep(10)
    
    print("\nStep 3: Deploying Lambda function...")
    lambda_arn = deploy_lambda(lambda_role)
    
    print("\nStep 4: Setting up agent action group...")
    agent_id = 'HSSKM4JAUB'
    setup_agent_action_group(agent_id, lambda_arn)
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT COMPLETE!")
    print("=" * 60)
    print(f"\nAgent ID: {agent_id}")
    print(f"Lambda ARN: {lambda_arn}")
    print("\nNext: Prepare and test the agent")
