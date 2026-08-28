from math import radians, sin, cos, sqrt, atan2


def calculate_distance_km(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
):

    earth_radius_km = 6371

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    difference_latitude = radians(
        latitude2 - latitude1
    )

    difference_longitude = radians(
        longitude2 - longitude1
    )

    a = (
        sin(difference_latitude / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(difference_longitude / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(
        earth_radius_km * c,
        2
    )