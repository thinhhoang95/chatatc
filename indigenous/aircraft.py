import math
from scipy.integrate import solve_ivp
from dynamics import fx as fx_dynamics
import numpy as np
from converter import *

import utm
import json

class Aircraft:
    def deg_to_rad(self, deg):
        return deg * math.pi / 180.0
    
    def __init__(self, callsign, x, y, z, Vs, khi, mu, r_phi, V, eta_z, eta_khi, eta_mu, eta_V, c, kpz, kdz, kiz, kpvs, kpkhi, kdkhi, kikhi, kpmu, kdmu, kimu, kpV, kiV) -> None:
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
        self.eta_z = eta_z
        self.eta_khi = eta_khi
        self.eta_mu = eta_mu
        self.eta_V = eta_V
        
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
        
    # State vector: [x, y, z, z_dot, khi, mu, r_phi, V, eta_z, eta_khi, eta_mu, eta_V]
    
    def speed_to(self, V_desired):
        self.V_desired = V_desired
        self.eta_V = 0
        
    def heading_to(self, khi_desired):
        self.khi_desired = khi_desired
        self.eta_khi = 0
        self.eta_mu = 0
        
    def altitude_to(self, z_desired):
        self.z_desired = z_desired
        self.eta_z = 0
        
    def get_response(self, t_span, dt=0.05):
        t_vec = np.linspace(t_span[0], t_span[1], int((t_span[1] - t_span[0]) / dt))
        # response = np.zeros((len(t_vec), 7))
        
        x_init = np.array([self.x, self.y, self.z, self.Vs, self.khi, self.mu, self.r_phi, self.V, self.eta_z, self.eta_khi, self.eta_mu, self.eta_V])
        sol = solve_ivp(fun = fx_dynamics, t_span=t_span, y0=x_init, args=(
            self.V_desired, self.khi_desired, self.z_desired, self.c, self.kpz, self.kdz, self.kiz, self.kpvs, self.kpkhi, self.kdkhi, self.kikhi, self.kpmu, self.kdmu, self.kimu, self.kpV, self.kiV
            ), t_eval=t_vec,method='RK45')

        self.sol_temp = sol
        return sol.t, sol.y
    
    def commit_state_update(self): # to revise
        if self.sol_temp is not None:
            self.x = self.sol_temp.y[0, -1]
            self.y = self.sol_temp.y[1, -1]
            self.z = self.sol_temp.y[2, -1]
            self.Vs = self.sol_temp.y[3, -1]
            self.khi = self.sol_temp.y[4, -1]
            self.mu = self.sol_temp.y[5, -1]
            self.r_phi = self.sol_temp.y[6, -1]
            self.V = self.sol_temp.y[7, -1]
            self.eta_z = self.sol_temp.y[8, -1]
            self.eta_khi = self.sol_temp.y[9, -1]
            self.eta_mu = self.sol_temp.y[10, -1]
            self.eta_V = self.sol_temp.y[11, -1]
            self.sol_temp = None
        else:
            print("WARNING: No state update to commit.")

    def get_state(self):
        lat, lon = utm.to_latlon(self.x, self.y, 48, 'P')
        z_ft = m_to_ft(self.z)
        state_to_serialize = {
            "callsign": self.callsign,
            "x": self.x,
            "y": self.y,
            "lat": lat,
            "lon": lon,
            "z": z_ft,
            "Vs": ms_to_fpm(self.Vs),
            "psi": degree_fixer(rad_to_deg(khi_to_psi(self.khi))),
            "psi_desired": degree_fixer(rad_to_deg(khi_to_psi(self.khi_desired))),
            "V_desired": ms_to_knots(self.V_desired),
            "V": ms_to_knots(self.V),
            "z_desired": m_to_ft(self.z_desired)
        }
        # json_str = json.dumps(state_to_serialize)
        return state_to_serialize