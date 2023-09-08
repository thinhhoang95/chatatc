import math
from scipy.integrate import solve_ivp
from dynamics import fx as fx_dynamics
import numpy as np
from converter import ft_to_m, ms_to_fpm, ms_to_knots, rad_to_deg

import utm

class Aircraft:
    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0
    
    def __init__(self, callsign, x, y, z, Vs, khi, mu, r_phi, V, c, kpz, kdz, kiz, kpvs, kpkhi, kdkhi, kikhi, kpmu, kdmu, kimu, kpV, kiV) -> None:
        self.callsign = callsign
        
        # Initialize state variables
        self.x = x
        self.y = y
        self.z = z
        self.Vs = Vs
        self.khi = khi
        self.mu = mu
        self.r_phi = r_phi
        self.V = V
        
        # Model parameters
        self.c = c
        
        # feedback control parameters
        self.kpz = kpz
        self.kdz = kdz
        self.kiz = kiz
        self.kpvs = kpvs
        self.kpkhi = kpkhi
        self.kdkhi = kdkhi
        self.kikhi = kikhi
        self.kpmu = kpmu
        self.kdmu = kdmu
        self.kimu = kimu
        self.kpV = kpV
        self.kiV = kiV
        
        # desired, or reference values
        self.V_desired = V
        self.khi_desired = khi
        self.z_desired = z
        
    # State vector: [x, y, z, z_dot, khi, mu, r_phi, V, eta_z, eta_khi, eta_V]
    
    def speed_to(self, V_desired):
        self.V_desired = V_desired
        
    def heading_to(self, khi_desired):
        self.khi_desired = khi_desired
        
    def altitude_to(self, z_desired):
        self.z_desired = z_desired
        
    def get_response(self, t_span, dt=0.05):
        t_vec = np.linspace(t_span[0], t_span[1], int((t_span[1] - t_span[0]) / dt))
        # response = np.zeros((len(t_vec), 7))
        
        x_init = np.array([self.x, self.y, self.z, self.Vs, self.khi, self.mu, self.r_phi, self.V, 0, 0, 0, 0])
        sol = solve_ivp(fun = fx_dynamics, t_span=t_span, y0=x_init, args=(
            self.V_desired, self.khi_desired, self.z_desired, self.c, self.kpz, self.kdz, self.kiz, self.kpvs, self.kpkhi, self.kdkhi, self.kikhi, self.kpmu, self.kdmu, self.kimu, self.kpV, self.kiV
            ), t_eval=t_vec,method='RK45')

        self.sol_temp = sol
        return sol.t, sol.y
    
    ### TO REVISE ###
    def commit_state_update(self): # to revise
        if self.sol_temp is not None:
            self.xe = self.sol_temp.y[0][-1]
            self.ye = self.sol_temp.y[1][-1]
            self.he = self.sol_temp.y[2][-1]
            self.he_dot = self.sol_temp.y[3][-1]
            self.khi = self.sol_temp.y[4][-1]
            self.mu = self.sol_temp.y[5][-1]
            self.V = self.sol_temp.y[6][-1]
            self.sol_temp = None
        else:
            print("WARNING: No state update to commit.")
    
    def get_usable_state(self, x): # to revise
        xe = x[0]
        ye = x[1]
        he = x[2]
        he_dot = x[3]
        khi = x[4]
        mu = x[5]
        V = x[6]
        
        lat, lon = utm.to_latlon(xe, ye, 48, 'P')
        hexx = ft_to_m(he)
        he_dotx = ms_to_fpm(he_dot)
        khix = rad_to_deg(khi)
        mux = rad_to_deg(mu)
        Vx = ms_to_knots(V)
        
        return np.array([lat, lon, hexx, he_dotx, khix, mux, Vx])
        