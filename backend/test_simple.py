import requests

print("Testing patients endpoint...")
response = requests.get("http://127.0.0.1:8000/api/patients")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    data = response.json()
    print(f"\nType: {type(data)}")
    print(f"Length: {len(data)}")
    if data:
        print(f"First item: {data[0]}")
