from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.clinic import Clinic
from backend.models.clinic_metric import ClinicMetric
from backend.schemas.clinic_metric import ClinicMetricCreate
from backend.services.historical_service import get_hourly_crowding_averages
from backend.services.advice_service import generate_advice
from backend.services.distance_service import calculate_distance_km

from backend.services.prediction_service import (
    calculate_crowding,
    get_crowding_level,
    calculate_estimated_wait,
    calculate_trend,
    generate_forecast
)


router = APIRouter(
    prefix="/clinics",
    tags=["Clinic Metrics"]
)


@router.post("/{clinic_id}/metrics")
def create_metric(
    clinic_id: int,
    metric_data: ClinicMetricCreate,
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

    metric = ClinicMetric(
        clinic_id=clinic_id,
        patients_waiting=metric_data.patients_waiting,
        patients_arrived=metric_data.patients_arrived,
        patients_served=metric_data.patients_served,
        active_staff=metric_data.active_staff,
        average_wait_minutes=metric_data.average_wait_minutes
    )

    db.add(metric)
    db.commit()
    db.refresh(metric)

    return metric


@router.get("/{clinic_id}/metrics")
def get_metrics(
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

    metrics = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic_id)
        .order_by(ClinicMetric.recorded_at.desc())
        .all()
    )

    return metrics


@router.get("/{clinic_id}/crowding")
def get_current_crowding(
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

    latest_metric = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic_id)
        .order_by(ClinicMetric.recorded_at.desc())
        .first()
    )

    if not latest_metric:
        raise HTTPException(
            status_code=404,
            detail="No clinic metrics available"
        )

    previous_metric = (
        db.query(ClinicMetric)
        .filter(
            ClinicMetric.clinic_id == clinic_id,
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

    return {
        "clinic_id": clinic.id,
        "clinic_name": clinic.name,
        "patients_waiting": latest_metric.patients_waiting,
        "capacity": clinic.capacity,
        "crowding_percentage": crowding,
        "crowding_level": level,
        "estimated_wait_minutes": estimated_wait,
        "trend": trend,
        "recorded_at": latest_metric.recorded_at
    }


@router.get("/{clinic_id}/forecast")
def get_crowding_forecast(
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

    latest_metric = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic_id)
        .order_by(ClinicMetric.recorded_at.desc())
        .first()
    )

    if not latest_metric:
        raise HTTPException(
            status_code=404,
            detail="No clinic metrics available"
        )

    historical_averages = get_hourly_crowding_averages(
        db,
        clinic_id,
        clinic.capacity
    )

    forecast = generate_forecast(
        patients_waiting=latest_metric.patients_waiting,
        patients_arriving=latest_metric.patients_arrived,
        patients_served=latest_metric.patients_served,
        capacity=clinic.capacity,
        start_hour=latest_metric.recorded_at.hour,
        historical_averages=historical_averages
    )

    current_crowding = calculate_crowding(
        latest_metric.patients_waiting,
        clinic.capacity
    )
    current_level = get_crowding_level(current_crowding)

    advice = generate_advice(current_level, forecast)

    return {
        "clinic_id": clinic.id,
        "clinic_name": clinic.name,
        "forecast": forecast,
        "advice": advice
    }
@router.get("/{clinic_id}/recommendations")
def get_clinic_recommendations(
    clinic_id: int,
    db: Session = Depends(get_db)
):

    selected_clinic = (
        db.query(Clinic)
        .filter(Clinic.id == clinic_id)
        .first()
    )

    if not selected_clinic:
        raise HTTPException(
            status_code=404,
            detail="Clinic not found"
        )

    latest_selected_metric = (
        db.query(ClinicMetric)
        .filter(
            ClinicMetric.clinic_id == clinic_id
        )
        .order_by(
            ClinicMetric.recorded_at.desc()
        )
        .first()
    )

    if not latest_selected_metric:
        raise HTTPException(
            status_code=404,
            detail="No metrics available for selected clinic"
        )

    selected_crowding = calculate_crowding(
        latest_selected_metric.patients_waiting,
        selected_clinic.capacity
    )

    clinics = (
        db.query(Clinic)
        .filter(Clinic.id != clinic_id)
        .all()
    )

    recommendations = []

    for clinic in clinics:

        latest_metric = (
            db.query(ClinicMetric)
            .filter(
                ClinicMetric.clinic_id == clinic.id
            )
            .order_by(
                ClinicMetric.recorded_at.desc()
            )
            .first()
        )

        if not latest_metric:
            continue

        crowding = calculate_crowding(
            latest_metric.patients_waiting,
            clinic.capacity
        )

        # Only recommend clinics that are less crowded
        if crowding >= selected_crowding:
            continue

        estimated_wait = calculate_estimated_wait(
            latest_metric.patients_waiting,
            latest_metric.patients_served,
            latest_metric.average_wait_minutes
        )

        distance = None

        if (
            selected_clinic.latitude is not None
            and selected_clinic.longitude is not None
            and clinic.latitude is not None
            and clinic.longitude is not None
        ):
            distance = calculate_distance_km(
                selected_clinic.latitude,
                selected_clinic.longitude,
                clinic.latitude,
                clinic.longitude
            )

        level = get_crowding_level(crowding)

        recommendations.append({
            "clinic_id": clinic.id,
            "clinic_name": clinic.name,
            "location": clinic.location,
            "crowding_percentage": crowding,
            "crowding_level": level,
            "estimated_wait_minutes": estimated_wait,
            "distance_km": distance,
            "reason": "Lower crowding than selected clinic"
        })

    # Prefer clinics that are both less crowded and closer.
    recommendations.sort(
        key=lambda x: (
            x["distance_km"]
            if x["distance_km"] is not None
            else 999999,
            x["crowding_percentage"]
        )
    )

    return {
        "selected_clinic": {
            "id": selected_clinic.id,
            "name": selected_clinic.name,
            "crowding_percentage": selected_crowding
        },
        "recommendations": recommendations[:3]
    }