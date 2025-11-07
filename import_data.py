import boto3
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class HealthLakeImporter:
    def __init__(self, datastore_id, region='us-west-2'):
        self.datastore_id = datastore_id
        self.client = boto3.client('healthlake', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        self.region = region
    
    def check_import_jobs(self):
        """Check existing import jobs"""
        try:
            response = self.client.list_fhir_import_jobs(DatastoreId=self.datastore_id)
            return response.get('ImportJobPropertiesList', [])
        except Exception as e:
            return f"Error: {str(e)}"
    
    def start_import_from_s3(self, s3_uri, role_arn):
        """Start import job from S3"""
        try:
            response = self.client.start_fhir_import_job(
                DatastoreId=self.datastore_id,
                InputDataConfig={
                    'S3Uri': s3_uri
                },
                JobOutputDataConfig={
                    'S3Configuration': {
                        'S3Uri': s3_uri.rsplit('/', 1)[0] + '/output/',
                        'KmsKeyId': 'AWS_OWNED_KMS_KEY'
                    }
                },
                DataAccessRoleArn=role_arn
            )
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_aws_open_data(self):
        """Check for FHIR datasets in AWS Open Data Registry"""
        print("Checking AWS Open Data Registry for FHIR datasets...\n")
        
        # Known FHIR datasets on AWS
        datasets = [
            {
                'name': 'MIMIC-IV Clinical Database',
                'description': 'De-identified health data from ICU patients',
                'bucket': 'physionet-open',
                'fhir': False
            },
            {
                'name': 'CMS Medicare Data',
                'description': 'Medicare claims data',
                'bucket': 'cms-public-data',
                'fhir': False
            },
            {
                'name': 'SYNTHEA Sample Data',
                'description': 'Synthetic patient data in FHIR format',
                'url': 'https://synthetichealth.github.io/synthea-sample-data/downloads/',
                'fhir': True
            }
        ]
        
        return datasets
    
    def download_synthea_sample(self, output_path='synthea_sample.zip'):
        """Download SYNTHEA sample data"""
        url = 'https://synthetichealth.github.io/synthea-sample-data/downloads/latest/synthea_sample_data_fhir_latest.zip'
        
        print(f"Downloading SYNTHEA sample data from: {url}")
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded to: {output_path}")
                return output_path
            else:
                return f"Error: HTTP {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    importer = HealthLakeImporter('b1f04342d94dcc96c47f9528f039f5a8')
    
    print("=" * 60)
    print("HEALTHLAKE DATA IMPORT OPTIONS")
    print("=" * 60)
    
    # Check existing import jobs
    print("\n1. Checking existing import jobs...")
    jobs = importer.check_import_jobs()
    if isinstance(jobs, list):
        print(f"   Found {len(jobs)} import jobs")
        for job in jobs[:3]:
            print(f"   - Job ID: {job.get('JobId')}")
            print(f"     Status: {job.get('JobStatus')}")
    else:
        print(f"   {jobs}")
    
    # Check AWS Open Data
    print("\n2. Available FHIR datasets:")
    datasets = importer.check_aws_open_data()
    for ds in datasets:
        print(f"\n   - {ds['name']}")
        print(f"     {ds['description']}")
        print(f"     FHIR Format: {'Yes' if ds['fhir'] else 'No'}")
        if 'url' in ds:
            print(f"     URL: {ds['url']}")
    
    # Download SYNTHEA sample
    print("\n3. Downloading SYNTHEA sample data...")
    result = importer.download_synthea_sample()
    print(f"   Result: {result}")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("1. Extract the downloaded SYNTHEA data")
    print("2. Upload FHIR bundles to S3")
    print("3. Create IAM role for HealthLake import")
    print("4. Start import job using start_import_from_s3()")
