from collections import defaultdict
from sqlalchemy.orm import Session

from backend.models.clinic_metric import ClinicMetric
from backend.services.prediction_service import calculate_crowding


def get_hourly_crowding_averages(
    db: Session,
    clinic_id: int,
    capacity: int
):
    """
    Groups past metrics for a clinic by hour-of-day (0-23) and
    returns the average crowding percentage and sample size per hour.

    Example:
    {
        14: {"avg_crowding": 76.5, "sample_size": 3},
        15: {"avg_crowding": 82.0, "sample_size": 2},
    }
    """
    metrics = (
        db.query(ClinicMetric)
        .filter(ClinicMetric.clinic_id == clinic_id)
        .all()
    )

    buckets = defaultdict(list)

    for metric in metrics:
        hour = metric.recorded_at.hour
        crowding = calculate_crowding(
            metric.patients_waiting,
            capacity
        )
        buckets[hour].append(crowding)

    averages = {}

    for hour, values in buckets.items():
        averages[hour] = {
            "avg_crowding": sum(values) / len(values),
            "sample_size": len(values)
        }

    return averages