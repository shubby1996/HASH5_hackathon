import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import requests
from dotenv import load_dotenv

load_dotenv()

REGION = 'us-west-2'
DATASTORE_ID = 'b1f04342d94dcc96c47f9528f039f5a8'

def search_healthlake(resource_type, params=None):
    endpoint = f"https://healthlake.{REGION}.amazonaws.com/datastore/{DATASTORE_ID}/r4/"
    session = boto3.Session(region_name=REGION)
    credentials = session.get_credentials()
    
    url = f"{endpoint}{resource_type}"
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    request = AWSRequest(method='GET', url=url)
    SigV4Auth(credentials, 'healthlake', REGION).add_auth(request)
    
    response = requests.get(url, headers=dict(request.headers))
    return response.json()

# Search for vital signs observations
vital_codes = {
    '85354-9': 'Blood Pressure',
    '8867-4': 'Heart Rate',
    '8310-5': 'Body Temperature',
    '9279-1': 'Respiratory Rate',
    '2708-6': 'Oxygen Saturation',
    '29463-7': 'Body Weight',
    '8302-2': 'Body Height',
    '39156-5': 'BMI'
}

print("Searching for vital signs across all patients...\n")

for code, name in vital_codes.items():
    obs = search_healthlake('Observation', {'code': code, '_count': '5'})
    count = len(obs.get('entry', []))
    
    if count > 0:
        print(f"✓ {name:25} | Code: {code} | Found: {count}")
        sample = obs['entry'][0]['resource']
        
        if 'valueQuantity' in sample:
            val = sample['valueQuantity']
            print(f"  Sample: {val.get('value')} {val.get('unit', '')}")
        elif 'component' in sample:
            print(f"  Components:")
            for comp in sample['component']:
                comp_name = comp.get('code', {}).get('text', 'Unknown')
                if 'valueQuantity' in comp:
                    comp_val = comp['valueQuantity']
                    print(f"    - {comp_name}: {comp_val.get('value')} {comp_val.get('unit', '')}")
        print()
    else:
        print(f"✗ {name:25} | Code: {code} | Not found")
