import boto3
import json
from dotenv import load_dotenv
from explore_healthlake import HealthLakeExplorer

load_dotenv()

def visualize_data():
    explorer = HealthLakeExplorer('b1f04342d94dcc96c47f9528f039f5a8')
    
    print("=" * 60)
    print("HEALTHLAKE DATA VISUALIZATION")
    print("=" * 60)
    
    # Get patients
    patients = explorer.search_resources('Patient', count=5)
    print(f"\nTotal Patients: {patients.get('total', 0)}")
    
    if 'entry' in patients and len(patients['entry']) > 0:
        patient_id = patients['entry'][0]['resource']['id']
        
        # Get observations for first patient
        observations = explorer.search_resources('Observation', count=100)
        print(f"Total Observations: {observations.get('total', 0)}")
        
        # Get conditions
        conditions = explorer.search_resources('Condition', count=100)
        print(f"Total Conditions: {conditions.get('total', 0)}")
        
        # Get medications
        meds = explorer.search_resources('MedicationRequest', count=100)
        print(f"Total Medication Requests: {meds.get('total', 0)}")
        
        # Get encounters
        encounters = explorer.search_resources('Encounter', count=100)
        print(f"Total Encounters: {encounters.get('total', 0)}")
        
        # Get procedures
        procedures = explorer.search_resources('Procedure', count=100)
        print(f"Total Procedures: {procedures.get('total', 0)}")
        
        print("\n" + "=" * 60)
        print("SAMPLE PATIENT DETAILS")
        print("=" * 60 + "\n")
        
        for i, entry in enumerate(patients['entry'][:3], 1):
            patient = entry['resource']
            name = patient.get('name', [{}])[0]
            full_name = f"{name.get('given', [''])[0]} {name.get('family', '')}"
            
            print(f"\n{i}. {full_name}")
            print(f"   ID: {patient.get('id')}")
            print(f"   Gender: {patient.get('gender', 'Unknown')}")
            print(f"   Birth Date: {patient.get('birthDate', 'Unknown')}")
            
            if 'address' in patient and len(patient['address']) > 0:
                addr = patient['address'][0]
                city = addr.get('city', '')
                state = addr.get('state', '')
                print(f"   Location: {city}, {state}")
        
        # Sample conditions
        if 'entry' in conditions and len(conditions['entry']) > 0:
            print("\n" + "=" * 60)
            print("SAMPLE CONDITIONS")
            print("=" * 60)
            for i, entry in enumerate(conditions['entry'][:5], 1):
                condition = entry['resource']
                code = condition.get('code', {}).get('coding', [{}])[0]
                display = code.get('display', 'Unknown')
                print(f"{i}. {display}")
        
        # Sample observations
        if 'entry' in observations and len(observations['entry']) > 0:
            print("\n" + "=" * 60)
            print("SAMPLE OBSERVATIONS (Vital Signs/Labs)")
            print("=" * 60)
            for i, entry in enumerate(observations['entry'][:5], 1):
                obs = entry['resource']
                code = obs.get('code', {}).get('coding', [{}])[0]
                display = code.get('display', 'Unknown')
                value = obs.get('valueQuantity', {})
                val_str = f"{value.get('value', '')} {value.get('unit', '')}" if value else "N/A"
                print(f"{i}. {display}: {val_str}")

if __name__ == "__main__":
    visualize_data()
