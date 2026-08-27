def calculate_crowding(
    patients_waiting: int,
    capacity: int
):
    if capacity <= 0:
        return 0

    percentage = (patients_waiting / capacity) * 100

    return min(round(percentage), 100)


def get_crowding_level(
    crowding_percentage: int
):
    if crowding_percentage < 30:
        return "LOW"

    if crowding_percentage < 60:
        return "MODERATE"

    if crowding_percentage < 80:
        return "HIGH"

    return "CRITICAL"


def calculate_estimated_wait(
    patients_waiting: int,
    patients_served: int,
    average_wait_minutes: float
):
    if patients_served <= 0:
        return round(average_wait_minutes)

    estimated_wait = (
        patients_waiting / patients_served
    ) * average_wait_minutes

    return round(estimated_wait)


def calculate_trend(
    current_waiting: int,
    previous_waiting: int
):
    if current_waiting > previous_waiting:
        return "INCREASING"

    if current_waiting < previous_waiting:
        return "DECREASING"

    return "STABLE"


def blend_with_history(
    trend_crowding: int,
    historical_averages: dict,
    target_hour: int,
    min_samples: int = 2,
    max_weight: float = 0.6
):
    """
    Blends a trend-based crowding estimate with the historical
    average for that hour-of-day, when enough history exists.
    """
    bucket = historical_averages.get(target_hour)

    if not bucket or bucket["sample_size"] < min_samples:
        return trend_crowding

    weight = min(bucket["sample_size"] / 5, max_weight)

    blended = (
        weight * bucket["avg_crowding"]
        + (1 - weight) * trend_crowding
    )

    return min(round(blended), 100)


def generate_forecast(
    patients_waiting: int,
    patients_arriving: int,
    patients_served: int,
    capacity: int,
    hours: int = 3,
    start_hour: int | None = None,
    historical_averages: dict | None = None
):

    forecast = []
    waiting = patients_waiting
    net_change = patients_arriving - patients_served
    historical_averages = historical_averages or {}

    for hour in range(1, hours + 1):

        waiting = max(
            0,
            waiting + net_change
        )

        trend_crowding = calculate_crowding(
            waiting,
            capacity
        )

        if start_hour is not None:
            target_hour = (start_hour + hour) % 24
            crowding = blend_with_history(
                trend_crowding,
                historical_averages,
                target_hour
            )
        else:
            crowding = trend_crowding

        level = get_crowding_level(
            crowding
        )

        forecast.append({
            "hour_ahead": hour,
            "predicted_patients_waiting": waiting,
            "predicted_crowding_percentage": crowding,
            "predicted_level": level
        })

    return forecast