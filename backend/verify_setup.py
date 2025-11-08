"""Verify backend setup and all components"""
import sys
import os

print("=" * 60)
print("BACKEND SETUP VERIFICATION")
print("=" * 60)

# 1. Check directory structure
print("\n1. Checking directory structure...")
required_dirs = [
    'app',
    'app/api',
    'app/api/routes',
    'app/core',
    'app/models',
    'app/services'
]

for dir_path in required_dirs:
    exists = os.path.exists(dir_path)
    status = "[OK]" if exists else "[MISSING]"
    print(f"   {status} {dir_path}")

# 2. Check required files
print("\n2. Checking required files...")
required_files = [
    'app/__init__.py',
    'app/main.py',
    'app/core/config.py',
    'app/models/patient.py',
    'app/models/report.py',
    'app/services/healthlake_service.py',
    'app/services/bedrock_service.py',
    'app/services/storage_service.py',
    'app/api/routes/health.py',
    'app/api/routes/patients.py',
    'app/api/routes/reports.py',
    'agent_config.json',
    'requirements.txt'
]

for file_path in required_files:
    exists = os.path.exists(file_path)
    status = "[OK]" if exists else "[MISSING]"
    print(f"   {status} {file_path}")

# 3. Check imports
print("\n3. Checking Python imports...")
try:
    from app.core.config import settings
    print("   [OK] app.core.config")
except Exception as e:
    print(f"   [ERROR] app.core.config: {e}")

try:
    from app.models.patient import Patient, PatientSummary
    print("   [OK] app.models.patient")
except Exception as e:
    print(f"   [ERROR] app.models.patient: {e}")

try:
    from app.models.report import Report, ReportStatus
    print("   [OK] app.models.report")
except Exception as e:
    print(f"   [ERROR] app.models.report: {e}")

try:
    from app.services.healthlake_service import healthlake_service
    print("   [OK] app.services.healthlake_service")
except Exception as e:
    print(f"   [ERROR] app.services.healthlake_service: {e}")

try:
    from app.services.bedrock_service import bedrock_service
    print("   [OK] app.services.bedrock_service")
except Exception as e:
    print(f"   [ERROR] app.services.bedrock_service: {e}")

try:
    from app.services.storage_service import storage_service
    print("   [OK] app.services.storage_service")
except Exception as e:
    print(f"   [ERROR] app.services.storage_service: {e}")

try:
    from app.api.routes import health, patients, reports
    print("   [OK] app.api.routes (all)")
except Exception as e:
    print(f"   [ERROR] app.api.routes: {e}")

# 4. Check configuration
print("\n4. Checking configuration...")
try:
    from app.core.config import settings
    print(f"   AWS Region: {settings.AWS_REGION}")
    print(f"   Has Access Key: {bool(settings.AWS_ACCESS_KEY_ID)}")
    print(f"   Has Secret Key: {bool(settings.AWS_SECRET_ACCESS_KEY)}")
    print(f"   Has Session Token: {bool(settings.AWS_SESSION_TOKEN)}")
    print(f"   Datastore ID: {settings.HEALTHLAKE_DATASTORE_ID[:20]}...")
except Exception as e:
    print(f"   [ERROR] Configuration error: {e}")

# 5. Check agent config
print("\n5. Checking agent configuration...")
try:
    import json
    with open('agent_config.json', 'r') as f:
        config = json.load(f)
    
    agents = ['cardiologist_agent', 'radiologist_agent', 'endocrinologist_agent', 'orchestrator_agent', 'qa_agent']
    for agent in agents:
        if agent in config:
            print(f"   [OK] {agent}: {config[agent]['agent_id']}")
        else:
            print(f"   [MISSING] {agent}: Missing")
except Exception as e:
    print(f"   [ERROR] Agent config error: {e}")

# 6. Test AWS credentials
print("\n6. Testing AWS credentials...")
try:
    import boto3
    from app.core.config import settings
    
    sts = boto3.client(
        'sts',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_REGION
    )
    
    identity = sts.get_caller_identity()
    print(f"   [OK] Credentials valid")
    print(f"   Account: {identity['Account']}")
except Exception as e:
    print(f"   [ERROR] Credentials invalid: {e}")

# 7. Test HealthLake connection
print("\n7. Testing HealthLake connection...")
try:
    from app.services.healthlake_service import healthlake_service
    patients = healthlake_service.get_all_patients()
    print(f"   [OK] HealthLake connected")
    print(f"   Found {len(patients)} patients")
except Exception as e:
    print(f"   [ERROR] HealthLake error: {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
