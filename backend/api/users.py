from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.clinic_metric import ClinicMetric
from backend.models.user import User
from backend.auth import get_current_user

from backend.services.prediction_service import (
    calculate_crowding,
    get_crowding_level,
    calculate_estimated_wait,
    calculate_trend
)
from backend.services.recommendation_service import get_recommendations_for_clinic


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/me/status")
def get_my_clinic_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    clinic = current_user.home_clinic

    latest_metric = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic.id)
        .order_by(ClinicMetric.recorded_at.desc())
        .first()
    )

    if not latest_metric:
        raise HTTPException(
            status_code=404,
            detail="No metrics available for your clinic yet"
        )

    previous_metric = (
        db.query(ClinicMetric)
        .filter(
            ClinicMetric.clinic_id == clinic.id,
            ClinicMetric.id != latest_metric.id
        )
        .order_by(ClinicMetric.recorded_at.desc())
        .first()
    )

    crowding = calculate_crowding(
        latest_metric.patients_waiting,
        clinic.capacity
    )
    level = get_crowding_level(crowding)

    estimated_wait = calculate_estimated_wait(
        latest_metric.patients_waiting,
        latest_metric.patients_served,
        latest_metric.average_wait_minutes
    )

    trend = "STABLE"
    if previous_metric:
        trend = calculate_trend(
            latest_metric.patients_waiting,
            previous_metric.patients_waiting
        )

    response = {
        "user_name": current_user.name,
        "home_clinic_id": clinic.id,
        "home_clinic_name": clinic.name,
        "crowding_percentage": crowding,
        "crowding_level": level,
        "estimated_wait_minutes": estimated_wait,
        "trend": trend,
        "is_full": level in ("HIGH", "CRITICAL"),
        "recommendations": []
    }

    if level in ("HIGH", "CRITICAL"):
        try:
            rec_data = get_recommendations_for_clinic(db, clinic.id)
            response["recommendations"] = rec_data["recommendations"]
        except ValueError:
            pass

    return response