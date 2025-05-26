
from navegation import NavPoint, NavSegment, NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = {}     # key: number, value: NavPoint
        self.navsegments = []   # List of NavSegment
        self.navairports = []   # List of NavAirport

    def load_navpoints(self, filename: str):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                number = int(parts[0])
                name = parts[1]
                latitude = float(parts[2])
                longitude = float(parts[3])
                self.navpoints[number] = NavPoint(number, name, latitude, longitude)

    def load_navsegments(self, filename: str):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                origin = int(parts[0])
                dest = int(parts[1])
                dist = float(parts[2])
                self.navsegments.append(NavSegment(origin, dest, dist))

    def load_airports(self, filename: str):
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            i = 0
            while i < len(lines):
                name = lines[i]
                i += 1
                sids = []
                while i < len(lines) and lines[i].endswith(".D"):
                    navpoint = self._find_navpoint_by_name(lines[i])
                    if navpoint:
                        sids.append(navpoint)
                    i += 1
                stars = []
                while i < len(lines) and lines[i].endswith(".A"):
                    navpoint = self._find_navpoint_by_name(lines[i])
                    if navpoint:
                        stars.append(navpoint)
                    i += 1
                self.navairports.append(NavAirport(name, sids, stars))

    def _find_navpoint_by_name(self, name: str):
        for navpoint in self.navpoints.values():
            if navpoint.name == name:
                return navpoint
        return None
