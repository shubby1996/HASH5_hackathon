import boto3
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = 'HSSKM4JAUB'
LAMBDA_NAME = 'HealthLakeQueryFunction'
REGION = 'us-west-2'

def add_lambda_permission():
    """Grant Bedrock permission to invoke Lambda"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    try:
        lambda_client.add_permission(
            FunctionName=LAMBDA_NAME,
            StatementId='AllowBedrockInvoke',
            Action='lambda:InvokeFunction',
            Principal='bedrock.amazonaws.com',
            SourceArn=f'arn:aws:bedrock:{REGION}:891450252216:agent/{AGENT_ID}'
        )
        print("Added Lambda permission for Bedrock")
    except lambda_client.exceptions.ResourceConflictException:
        print("Permission already exists")

if __name__ == "__main__":
    add_lambda_permission()
