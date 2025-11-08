import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_report_generation():
    print("Testing Report Generation API\n")
    
    # 1. Get a patient
    print("1. Fetching patients...")
    response = requests.get(f"{BASE_URL}/patients")
    patients = response.json()
    
    if not patients:
        print("No patients found!")
        return
    
    patient = patients[0]
    print(f"   Selected: {patient['name']} (ID: {patient['id'][:8]}...)")
    
    # 2. Start report generation
    print("\n2. Starting report generation...")
    response = requests.post(
        f"{BASE_URL}/reports/generate",
        json={"patient_id": patient['id']}
    )
    
    if response.status_code != 200:
        print(f"   Error: {response.text}")
        return
    
    result = response.json()
    job_id = result['job_id']
    print(f"   Job ID: {job_id}")
    print(f"   Status: {result['status']}")
    
    # 3. Poll for completion
    print("\n3. Polling for completion...")
    max_attempts = 60  # 5 minutes max
    attempt = 0
    
    while attempt < max_attempts:
        time.sleep(5)  # Poll every 5 seconds
        attempt += 1
        
        response = requests.get(f"{BASE_URL}/reports/status/{job_id}")
        status = response.json()
        
        print(f"   [{attempt}] Status: {status['status']} - {status.get('progress', '')}")
        
        if status['status'] == 'completed':
            print("\n✓ Report generation completed!")
            break
        elif status['status'] == 'failed':
            print(f"\n✗ Report generation failed: {status.get('progress')}")
            return
    
    # 4. Get the report
    print("\n4. Fetching completed report...")
    response = requests.get(f"{BASE_URL}/reports/{job_id}")
    
    if response.status_code != 200:
        print(f"   Error: {response.text}")
        return
    
    report = response.json()
    
    print(f"\n=== REPORT SUMMARY ===")
    print(f"Patient: {report['patient_name']}")
    print(f"Created: {report['created_at']}")
    print(f"\nCardiology Report Length: {len(report['cardiology'])} chars")
    print(f"Radiology Report Length: {len(report['radiology'])} chars")
    print(f"Endocrinology Report Length: {len(report['endocrinology'])} chars")
    print(f"Comprehensive Report Length: {len(report['comprehensive'])} chars")
    
    print(f"\n=== CARDIOLOGY PREVIEW ===")
    print(report['cardiology'][:200] + "...")
    
    print("\n✓ All tests passed!")

if __name__ == '__main__':
    test_report_generation()
