# HealthLake FHIR Schema Summary

## Overview
Your HealthLake datastore contains **10 FHIR resource types** with synthetic patient data (SYNTHEA).

---

## Resource Types & Key Fields

### 1. **Patient** (Demographics)
- **Fields**: 16
- **Key Data**:
  - `id`, `name`, `gender`, `birthDate`, `address`
  - `identifier`: SSN, Driver's License, Passport, Medical Record Number
  - `telecom`: Phone numbers
  - `maritalStatus`, `communication` (language)
  - `multipleBirth` (boolean/integer)
  - `deceasedDateTime` (if applicable)

**Example**: Dexter530 Little434, Male, DOB: 1997-11-22, SSN: 999-83-3466

---

### 2. **Observation** (Vital Signs & Lab Results)
- **Fields**: 13
- **Key Data**:
  - `code`: LOINC codes (e.g., "72166-2" for Tobacco smoking status)
  - `status`: final, preliminary
  - `category`: vital-signs, laboratory, survey
  - `valueQuantity`: Numeric values with units
  - `valueCodeableConcept`: Coded values
  - `component`: Multi-part observations (e.g., Blood Pressure)
  - `effectiveDateTime`, `issued`

**Examples**: Blood pressure, Body weight, Hemoglobin, Smoking status

---

### 3. **Condition** (Diagnoses)
- **Fields**: 11
- **Key Data**:
  - `code`: SNOMED CT codes (e.g., "72892002" for Normal pregnancy)
  - `clinicalStatus`: active, resolved, inactive
  - `verificationStatus`: confirmed, provisional
  - `onsetDateTime`, `abatementDateTime`
  - `encounter`: Reference to visit

**Examples**: COVID-19, Acute bronchitis, Normal pregnancy, Joint pain

---

### 4. **MedicationRequest** (Prescriptions)
- **Fields**: 11
- **Key Data**:
  - `medicationCodeableConcept`: RxNorm codes
  - `status`: active, stopped, completed
  - `intent`: order, plan
  - `authoredOn`: Prescription date
  - `requester`: Prescribing provider
  - `reasonReference`: Link to condition

**Example**: NuvaRing 0.12/0.015 MG per 24HR 21 Day Vaginal Ring

---

### 5. **Encounter** (Healthcare Visits)
- **Fields**: 11
- **Key Data**:
  - `class`: AMB (ambulatory), EMER (emergency), IMP (inpatient)
  - `type`: SNOMED CT codes (e.g., "698314001" for Consultation)
  - `status`: finished, in-progress
  - `period`: Start and end times
  - `participant`: Healthcare providers
  - `serviceProvider`: Hospital/clinic
  - `reasonCode`: Visit reason

---

### 6. **Procedure** (Medical Procedures)
- **Fields**: 9
- **Key Data**:
  - `code`: SNOMED CT codes (e.g., "371908008" for Oxygen administration)
  - `status`: completed, in-progress
  - `performedPeriod`: When performed
  - `reasonReference`: Why performed (link to condition)
  - `encounter`: Associated visit

**Example**: Oxygen administration by mask (procedure)

---

### 7. **AllergyIntolerance** (Allergies)
- **Fields**: 11
- **Key Data**:
  - `code`: SNOMED CT codes (e.g., "424213003" for Bee venom allergy)
  - `clinicalStatus`: active, inactive, resolved
  - `verificationStatus`: confirmed, unconfirmed
  - `type`: allergy, intolerance
  - `category`: food, medication, environment
  - `criticality`: low, high, unable-to-assess
  - `recordedDate`

**Example**: Allergy to bee venom (low criticality)

---

### 8. **Immunization** (Vaccinations)
- **Fields**: 9
- **Key Data**:
  - `vaccineCode`: CVX codes (e.g., "140" for Influenza vaccine)
  - `status`: completed, not-done
  - `occurrenceDateTime`: When administered
  - `primarySource`: true/false (directly reported)
  - `encounter`: Associated visit

**Example**: Influenza, seasonal, injectable, preservative free

---

### 9. **DiagnosticReport** (Lab Reports)
- **Fields**: 11
- **Key Data**:
  - `code`: LOINC codes (e.g., "94531-1" for SARS-CoV-2 RNA test)
  - `status`: final, preliminary
  - `category`: LAB, RAD (radiology)
  - `result`: References to Observation resources
  - `effectiveDateTime`, `issued`

**Example**: SARS-CoV-2 RNA Panel Respiratory NAA+probe

---

### 10. **CarePlan** (Treatment Plans)
- **Fields**: 13
- **Key Data**:
  - `status`: active, completed
  - `intent`: plan, order
  - `category`: SNOMED CT codes (e.g., "736376001" for Infectious disease care plan)
  - `period`: Start and end dates
  - `activity`: List of planned activities
  - `addresses`: Conditions being treated
  - `careTeam`: Healthcare team members

**Example**: COVID-19 care plan with airborne precautions and isolation

---

## Standard Coding Systems Used

| System | Purpose | Example |
|--------|---------|---------|
| **LOINC** | Lab tests & observations | 72166-2 (Tobacco smoking status) |
| **SNOMED CT** | Clinical terms | 72892002 (Normal pregnancy) |
| **RxNorm** | Medications | 1367439 (NuvaRing) |
| **CVX** | Vaccines | 140 (Influenza vaccine) |
| **ICD-10** | Diagnoses | (if present) |

---

## Common Relationships

```
Patient
  ├── Encounter (visits)
  │     ├── Observation (vitals/labs during visit)
  │     ├── Condition (diagnoses made)
  │     ├── Procedure (procedures performed)
  │     ├── MedicationRequest (prescriptions written)
  │     └── DiagnosticReport (lab reports)
  ├── AllergyIntolerance (patient allergies)
  ├── Immunization (vaccination history)
  └── CarePlan (treatment plans)
```

---

## Query Capabilities

Your Bedrock Agent can now query:
1. **Patient demographics** - Name, age, gender, location
2. **Medical conditions** - Active/resolved diagnoses
3. **Vital signs** - Blood pressure, weight, temperature
4. **Lab results** - CBC, metabolic panels, COVID tests
5. **Medications** - Current and past prescriptions
6. **Procedures** - Medical procedures performed
7. **Allergies** - Known allergies and intolerances
8. **Immunizations** - Vaccination history
9. **Encounters** - Healthcare visits
10. **Care plans** - Treatment plans

---

## Files Generated
- `healthlake_schema.json` - Full schema with samples
- `schema_report.txt` - Detailed text report
- `HEALTHLAKE_SCHEMA_SUMMARY.md` - This summary

---

## Next Steps
1. ✅ Schema analyzed
2. ✅ Bedrock Agent connected
3. ✅ Streamlit UI created (`app.py`)
4. 🔄 Run the UI: `run_app.bat` or `streamlit run app.py`
5. 🔄 Expand agent capabilities (add more action groups)
6. 🔄 Import additional data when ready
