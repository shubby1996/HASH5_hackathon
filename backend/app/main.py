from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, patients, reports, qa, medical_data
from dotenv import load_dotenv
from pathlib import Path

# Load .env from root directory (go up from app/main.py -> app -> backend -> root)
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

app = FastAPI(
    title="HealthLake AI API",
    description="Backend API for HealthLake AI Assistant",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for AWS deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(patients.router, prefix="/api", tags=["patients"])
app.include_router(reports.router, prefix="/api", tags=["reports"])
app.include_router(qa.router, prefix="/api", tags=["qa"])
app.include_router(medical_data.router, prefix="/api", tags=["medical_data"])

@app.get("/")
async def root():
    return {
        "message": "HealthLake AI API",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/test")
async def test():
    return {"message": "Server is running NEW code!", "timestamp": "2025-01-08"}

@app.get("/debug/config")
async def debug_config():
    from app.core.config import settings
    return {
        "region": settings.AWS_REGION,
        "has_access_key": bool(settings.AWS_ACCESS_KEY_ID),
        "has_secret_key": bool(settings.AWS_SECRET_ACCESS_KEY),
        "has_session_token": bool(settings.AWS_SESSION_TOKEN),
        "datastore_id": settings.HEALTHLAKE_DATASTORE_ID[:20] + "..."
    }
