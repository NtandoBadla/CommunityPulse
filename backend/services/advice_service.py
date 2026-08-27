def generate_advice(
    current_level: str,
    forecast: list[dict]
):
    if current_level == "CRITICAL":
        return (
            "This clinic is extremely busy right now. "
            "Consider visiting another clinic or coming back later today."
        )

    worsening_hour = None

    for entry in forecast:
        if entry["predicted_level"] in ("HIGH", "CRITICAL"):
            worsening_hour = entry
            break

    if worsening_hour:
        hours_ahead = worsening_hour["hour_ahead"]
        return (
            f"This clinic is expected to become very busy "
            f"within the next {hours_ahead} hour(s). "
            f"Visit soon if you can, or consider another nearby clinic."
        )

    if current_level in ("LOW", "MODERATE"):
        return "This clinic is not too busy right now, a good time to visit."

    return "Crowding levels are expected to stay stable."