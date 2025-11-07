import boto3
import json
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DATASTORE_ID = 'b1f04342d94dcc96c47f9528f039f5a8'
REGION = 'us-west-2'

def search_healthlake(resource_type, count=100):
    """Search HealthLake FHIR resources"""
    endpoint = f"https://healthlake.{REGION}.amazonaws.com/datastore/{DATASTORE_ID}/r4/"
    
    session = boto3.Session(region_name=REGION)
    credentials = session.get_credentials()
    
    url = f"{endpoint}{resource_type}?_count={count}"
    request = AWSRequest(method='GET', url=url)
    SigV4Auth(credentials, 'healthlake', REGION).add_auth(request)
    
    response = requests.get(url, headers=dict(request.headers))
    return response.json()

def analyze_resource_schema(resource_type):
    """Analyze schema of a resource type"""
    data = search_healthlake(resource_type, count=50)
    
    fields = defaultdict(set)
    sample = None
    
    for entry in data.get('entry', [])[:10]:
        resource = entry['resource']
        if not sample:
            sample = resource
        
        for key in resource.keys():
            fields[key].add(type(resource[key]).__name__)
    
    return {
        'total': data.get('total', 0),
        'fields': {k: list(v) for k, v in fields.items()},
        'sample': sample
    }

if __name__ == "__main__":
    print("=" * 80)
    print("HEALTHLAKE FHIR SCHEMA ANALYSIS")
    print("=" * 80)
    
    resource_types = [
        'Patient', 'Observation', 'Condition', 'MedicationRequest',
        'Encounter', 'Procedure', 'AllergyIntolerance', 'Immunization',
        'DiagnosticReport', 'CarePlan'
    ]
    
    schema_summary = {}
    
    for resource_type in resource_types:
        print(f"\n{'='*80}")
        print(f"Resource: {resource_type}")
        print('='*80)
        
        try:
            schema = analyze_resource_schema(resource_type)
            schema_summary[resource_type] = schema
            
            print(f"Total Records: {schema['total']}")
            print(f"\nFields ({len(schema['fields'])}):")
            for field, types in sorted(schema['fields'].items()):
                print(f"  - {field}: {', '.join(types)}")
            
            if schema['sample']:
                print(f"\nSample Record:")
                print(json.dumps(schema['sample'], indent=2)[:500] + "...")
        
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Save schema to file
    with open('healthlake_schema.json', 'w') as f:
        json.dump(schema_summary, f, indent=2, default=str)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    for resource_type, schema in schema_summary.items():
        if schema['total'] > 0:
            print(f"{resource_type}: {schema['total']} records, {len(schema['fields'])} fields")
    
    print("\nFull schema saved to: healthlake_schema.json")
