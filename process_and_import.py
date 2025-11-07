import boto3
import json
import zipfile
import os
from dotenv import load_dotenv

load_dotenv()

def extract_synthea_data(zip_path='synthea_sample.zip', extract_to='synthea_data'):
    """Extract SYNTHEA zip file"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to: {extract_to}")
    
    # List FHIR files
    fhir_files = []
    for root, dirs, files in os.walk(extract_to):
        for file in files:
            if file.endswith('.json'):
                fhir_files.append(os.path.join(root, file))
    
    print(f"Found {len(fhir_files)} FHIR JSON files")
    return fhir_files

def upload_to_s3(fhir_files, bucket_name, prefix='fhir-import/'):
    """Upload FHIR files to S3"""
    s3 = boto3.client('s3')
    
    # Create bucket if needed
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Using existing bucket: {bucket_name}")
    except:
        print(f"Creating bucket: {bucket_name}")
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': os.getenv('AWS_REGION', 'us-west-2')}
        )
    
    # Upload files
    uploaded = []
    for i, file_path in enumerate(fhir_files[:10], 1):  # Upload first 10 files
        key = prefix + os.path.basename(file_path)
        print(f"Uploading {i}/{min(10, len(fhir_files))}: {os.path.basename(file_path)}")
        s3.upload_file(file_path, bucket_name, key)
        uploaded.append(f"s3://{bucket_name}/{key}")
    
    return uploaded

def create_import_role():
    """Create IAM role for HealthLake import"""
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "healthlake.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket", "s3:PutObject"],
                "Resource": ["arn:aws:s3:::*"]
            }
        ]
    }
    
    try:
        role = iam.create_role(
            RoleName='HealthLakeImportRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        
        iam.put_role_policy(
            RoleName='HealthLakeImportRole',
            PolicyName='HealthLakeS3Access',
            PolicyDocument=json.dumps(policy_document)
        )
        
        print(f"Created role: {role['Role']['Arn']}")
        return role['Role']['Arn']
    except iam.exceptions.EntityAlreadyExistsException:
        role = iam.get_role(RoleName='HealthLakeImportRole')
        print(f"Using existing role: {role['Role']['Arn']}")
        return role['Role']['Arn']

def start_import(datastore_id, s3_uri, role_arn):
    """Start HealthLake import job"""
    client = boto3.client('healthlake', region_name='us-west-2')
    
    response = client.start_fhir_import_job(
        DatastoreId=datastore_id,
        InputDataConfig={'S3Uri': s3_uri},
        JobOutputDataConfig={
            'S3Configuration': {
                'S3Uri': s3_uri.rsplit('/', 1)[0] + '/output/',
                'KmsKeyId': 'AWS_OWNED_KMS_KEY'
            }
        },
        DataAccessRoleArn=role_arn
    )
    
    return response

if __name__ == "__main__":
    print("=" * 60)
    print("IMPORTING SYNTHEA DATA TO HEALTHLAKE")
    print("=" * 60)
    
    # Step 1: Extract
    print("\nStep 1: Extracting SYNTHEA data...")
    fhir_files = extract_synthea_data()
    
    # Step 2: Upload to S3
    print("\nStep 2: Uploading to S3...")
    bucket_name = f"healthlake-import-{boto3.client('sts').get_caller_identity()['Account']}"
    uploaded = upload_to_s3(fhir_files, bucket_name)
    print(f"Uploaded {len(uploaded)} files")
    
    # Step 3: Create role
    print("\nStep 3: Creating IAM role...")
    role_arn = create_import_role()
    
    # Step 4: Start import
    print("\nStep 4: Starting import job...")
    s3_uri = f"s3://{bucket_name}/fhir-import/"
    result = start_import('b1f04342d94dcc96c47f9528f039f5a8', s3_uri, role_arn)
    
    print(f"\nImport job started!")
    print(f"Job ID: {result['JobId']}")
    print(f"Status: {result['JobStatus']}")
