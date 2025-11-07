import boto3
import json
import os
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from dotenv import load_dotenv

load_dotenv()

def import_fhir_bundle_directly(datastore_id, bundle_path, region='us-west-2'):
    """Import FHIR bundle directly via API"""
    endpoint = f"https://healthlake.{region}.amazonaws.com/datastore/{datastore_id}/r4/"
    
    session = boto3.Session(region_name=region)
    credentials = session.get_credentials()
    
    # Read bundle
    with open(bundle_path, 'r') as f:
        bundle = json.load(f)
    
    # POST bundle
    url = endpoint
    headers = {'Content-Type': 'application/fhir+json'}
    
    request = AWSRequest(method='POST', url=url, data=json.dumps(bundle), headers=headers)
    SigV4Auth(credentials, 'healthlake', region).add_auth(request)
    
    response = requests.post(url, data=json.dumps(bundle), headers=dict(request.headers))
    return response

if __name__ == "__main__":
    print("=" * 60)
    print("DIRECT FHIR IMPORT TO HEALTHLAKE")
    print("=" * 60)
    
    # Get first FHIR file
    fhir_dir = 'synthea_data'
    if os.path.exists(fhir_dir):
        files = [f for f in os.listdir(fhir_dir) if f.endswith('.json')]
        
        print(f"\nFound {len(files)} FHIR bundles")
        print(f"Importing first 5 bundles...\n")
        
        for i, file in enumerate(files[:5], 1):
            file_path = os.path.join(fhir_dir, file)
            print(f"{i}. Importing {file}...")
            
            try:
                response = import_fhir_bundle_directly(
                    'b1f04342d94dcc96c47f9528f039f5a8',
                    file_path
                )
                
                if response.status_code in [200, 201]:
                    print(f"   Success! Status: {response.status_code}")
                else:
                    print(f"   Failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
            except Exception as e:
                print(f"   Error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("Import complete! Run visualize_healthlake.py to see new data")
    else:
        print(f"Directory not found: {fhir_dir}")
        print("Run import_data.py first to download SYNTHEA data")
