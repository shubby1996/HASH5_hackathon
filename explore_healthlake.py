import boto3
import json
from dotenv import load_dotenv

load_dotenv()

class HealthLakeExplorer:
    def __init__(self, datastore_id, region='us-west-2'):
        self.datastore_id = datastore_id
        self.client = boto3.client('healthlake', region_name=region)
        self.endpoint = f"https://healthlake.{region}.amazonaws.com/datastore/{datastore_id}/r4/"
    
    def search_resources(self, resource_type, count=10):
        """Search for FHIR resources"""
        import requests
        from botocore.auth import SigV4Auth
        from botocore.awsrequest import AWSRequest
        import os
        
        session = boto3.Session(region_name=os.getenv('AWS_REGION', 'us-west-2'))
        credentials = session.get_credentials()
        
        url = f"{self.endpoint}{resource_type}?_count={count}"
        request = AWSRequest(method='GET', url=url)
        SigV4Auth(credentials, 'healthlake', 'us-west-2').add_auth(request)
        
        response = requests.get(url, headers=dict(request.headers))
        return response.json()
    
    def get_resource_counts(self):
        """Get counts of different resource types"""
        resource_types = ['Patient', 'Observation', 'Condition', 'Medication', 
                         'MedicationRequest', 'Procedure', 'Encounter', 'AllergyIntolerance']
        
        counts = {}
        for resource_type in resource_types:
            try:
                result = self.search_resources(resource_type, count=1)
                counts[resource_type] = result.get('total', 0)
            except Exception as e:
                counts[resource_type] = f"Error: {str(e)}"
        
        return counts

if __name__ == "__main__":
    explorer = HealthLakeExplorer('b1f04342d94dcc96c47f9528f039f5a8')
    
    print("=== HealthLake Data Summary ===\n")
    counts = explorer.get_resource_counts()
    
    for resource, count in counts.items():
        print(f"{resource}: {count}")
    
    print("\n=== Sample Patient Data ===")
    patients = explorer.search_resources('Patient', count=3)
    
    if 'entry' in patients:
        for entry in patients['entry'][:3]:
            patient = entry['resource']
            name = patient.get('name', [{}])[0]
            full_name = f"{name.get('given', [''])[0]} {name.get('family', '')}"
            gender = patient.get('gender', 'Unknown')
            birth_date = patient.get('birthDate', 'Unknown')
            print(f"\nPatient: {full_name}")
            print(f"  Gender: {gender}")
            print(f"  Birth Date: {birth_date}")
            print(f"  ID: {patient.get('id')}")
