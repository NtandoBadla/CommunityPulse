from fastapi import FastAPI

from backend.database import Base, engine
from backend.models.clinic import Clinic
from backend.api.clinics import router as clinics_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CommunityPulse API",
    description="Community resilience intelligence platform",
    version="0.1.0"
)


app.include_router(clinics_router)


@app.get("/")
def root():
    return {
        "message": "CommunityPulse API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }