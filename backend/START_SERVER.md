# Start FastAPI Server

## Step 1: Open a terminal and run:
```bash
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

## Step 2: Wait for this message:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

## Step 3: In a NEW terminal, run the test:
```bash
cd backend
..\.venv\Scripts\python.exe test_reports.py
```

## Or test in browser:
- Swagger UI: http://127.0.0.1:8000/docs
- Patients: http://127.0.0.1:8000/api/patients
