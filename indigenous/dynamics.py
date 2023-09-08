# from scipy.integrate import solve_ivp
import numpy as np
from converter import *

### ALL COMPUTATIONS MUST BE DONE IN SI UNITS ###

# STATE VARIABLES
# [x, y, z, z_dot, khi, mu, r_phi, V, eta_z, eta_khi, eta_mu, eta_V]
# Description:
# x: East position
# y: North position
# z: Altitude
# z_dot: Vertical speed
# khi: Heading angle
# mu: Roll angle
# r_phi: Roll rate
# V: Ground speed
# eta_z: Integrated error in altitude
# eta_khi: Integrated error in heading angle
# eta_V: Integrated error in ground speed

# REFERENCE VARIABLES
# [V_ref, khi_ref, z_ref]
# Description:
# V_ref: Desired ground speed
# khi_ref: Desired heading angle
# z_ref: Desired altitude
    
# STATE DYNAMICS
def fx(t, state, V_ref, khi_ref, z_ref, c, kpz, kdz, kiz, kpvs, kpkhi, kdkhi, kikhi, kpmu, kdmu, kimu, kpV, kiV):
    # Unpacking State variables 

    # Fundamental state variables
    x = state[0]
    y = state[1]
    z = state[2]
    Vs = state[3] # vertical speed, or z_dot
    khi = state[4]
    mu = state[5]
    r_mu = state[6] # roll rate
    V = state[7]
    
    # Augmented integrated error state variables
    eta_z = state[8]
    eta_khi = state[9]
    eta_mu = state[10]
    eta_V = state[11]
    
    # Longitudinal dynamics (z, z_dot, V)
    eta_z_dot = z - z_ref
    z_dot = Vs
    Vs_ref = saturation(-kpz * (z - z_ref) - kdz * Vs - kiz * eta_z, -fpm_to_ms(1800), fpm_to_ms(1800)) # vertical speed given by PID control in V/S mode
    # print('Vs_ref: ', ms_to_fpm(Vs_ref))
    Vs_dot = -kpvs * (Vs - Vs_ref) # P control
    eta_V_dot = V - V_ref
    V_dot = -kpV * (V - V_ref) - kiV * eta_V # PI control
    
    # Lateral dynamics (khi, mu)
    x_dot = V * np.cos(khi)
    y_dot = V * np.sin(khi)
    
    eta_khi_dot = khi - khi_ref
    khi_dot = c * np.sin(mu) / V
    
    mu_ref = saturation(-kpkhi * (khi - khi_ref) - kdkhi * (c * np.sin(mu) / V) - kikhi * eta_khi, -deg_to_rad(30), deg_to_rad(30)) # roll angle given by PID control in HDG mode
    # print('mu_ref: ', mu_ref)
    eta_mu_dot = mu - mu_ref
    mu_dot = r_mu # roll rate
    r_mu_dot = -kpmu * (mu - mu_ref) - kdmu * r_mu - kimu * eta_mu # roll rate given by PID control in HDG mode
    
    state_vec = np.array([
        x_dot,
        y_dot,
        z_dot,
        Vs_dot,
        khi_dot,
        mu_dot,
        r_mu_dot,
        V_dot,
        eta_z_dot,
        eta_khi_dot,
        eta_mu_dot,
        eta_V_dot
    ])
    
    return state_vec

def saturation(x, x_min, x_max):
    if x <= x_min:
        return x_min
    elif x >= x_max:
        return x_max
    else:
        return x
    
# GET SATURATION LAW
# Use the "softer" of the two laws
def get_sat_law(main_law, sat_law):
    if np.abs(main_law) < np.abs(sat_law):
        return main_law
    else:
        return sat_law

# GET V/S SATURATION CONTROL
# Control the V/S to the boundary values of +-1500fpm, depending on the sign of Vs
def Vs_dot_law_for_Vs_saturation(Vs, ez, kpvs, Vs_min = fpm_to_ms(-1500), Vs_max = fpm_to_ms(1500)):
    Vs_target = Vs_min
    if ez < 0: # z < z_ref => climb => Vs_target = Vs_max
        Vs_target = Vs_max
        
    return -kpvs * (Vs - Vs_target) # P control

# GET ROLL SATURATION CONTROL
# Control the roll rate to the boundary values of +-30deg/s, depending on the sign of mu
def r_phi_dot_law_for_mu_saturation(mu, e_khi, r_phi, kpmu, kdmu, mu_min = deg_to_rad(-30), mu_max = deg_to_rad(30)):
    mu_target = mu_min
    if e_khi < 0: # khi < khi_ref => need to increase khi => khi_dot > 0 => mu > 0 => mu_target = mu_max
        mu_target = mu_max
        
    return -kpmu * (mu - mu_target) - kdmu * r_phi # PD control
    
# def fx(t, x, V_desired, khi_desired, he_desired, c, Wx, Wy, khe, kmu, kV, sigma_he, sigma_mu, sigma_V):
#     # State variables
#     xe = x[0]
#     ye = x[1]
#     he = x[2]
#     he_dot = x[3]
#     khi = x[4]
#     mu = x[5]
#     V = x[6]
#     # Reference values
#     # V_desired, khi_desired, he_desired
    
#     # Additional arguments
#     # c, Wx, Wy, khe, kmu, kV, sigma_he, sigma_mu, sigma_V
    
#     # Sample noise
#     epsilon_he = np.random.normal(0, sigma_he)
#     epsilon_mu = np.random.normal(0, sigma_mu)
#     epsilon_V = np.random.normal(0, sigma_V)
    
#     # State dynamics
#     return np.array([
#         V * np.cos(khi) + Wx, # xe_dot, or east speed response
#         V * np.sin(khi) + Wy, # ye_dot, or north speed response
#         he_dot, # he_dot, or vertical speed response
#         sat(-khe * (he - he_desired) + epsilon_he, x_min = fpm_to_ms(-1500), x_max = fpm_to_ms(1500)), # he_dot_dot, or vertical speed control
#         c * np.sin(mu) / V, # khi_dot, or heading angle response
#         sat(-kmu * (khi - khi_desired) + epsilon_mu, x_min = deg_to_rad(-30), x_max = deg_to_rad(30)), # mu_dot, or roll angle control
#         -kV * (V - V_desired) + epsilon_V # V_dot, or ground speed control
#     ])