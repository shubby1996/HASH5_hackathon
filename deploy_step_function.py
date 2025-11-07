import boto3
import json
import time
from dotenv import load_dotenv

load_dotenv()

REGION = 'us-west-2'

def create_step_function_role():
    """Create IAM role for Step Functions"""
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "states.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    # Policy for invoking Bedrock agents
    bedrock_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent",
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }]
    }
    
    try:
        # Create role
        role_response = iam.create_role(
            RoleName='MultiAgentStepFunctionRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for Multi-Agent Step Function'
        )
        role_arn = role_response['Role']['Arn']
        print(f"[OK] IAM Role created: {role_arn}")
        
        # Create and attach policy
        policy_response = iam.create_policy(
            PolicyName='MultiAgentBedrockPolicy',
            PolicyDocument=json.dumps(bedrock_policy)
        )
        policy_arn = policy_response['Policy']['Arn']
        
        iam.attach_role_policy(
            RoleName='MultiAgentStepFunctionRole',
            PolicyArn=policy_arn
        )
        print("[OK] Policy attached")
        
        time.sleep(10)
        return role_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        role_response = iam.get_role(RoleName='MultiAgentStepFunctionRole')
        role_arn = role_response['Role']['Arn']
        print(f"[OK] Using existing role: {role_arn}")
        return role_arn
    except Exception as e:
        if 'EntityAlreadyExists' in str(e):
            role_response = iam.get_role(RoleName='MultiAgentStepFunctionRole')
            role_arn = role_response['Role']['Arn']
            print(f"[OK] Using existing role: {role_arn}")
            return role_arn
        raise

def deploy_step_function():
    """Deploy Step Functions state machine"""
    sfn = boto3.client('stepfunctions', region_name=REGION)
    
    print("Creating Step Function...")
    
    # Get role ARN
    role_arn = create_step_function_role()
    
    # Load state machine definition
    with open('step_function_definition.json', 'r') as f:
        definition = f.read()
    
    try:
        response = sfn.create_state_machine(
            name='MultiAgentMedicalAnalysis',
            definition=definition,
            roleArn=role_arn,
            type='STANDARD'
        )
        
        state_machine_arn = response['stateMachineArn']
        print(f"[OK] Step Function created: {state_machine_arn}")
        
        # Save to config
        with open('agent_config.json', 'r') as f:
            config = json.load(f)
        
        config['step_function'] = {
            'arn': state_machine_arn,
            'name': 'MultiAgentMedicalAnalysis'
        }
        
        with open('agent_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("[OK] Config updated")
        
        print("\n" + "="*50)
        print("STEP FUNCTION DEPLOYED SUCCESSFULLY!")
        print("="*50)
        print(f"ARN: {state_machine_arn}")
        
        return state_machine_arn
        
    except sfn.exceptions.StateMachineAlreadyExists:
        print("[WARN] Step Function already exists")
        # List and get existing
        machines = sfn.list_state_machines()
        for machine in machines['stateMachines']:
            if machine['name'] == 'MultiAgentMedicalAnalysis':
                print(f"[OK] Using existing: {machine['stateMachineArn']}")
                return machine['stateMachineArn']
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

if __name__ == "__main__":
    deploy_step_function()
