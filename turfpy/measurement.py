from geojson import Point
from math import radians, sin, cos, degrees, atan2, asin, sqrt


def bearing(start: Point, end: Point, final=False):
    """
    Takes two {@link Point} and finds the geographic bearing between them,
    :param Point start: Start point
    :param Point end: Ending point
    :param boolean final:
    :return float: calculates the final bearing if true

    Example :-
    from turfpy import measurement
    from geojson import Point
    start = Point((-75.343, 39.984))
    end = Point((-75.534, 39.123))
    measurement.bearing(start,end)
    """
    if final:
        return calculate_final_bearing(start, end)
    start_coordinates = start['coordinates']
    end_coordinates = end['coordinates']
    lon1 = radians(float(start_coordinates[0]))
    lon2 = radians(float(end_coordinates[0]))
    lat1 = radians(float(start_coordinates[1]))
    lat2 = radians(float(end_coordinates[1]))

    a = sin(lon2 - lon1) * sin(lat2)
    b = (cos(lat1) * sin(lat2)) - (sin(lat1) * cos(lat2) * cos(lon2 - lon1))
    return degrees(atan2(a, b))


def calculate_final_bearing(start, end):
    bear = bearing(end, start)
    bear = (bear + 180) % 360
    return bear


def distance(point1: Point, point2: Point, unit: str = 'km'):
    """
    Calculates distance between two Points. A point is containing latitude and
    logitude in decimal degrees and ``unit`` is optional.
    It calculates distance in units such as kilometers, meters, miles, feet and inches.
    :param point1: first point; tuple of (latitude, longitude) in decimal degrees
    :param point2: second point; tuple of (latitude, longitude) in decimal degrees
    :param unit: A string containing unit, E.g. kilometers = 'km', miles = 'mi',
    meters = 'm', feet = 'ft', inches = 'in'.
    Example :-

    >>> from turfpy import measurement
    >>> from geojson import Point
    >>> start = Point((-75.343, 39.984))
    >>> end = Point((-75.534, 39.123))
    >>> measurement.distance(start,end)

    :return: The distance between the two points in the requested unit, as a float.
    """
    avg_earth_radius_km = 6371.0088
    conversions = {'km': 1.0, 'm': 1000.0, 'mi': 0.621371192,
                   'ft': 3280.839895013, 'in': 39370.078740158
                   }
    lat1, lon1 = point1['coordinates']
    lat2, lon2 = point2['coordinates']

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    lat = lat2 - lat1
    lon = lon2 - lon1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lon * 0.5) ** 2
    return 2 * avg_earth_radius_km * conversions[unit] * asin(sqrt(d))
