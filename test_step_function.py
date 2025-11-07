import boto3
import json
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

REGION = 'us-west-2'

# Load config
with open('agent_config.json', 'r') as f:
    config = json.load(f)

STATE_MACHINE_ARN = config['step_function']['arn']

def test_step_function():
    """Test Step Functions workflow"""
    sfn = boto3.client('stepfunctions', region_name=REGION)
    
    print("="*60)
    print("TESTING STEP FUNCTIONS WORKFLOW")
    print("="*60)
    print(f"\nState Machine: {STATE_MACHINE_ARN}")
    
    # Input for execution
    execution_input = {
        "patientId": "6df562fc-25a7-4e72-8753-9583e3259572",
        "patientName": "Sarah Johnson",
        "sessionId": str(uuid.uuid4())
    }
    
    print(f"\nStarting execution for patient: {execution_input['patientName']}")
    print(f"Session ID: {execution_input['sessionId']}")
    
    # Start execution
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(execution_input)
    )
    
    execution_arn = response['executionArn']
    print(f"\n[OK] Execution started: {execution_arn}")
    
    # Wait and check status
    print("\nWaiting for execution to complete...")
    print("(This may take 30-60 seconds for parallel specialist analysis)")
    
    while True:
        time.sleep(5)
        status_response = sfn.describe_execution(executionArn=execution_arn)
        status = status_response['status']
        
        print(f"  Status: {status}")
        
        if status in ['SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED']:
            break
    
    print("\n" + "="*60)
    
    if status == 'SUCCEEDED':
        print("[SUCCESS] EXECUTION SUCCEEDED!")
        print("="*60)
        
        output = json.loads(status_response['output'])
        print("\nFINAL REPORT:")
        print(json.dumps(output, indent=2))
        
    else:
        print(f"[FAILED] EXECUTION {status}")
        print("="*60)
        if 'error' in status_response:
            print(f"Error: {status_response['error']}")
    
    return status_response

if __name__ == "__main__":
    test_step_function()
