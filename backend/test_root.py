import requests
r = requests.get('http://127.0.0.1:8000/')
print(f"Status: {r.status_code}")
print(f"Response: {r.json()}")

r2 = requests.get('http://127.0.0.1:8000/debug/config')
print(f"\nDebug Status: {r2.status_code}")
print(f"Debug Response: {r2.json()}")
