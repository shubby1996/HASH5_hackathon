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

# Get first patient
patients = search_healthlake('Patient', {'_count': '1'})
if patients.get('entry'):
    patient_id = patients['entry'][0]['resource']['id']
    print(f"Patient ID: {patient_id}\n")
    
    # Get all observations for this patient
    obs = search_healthlake('Observation', {'patient': patient_id, '_count': '50'})
    
    if obs.get('entry'):
        print(f"Found {len(obs['entry'])} observations\n")
        
        # Group by code
        codes = {}
        for entry in obs['entry']:
            r = entry['resource']
            code_text = r.get('code', {}).get('text', 'Unknown')
            code_code = r.get('code', {}).get('coding', [{}])[0].get('code', 'N/A')
            
            if code_text not in codes:
                codes[code_text] = {'code': code_code, 'count': 0, 'sample': r}
            codes[code_text]['count'] += 1
        
        print("Available Observation Types:")
        print("-" * 80)
        for code_text, data in sorted(codes.items(), key=lambda x: x[1]['count'], reverse=True):
            print(f"{code_text:50} | Code: {data['code']:15} | Count: {data['count']}")
            
            # Show sample data structure
            sample = data['sample']
            if 'valueQuantity' in sample:
                val = sample['valueQuantity']
                print(f"  → Value: {val.get('value')} {val.get('unit', '')}")
            elif 'component' in sample:
                print(f"  → Components: {len(sample['component'])}")
                for comp in sample['component'][:2]:
                    comp_name = comp.get('code', {}).get('text', 'Unknown')
                    if 'valueQuantity' in comp:
                        comp_val = comp['valueQuantity']
                        print(f"     - {comp_name}: {comp_val.get('value')} {comp_val.get('unit', '')}")
            print()
    else:
        print("No observations found")
else:
    print("No patients found")
