import requests

print("Testing /test endpoint...")
r = requests.get('http://127.0.0.1:8000/test')
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

print("\nTesting /api/patients endpoint...")
r2 = requests.get('http://127.0.0.1:8000/api/patients')
print(f"Status: {r2.status_code}")
patients = r2.json()
print(f"Patients count: {len(patients)}")
if patients:
    print(f"First patient: {patients[0]}")
