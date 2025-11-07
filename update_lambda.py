import boto3
import zipfile
from dotenv import load_dotenv

load_dotenv()

# Create zip
with zipfile.ZipFile('lambda_package.zip', 'w') as zipf:
    zipf.write('lambda_function.py')

# Update Lambda
client = boto3.client('lambda', region_name='us-west-2')
with open('lambda_package.zip', 'rb') as f:
    client.update_function_code(
        FunctionName='HealthLakeQueryFunction',
        ZipFile=f.read()
    )

print("Lambda function updated successfully!")
