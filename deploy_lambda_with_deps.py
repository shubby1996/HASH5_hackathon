import boto3
import zipfile
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Install requests to a temp directory
print("Installing dependencies...")
subprocess.run(['pip', 'install', 'requests', '-t', 'lambda_package'], check=True)

# Create deployment package
print("Creating deployment package...")
with zipfile.ZipFile('lambda_package.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add lambda function
    zipf.write('lambda_function.py')
    
    # Add dependencies
    for root, dirs, files in os.walk('lambda_package'):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, 'lambda_package')
            zipf.write(file_path, arcname)

# Update Lambda
print("Updating Lambda function...")
lambda_client = boto3.client('lambda', region_name='us-west-2')

with open('lambda_package.zip', 'rb') as f:
    lambda_client.update_function_code(
        FunctionName='HealthLakeQueryFunction',
        ZipFile=f.read()
    )

print("Lambda updated successfully!")

# Cleanup
import shutil
shutil.rmtree('lambda_package', ignore_errors=True)
