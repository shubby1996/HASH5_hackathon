import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("TESTING Q&A ENDPOINTS")
print("=" * 60)

# First, get a patient and generate a report
print("\n1. Getting patient...")
patients = requests.get(f"{BASE_URL}/patients").json()
patient_id = patients[0]['id']
patient_name = patients[0]['name']
print(f"   Patient: {patient_name}")

print("\n2. Getting patient summary...")
summary = requests.get(f"{BASE_URL}/patients/{patient_id}/summary").json()
print(f"   Conditions: {len(summary['conditions'])}")
print(f"   Medications: {len(summary['medications'])}")

# Create mock cached reports for testing
cached_reports = {
    "patient_id": patient_id,
    "patient_summary": summary,
    "cardiology": "Patient has atrial fibrillation with moderate risk. ECG shows irregular rhythm.",
    "radiology": "Cardiac MRI shows enlarged left atrium (4.5cm). Consistent with AFib.",
    "endocrinology": "LDL cholesterol 145 mg/dL (borderline high). Recommend statin therapy.",
    "comprehensive": "Patient requires anticoagulation for AFib, cardiology follow-up, and cholesterol management."
}

# Test Q&A
print("\n3. Testing Q&A - Ask about health risks...")
qa_request = {
    "question": "What are my top health risks?",
    "cached_reports": cached_reports
}

response = requests.post(f"{BASE_URL}/qa/ask", json=qa_request)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    qa_response = response.json()
    print(f"   Question: {qa_response['question']}")
    print(f"   Answer: {qa_response['answer'][:150]}...")
    print(f"   UI Type: {qa_response['ui_type']}")
    print(f"   Sources: {qa_response['sources']}")
    print(f"   Confidence: {qa_response['confidence']}")
else:
    print(f"   Error: {response.text}")

# Test another question
print("\n4. Testing Q&A - Ask about medications...")
qa_request2 = {
    "question": "What medications do I need?",
    "cached_reports": cached_reports
}

response2 = requests.post(f"{BASE_URL}/qa/ask", json=qa_request2)
print(f"   Status: {response2.status_code}")

if response2.status_code == 200:
    qa_response2 = response2.json()
    print(f"   Answer: {qa_response2['answer'][:150]}...")
    print(f"   UI Type: {qa_response2['ui_type']}")

# Test history
print("\n5. Testing Q&A history...")
history_response = requests.get(f"{BASE_URL}/qa/history/{patient_id}")
print(f"   Status: {history_response.status_code}")

if history_response.status_code == 200:
    history = history_response.json()
    print(f"   History items: {len(history)}")
    for i, item in enumerate(history, 1):
        print(f"   {i}. {item['question']}")

print("\n" + "=" * 60)
print("Q&A ENDPOINT TESTS COMPLETE")
print("=" * 60)
