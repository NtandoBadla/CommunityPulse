from sqlalchemy.orm import Session

from backend.models.clinic import Clinic
from backend.models.clinic_metric import ClinicMetric
from backend.services.distance_service import calculate_distance_km

from backend.services.prediction_service import (
    calculate_crowding,
    get_crowding_level,
    calculate_estimated_wait,
)


def get_recommendations_for_clinic(db: Session, clinic_id: int):
    """
    Returns the selected clinic's current crowding plus up to 3
    less-crowded alternatives, sorted by distance then crowding.
    Raises ValueError if the clinic or its metrics are missing.
    """

    selected_clinic = (
        db.query(Clinic)
        .filter(Clinic.id == clinic_id)
        .first()
    )

    if not selected_clinic:
        raise ValueError("Clinic not found")

    latest_selected_metric = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic_id)
        .order_by(ClinicMetric.recorded_at.desc())
        .first()
    )

    if not latest_selected_metric:
        raise ValueError("No metrics available for selected clinic")

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
            .filter(ClinicMetric.clinic_id == clinic.id)
            .order_by(ClinicMetric.recorded_at.desc())
            .first()
        )

        if not latest_metric:
            continue

        crowding = calculate_crowding(
            latest_metric.patients_waiting,
            clinic.capacity
        )

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

    recommendations.sort(
        key=lambda x: (
            x["distance_km"] if x["distance_km"] is not None else 999999,
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