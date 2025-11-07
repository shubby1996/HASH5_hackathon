# Bedrock Agent - Current Capabilities vs HealthLake Resources

## Current Agent Access (3 out of 10 resources)

### ✅ **Currently Accessible:**

| Resource | Agent Can Access | Details |
|----------|-----------------|---------|
| **Patient** | ✅ YES | Full access - name, gender, birthDate, ID |
| **Condition** | ✅ YES | Full access - diagnoses, clinical status, patient reference |
| **Observation** | ✅ YES | Full access - vital signs, lab results, values with units |

---

### ❌ **NOT Currently Accessible (7 resources):**

| Resource | Agent Can Access | What's Missing |
|----------|-----------------|----------------|
| **MedicationRequest** | ❌ NO | Prescriptions, medication names, dosages |
| **Encounter** | ❌ NO | Healthcare visits, visit types, dates, providers |
| **Procedure** | ❌ NO | Medical procedures performed, dates, reasons |
| **AllergyIntolerance** | ❌ NO | Patient allergies, criticality levels |
| **Immunization** | ❌ NO | Vaccination history, vaccine types, dates |
| **DiagnosticReport** | ❌ NO | Lab reports, test results, report summaries |
| **CarePlan** | ❌ NO | Treatment plans, care activities, goals |

---

## Current Agent Capabilities

### 1. **Search Patients** (`/search-patients`)
**What it does:**
- Lists patients with basic demographics
- Returns: ID, name, gender, birth date
- Supports count parameter (default: 10)

**Example queries:**
- "Show me a list of patients"
- "Find 20 patients"
- "Who are the patients in the system?"

---

### 2. **Search Conditions** (`/search-conditions`)
**What it does:**
- Lists medical conditions/diagnoses
- Can filter by patient ID
- Returns: Condition name, patient reference

**Example queries:**
- "What medical conditions are in the system?"
- "Show me conditions for patient X"
- "Find patients with COVID-19"

---

### 3. **Search Observations** (`/search-observations`)
**What it does:**
- Lists vital signs and lab results
- Can filter by patient ID
- Returns: Observation type, value with units

**Example queries:**
- "What vital signs are available?"
- "Show me lab results"
- "What are the observations for patient X?"

---

## What the Agent CANNOT Do (Yet)

### ❌ **Medication Queries**
- "What medications is patient X taking?"
- "Show me all prescriptions"
- "Find patients on aspirin"

### ❌ **Visit/Encounter Queries**
- "When did patient X last visit?"
- "Show me emergency room visits"
- "List all encounters for patient X"

### ❌ **Procedure Queries**
- "What procedures were performed?"
- "Show me surgeries for patient X"
- "List oxygen administration procedures"

### ❌ **Allergy Queries**
- "What allergies does patient X have?"
- "Show me all food allergies"
- "Find patients allergic to bee venom"

### ❌ **Immunization Queries**
- "What vaccines has patient X received?"
- "Show me flu vaccination records"
- "List all immunizations"

### ❌ **Diagnostic Report Queries**
- "Show me COVID test results"
- "What lab reports are available?"
- "Get diagnostic reports for patient X"

### ❌ **Care Plan Queries**
- "What is the treatment plan for patient X?"
- "Show me active care plans"
- "List care activities"

---

## Coverage Summary

```
Total HealthLake Resources: 10
Agent Can Access:           3 (30%)
Agent Cannot Access:        7 (70%)
```

### Accessible Resources (30%):
- ✅ Patient
- ✅ Condition  
- ✅ Observation

### Missing Resources (70%):
- ❌ MedicationRequest
- ❌ Encounter
- ❌ Procedure
- ❌ AllergyIntolerance
- ❌ Immunization
- ❌ DiagnosticReport
- ❌ CarePlan

---

## Recommendation: Expand Agent Capabilities

To make the agent a comprehensive healthcare assistant, you should add action groups for the remaining 7 resources.

### Priority Order (Suggested):

**High Priority:**
1. **MedicationRequest** - Critical for medication management
2. **Encounter** - Essential for visit history
3. **AllergyIntolerance** - Important for patient safety

**Medium Priority:**
4. **Procedure** - Useful for treatment history
5. **Immunization** - Important for preventive care
6. **DiagnosticReport** - Valuable for test results

**Lower Priority:**
7. **CarePlan** - Useful but less frequently queried

---

## Next Steps to Expand

1. Update `agent_schema.json` with new endpoints
2. Update `lambda_function.py` with new handlers
3. Redeploy Lambda function
4. Prepare agent again
5. Test new capabilities

Would you like me to expand the agent to access all 10 resource types?
