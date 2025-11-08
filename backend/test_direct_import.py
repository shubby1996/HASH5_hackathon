import sys
sys.path.insert(0, '.')

print("Testing direct imports...")

# Test config loading
from app.core.config import settings
print(f"\nConfig loaded:")
print(f"  Region: {settings.AWS_REGION}")
print(f"  Has access key: {bool(settings.AWS_ACCESS_KEY_ID)}")
print(f"  Access key starts with: {settings.AWS_ACCESS_KEY_ID[:10] if settings.AWS_ACCESS_KEY_ID else 'None'}")

# Test HealthLake service
from app.services.healthlake_service import healthlake_service
print(f"\nTesting HealthLake service...")
try:
    patients = healthlake_service.get_all_patients()
    print(f"  Found {len(patients)} patients")
    if patients:
        print(f"  First: {patients[0]['name']}")
except Exception as e:
    print(f"  Error: {e}")
