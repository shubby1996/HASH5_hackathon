import requests

# Check the job from the test
job_id = "51296ada-e6d6-4e51-923f-d079078a6fc4"

print(f"Checking status of job: {job_id}")
response = requests.get(f"http://127.0.0.1:8000/api/reports/status/{job_id}")
print(f"Status: {response.json()}")

if response.json()['status'] == 'completed':
    print("\nFetching report...")
    report = requests.get(f"http://127.0.0.1:8000/api/reports/{job_id}")
    if report.status_code == 200:
        r = report.json()
        print(f"Patient: {r['patient_name']}")
        print(f"Cardiology: {len(r['cardiology'])} chars")
        print(f"Radiology: {len(r['radiology'])} chars")
        print(f"Endocrinology: {len(r['endocrinology'])} chars")
        print(f"Comprehensive: {len(r['comprehensive'])} chars")
    else:
        print(f"Error: {report.text}")
