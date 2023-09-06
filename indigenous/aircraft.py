import math

class Aircraft:
    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0
    
    def __init__(self, callsign, V, khi, mu, he, c, Wx, Wy, khe, kmu, kV, sigma_he, sigma_mu, sigma_V) -> None:
        self.callsign = callsign
        
        # kinematic parameters
        self.V = V # ground speed
        # we don't need flight path angle because we have vertical speed
        self.khi = khi # heading angle
        self.mu = mu # roll angle
        self.he = he # altitude
        
        # wind parameters
        self.Wx = Wx # wind speed in x direction
        self.Wy = Wy # wind speed in y direction
        
        # feedback control parameters
        self.khe = khe # feedback term for vertical speed control: h_dot_dot = -khe * (he - he_desired) + epsilon_he = -V * sin(gamma)
        self.kmu = kmu # feedback term for roll control: mu_dot = -kmu * (khi - khi_desired) + epsilon_mu
        self.kV = kV # feedback term for ground speed control: V_dot = -kV * (V - V_desired) + epsilon_v
        self.c = c # constant for yaw rate: khi_dot = c/V * sin(mu)
        
        # noise parameters
        self.sigma_he = sigma_he # standard deviation of vertical speed noise
        self.sigma_mu = sigma_mu # standard deviation of roll angle noise
        self.sigma_V = sigma_V # standard deviation of ground speed noise
        
        # desired, or reference values
        self.V_desired = V
        self.khi_desired = khi
        self.he_desired = he
        
    # State vector: [xe, ye, he, he_dot, khi, mu, V]
    
    def speed_to(self, V_desired):
        self.V_desired = V_desired
        
    def heading_to(self, khi_desired):
        self.khi_desired = khi_desired
        
    def altitude_to(self, he_desired):
        self.he_desired = he_desired
        
    def roll(self, t=0.1, dt=0.05):
        # Use Runge-Kutta 4th order method to solve the differential equations
        pass
    
    