import math

class Aircraft:
    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0

    def __init__(self, lat, lon, alt, gs, vs, hdg) -> None:
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.gs = gs
        self.vs = vs
        self.hdg = hdg # must be in radians
    
    def predict_state(self, dt):
        self.lat = self.lat + self.gs * dt * math.cos(self.hdg)
        self.lon = self.lon + self.gs * dt * math.sin(self.hdg)
        self.alt = self.alt + self.vs * dt
        return (self.lat, self.lon, self.alt, self.gs, self.vs, self.hdg)
