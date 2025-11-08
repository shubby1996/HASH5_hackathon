import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_medical_data_endpoints():
    print("Testing Medical Data Endpoints\n" + "="*50)
    
    # Get a patient first
    print("\n1. Getting patient list...")
    response = requests.get(f"{BASE_URL}/patients")
    if response.status_code == 200:
        patients = response.json()
        if patients:
            patient_id = patients[0]['id']
            print(f"✓ Found patient: {patient_id}")
            
            # Test ECG endpoint
            print(f"\n2. Testing ECG endpoint for patient {patient_id}...")
            ecg_response = requests.get(f"{BASE_URL}/ecg/{patient_id}")
            print(f"Status: {ecg_response.status_code}")
            if ecg_response.status_code == 200:
                ecg_data = ecg_response.json()
                print(f"✓ ECG data retrieved")
                print(f"  - Data points: {len(ecg_data.get('data', []))}")
                if ecg_data.get('data'):
                    print(f"  - Sample: {ecg_data['data'][0]}")
            else:
                print(f"✗ ECG request failed: {ecg_response.text}")
            
            # Test MRI endpoint
            print(f"\n3. Testing MRI endpoint for patient {patient_id}...")
            mri_response = requests.get(f"{BASE_URL}/mri/{patient_id}")
            print(f"Status: {mri_response.status_code}")
            if mri_response.status_code == 200:
                mri_data = mri_response.json()
                print(f"✓ MRI data retrieved")
                print(f"  - Reports: {len(mri_data.get('reports', []))}")
                if mri_data.get('reports'):
                    print(f"  - Sample: {mri_data['reports'][0].get('type', 'N/A')}")
            else:
                print(f"✗ MRI request failed: {mri_response.text}")
        else:
            print("✗ No patients found")
    else:
        print(f"✗ Failed to get patients: {response.status_code}")

if __name__ == "__main__":
    try:
        test_medical_data_endpoints()
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend server. Make sure it's running on port 8000")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
