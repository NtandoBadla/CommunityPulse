from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.clinic import Clinic
from backend.schemas.clinic import ClinicCreate


router = APIRouter(
    prefix="/clinics",
    tags=["Clinics"]
)


@router.get("/")
def get_clinics(
    db: Session = Depends(get_db)
):
    clinics = db.query(Clinic).all()

    return clinics


@router.get("/{clinic_id}")
def get_clinic(
    clinic_id: int,
    db: Session = Depends(get_db)
):

    clinic = (
        db.query(Clinic)
        .filter(Clinic.id == clinic_id)
        .first()
    )

    if not clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    return clinic


@router.post("/")
def create_clinic(
    clinic_data: ClinicCreate,
    db: Session = Depends(get_db)
):

    clinic = Clinic(
        name=clinic_data.name,
        location=clinic_data.location,
        address=clinic_data.address,
        latitude=clinic_data.latitude,
        longitude=clinic_data.longitude,
        operating_hours=clinic_data.operating_hours,
        capacity=clinic_data.capacity
    )

    db.add(clinic)
    db.commit()
    db.refresh(clinic)

    return clinic