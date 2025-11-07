import json

# Load schema
with open('healthlake_schema.json', 'r') as f:
    schema = json.load(f)

print("=" * 100)
print("HEALTHLAKE FHIR DATA SCHEMA - DETAILED REPORT")
print("=" * 100)

# Overview
print("\nRESOURCE OVERVIEW")
print("-" * 100)
print(f"{'Resource Type':<25} {'Total Records':<15} {'Fields':<10} {'Key Attributes'}")
print("-" * 100)

for resource_type, data in schema.items():
    total = data.get('total', 0)
    fields = len(data.get('fields', {}))
    key_fields = ', '.join(list(data.get('fields', {}).keys())[:5])
    print(f"{resource_type:<25} {total:<15} {fields:<10} {key_fields}...")

# Detailed breakdown
print("\n\nDETAILED RESOURCE SCHEMAS")
print("=" * 100)

for resource_type, data in schema.items():
    print(f"\n{'='*100}")
    print(f"{resource_type.upper()}")
    print(f"{'='*100}")
    print(f"Total Records: {data.get('total', 0)}")
    print(f"\nFields ({len(data.get('fields', {}))}):")
    
    fields = data.get('fields', {})
    for field, types in sorted(fields.items()):
        print(f"  • {field:<30} {', '.join(types)}")
    
    # Show sample if available
    if data.get('sample'):
        sample = data['sample']
        print(f"\nSample Data Structure:")
        
        # Key fields to highlight
        if resource_type == 'Patient':
            print(f"  ID: {sample.get('id')}")
            if 'name' in sample:
                name = sample['name'][0] if sample['name'] else {}
                print(f"  Name: {name.get('given', [''])[0]} {name.get('family', '')}")
            print(f"  Gender: {sample.get('gender')}")
            print(f"  Birth Date: {sample.get('birthDate')}")
        
        elif resource_type == 'Observation':
            print(f"  ID: {sample.get('id')}")
            code = sample.get('code', {}).get('coding', [{}])[0]
            print(f"  Type: {code.get('display', 'N/A')}")
            print(f"  Status: {sample.get('status')}")
            if 'valueQuantity' in sample:
                val = sample['valueQuantity']
                print(f"  Value: {val.get('value')} {val.get('unit')}")
        
        elif resource_type == 'Condition':
            print(f"  ID: {sample.get('id')}")
            code = sample.get('code', {}).get('coding', [{}])[0]
            print(f"  Condition: {code.get('display', 'N/A')}")
            print(f"  Onset: {sample.get('onsetDateTime')}")
            print(f"  Status: {sample.get('clinicalStatus', {}).get('coding', [{}])[0].get('code')}")
        
        elif resource_type == 'MedicationRequest':
            print(f"  ID: {sample.get('id')}")
            med = sample.get('medicationCodeableConcept', {}).get('coding', [{}])[0]
            print(f"  Medication: {med.get('display', 'N/A')}")
            print(f"  Status: {sample.get('status')}")
            print(f"  Authored: {sample.get('authoredOn')}")

print("\n\n" + "=" * 100)
print("KEY INSIGHTS")
print("=" * 100)

print("""
1. PATIENT DATA:
   - Demographics: name, gender, birthDate, address
   - Identifiers: SSN, driver's license, passport
   - Communication preferences and marital status

2. CLINICAL OBSERVATIONS:
   - Vital signs: blood pressure, heart rate, temperature
   - Lab results: CBC, metabolic panels, specific tests
   - Survey responses and assessments

3. CONDITIONS:
   - Clinical status (active, resolved)
   - Onset and abatement dates
   - Verification status

4. MEDICATIONS:
   - Prescription details with RxNorm codes
   - Status tracking (active, stopped)
   - Reason references to conditions

5. ENCOUNTERS:
   - Visit types (ambulatory, emergency, inpatient)
   - Period and duration
   - Associated providers

6. PROCEDURES:
   - SNOMED CT coded procedures
   - Performance period
   - Linked to encounters and conditions

7. ALLERGIES:
   - Allergen identification
   - Criticality levels
   - Clinical and verification status

8. IMMUNIZATIONS:
   - CVX vaccine codes
   - Administration dates
   - Primary source tracking

9. DIAGNOSTIC REPORTS:
   - Lab reports with LOINC codes
   - Results references
   - Effective dates

10. CARE PLANS:
    - Treatment activities
    - Goals and addresses
    - Care team references
""")

print("\n" + "=" * 100)
print("Full schema details saved in: healthlake_schema.json")
print("=" * 100)
