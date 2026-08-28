def calculate_distance_score(
    crowding_percentage: int
):
    """
    Lower crowding produces a better recommendation score.
    """

    return max(
        0,
        100 - crowding_percentage
    )


def get_recommendation_reason(
    crowding_percentage: int
):

    if crowding_percentage < 30:
        return "Low crowding"

    if crowding_percentage < 60:
        return "Moderate crowding"

    if crowding_percentage < 80:
        return "High crowding"

    return "Critical crowding"