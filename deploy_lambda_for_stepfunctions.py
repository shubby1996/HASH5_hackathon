import boto3
import json
import zipfile
import io
import time
from dotenv import load_dotenv

load_dotenv()

REGION = 'us-west-2'

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
        role_response = iam.create_role(
            RoleName='InvokeBedrockAgentLambdaRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = role_response['Role']['Arn']
        print(f"[OK] Lambda role created: {role_arn}")
        
        # Attach policies
        iam.attach_role_policy(
            RoleName='InvokeBedrockAgentLambdaRole',
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        iam.attach_role_policy(
            RoleName='InvokeBedrockAgentLambdaRole',
            PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
        )
        print("[OK] Policies attached")
        
        time.sleep(10)
        return role_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_response = iam.get_role(RoleName='InvokeBedrockAgentLambdaRole')
        role_arn = role_response['Role']['Arn']
        print(f"[OK] Using existing role: {role_arn}")
        return role_arn

def deploy_lambda():
    """Deploy Lambda function"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    print("Creating Lambda function...")
    
    role_arn = create_lambda_role()
    
    # Create zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write('lambda_invoke_agent.py', 'lambda_function.py')
    
    zip_buffer.seek(0)
    
    try:
        response = lambda_client.create_function(
            FunctionName='InvokeBedrockAgent',
            Runtime='python3.12',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_buffer.read()},
            Timeout=300,
            MemorySize=512
        )
        
        function_arn = response['FunctionArn']
        print(f"[OK] Lambda created: {function_arn}")
        
        print("\n" + "="*50)
        print("LAMBDA FUNCTION DEPLOYED!")
        print("="*50)
        print(f"ARN: {function_arn}")
        
        return function_arn
        
    except lambda_client.exceptions.ResourceConflictException:
        print("[WARN] Lambda already exists, updating...")
        response = lambda_client.update_function_code(
            FunctionName='InvokeBedrockAgent',
            ZipFile=zip_buffer.read()
        )
        print(f"[OK] Lambda updated: {response['FunctionArn']}")
        return response['FunctionArn']
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

if __name__ == "__main__":
    deploy_lambda()
