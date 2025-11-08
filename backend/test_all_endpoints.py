"""Test all API endpoints"""
import requests
import time

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("TESTING ALL API ENDPOINTS")
print("=" * 60)

# 1. Test root endpoint
print("\n1. Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 2. Test health check
print("\n2. Testing health check...")
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   [ERROR] {e}")

# 3. Test get patients
PATIENT_ID = None
PATIENT_NAME = None
JOB_ID = None

print("\n3. Testing GET /api/patients...")
try:
    response = requests.get(f"{BASE_URL}/api/patients")
    print(f"   Status: {response.status_code}")
    patients = response.json()
    print(f"   Found {len(patients)} patients")
    if patients:
        print(f"   First patient: {patients[0]['name']} (ID: {patients[0]['id'][:8]}...)")
        PATIENT_ID = patients[0]['id']
        PATIENT_NAME = patients[0]['name']
    else:
        print("   [WARNING] No patients found. Check HealthLake connection.")
except Exception as e:
    print(f"   [ERROR] {e}")

# 4. Test get patient by ID
if PATIENT_ID:
    print(f"\n4. Testing GET /api/patients/{PATIENT_ID[:8]}...")
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{PATIENT_ID}")
        print(f"   Status: {response.status_code}")
        patient = response.json()
        print(f"   Patient: {patient['name']}")
        print(f"   Gender: {patient['gender']}")
        print(f"   Birth Date: {patient['birthDate']}")
    except Exception as e:
        print(f"   [ERROR] {e}")

# 5. Test get patient summary
if PATIENT_ID:
    print(f"\n5. Testing GET /api/patients/{PATIENT_ID[:8]}/summary...")
    try:
        response = requests.get(f"{BASE_URL}/api/patients/{PATIENT_ID}/summary")
        print(f"   Status: {response.status_code}")
        summary = response.json()
        print(f"   Patient: {summary['name']}")
        print(f"   Conditions: {len(summary['conditions'])}")
        print(f"   Medications: {len(summary['medications'])}")
        print(f"   Allergies: {len(summary['allergies'])}")
        print(f"   Has ECG: {summary['has_ecg']}")
        print(f"   MRI Reports: {summary['mri_reports_count']}")
    except Exception as e:
        print(f"   [ERROR] {e}")

# 6. Test report generation
if PATIENT_ID:
    print(f"\n6. Testing POST /api/reports/generate...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/reports/generate",
            json={"patient_id": PATIENT_ID}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Job ID: {result['job_id']}")
        print(f"   Status: {result['status']}")
        print(f"   Progress: {result.get('progress', 'N/A')}")
        JOB_ID = result['job_id']
    except Exception as e:
        print(f"   [ERROR] {e}")

# 7. Test report status polling
if JOB_ID:
    print(f"\n7. Testing GET /api/reports/status/{JOB_ID[:8]}...")
    print("   Polling for completion (max 60 seconds)...")
    
    for i in range(12):  # Poll for 60 seconds
        try:
            time.sleep(5)
            response = requests.get(f"{BASE_URL}/api/reports/status/{JOB_ID}")
            status = response.json()
            print(f"   [{i+1}] Status: {status['status']} - {status.get('progress', '')}")
            
            if status['status'] == 'completed':
                print("   [OK] Report generation completed!")
                break
            elif status['status'] == 'failed':
                print(f"   [ERROR] Report generation failed: {status.get('progress')}")
                JOB_ID = None
                break
        except Exception as e:
            print(f"   [ERROR] {e}")
            break

# 8. Test get report
if JOB_ID:
    print(f"\n8. Testing GET /api/reports/{JOB_ID[:8]}...")
    try:
        response = requests.get(f"{BASE_URL}/api/reports/{JOB_ID}")
        print(f"   Status: {response.status_code}")
        report = response.json()
        print(f"   Patient: {report['patient_name']}")
        print(f"   Created: {report['created_at']}")
        print(f"   Cardiology report: {len(report['cardiology'])} chars")
        print(f"   Radiology report: {len(report['radiology'])} chars")
        print(f"   Endocrinology report: {len(report['endocrinology'])} chars")
        print(f"   Comprehensive report: {len(report['comprehensive'])} chars")
        
        print(f"\n   === CARDIOLOGY PREVIEW ===")
        print(f"   {report['cardiology'][:150]}...")
    except Exception as e:
        print(f"   [ERROR] {e}")

# 9. Test get patient reports
if PATIENT_ID:
    print(f"\n9. Testing GET /api/reports/patient/{PATIENT_ID[:8]}...")
    try:
        response = requests.get(f"{BASE_URL}/api/reports/patient/{PATIENT_ID}")
        print(f"   Status: {response.status_code}")
        reports = response.json()
        print(f"   Found {len(reports)} reports for this patient")
    except Exception as e:
        print(f"   [ERROR] {e}")

print("\n" + "=" * 60)
print("ALL ENDPOINT TESTS COMPLETE")
print("=" * 60)
