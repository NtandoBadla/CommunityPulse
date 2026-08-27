def calculate_crowding(patients_waiting, capacity):
    percentage = (patients_waiting / capacity) * 100

    return min(round(percentage), 100)


def calculate_forecast(
    patients_waiting,
    patients_arriving_per_hour,
    patients_served_per_hour,
    capacity,
    hours=3
):
    forecasts = []

    current_waiting = patients_waiting

    for hour in range(hours):
        current_waiting += (
            patients_arriving_per_hour
            - patients_served_per_hour
        )

        current_waiting = max(current_waiting, 0)

        crowding = calculate_crowding(
            current_waiting,
            capacity
        )

        forecasts.append({
            "hour": hour + 1,
            "patients_waiting": current_waiting,
            "crowding_percentage": crowding
        })

    return forecasts