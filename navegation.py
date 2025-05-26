class NavPoint:
    def __init__(self, number: int, name: str, latitude: float, longitude: float):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"NavPoint({self.number}, {self.name}, {self.latitude}, {self.longitude})"


class NavSegment:
    def __init__(self, origin_number: int, destination_number: int, distance: float):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

    def __repr__(self):
        return f"NavSegment({self.origin_number} -> {self.destination_number}, {self.distance} km)"


class NavAirport:
    def __init__(self, name: str, sids: list, stars: list):
        self.name = name
        self.sids = sids
        self.stars = stars

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs: {[s.name for s in self.sids]}, STARs: {[s.name for s in self.stars]})"
