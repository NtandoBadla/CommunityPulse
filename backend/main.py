from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.models.clinic import Clinic
from backend.models.clinic_metric import ClinicMetric
from backend.models.user import User

from backend.api.clinics import router as clinics_router
from backend.api.clinic_metrics import router as clinic_metrics_router
from backend.api.auth import router as auth_router
from backend.api.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CommunityPulse API",
    description="Community resilience intelligence platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clinics_router)
app.include_router(clinic_metrics_router)
app.include_router(auth_router)
app.include_router(users_router)


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