import numpy as np

def knots_to_ms(knots):
    return knots * 0.514444444

def ms_to_knots(ms):
    return ms / 0.514444444

def deg_to_rad(deg):
    return deg * np.pi / 180.0

def rad_to_deg(rad):
    return rad * 180.0 / np.pi

def ft_to_m(ft):
    return ft * 0.3048

def m_to_ft(m):
    return m / 0.3048

def nm_to_m(nm):
    return nm * 1852.0

def m_to_nm(m):
    return m / 1852.0

def nm_to_ft(nm):
    return nm * 6076.12

def ft_to_nm(ft):
    return ft / 6076.12

def fpm_to_ms(fpm):
    return fpm * 0.00508

def ms_to_fpm(ms):
    return ms / 0.00508

def khi_to_psi(khi):
    return -khi + np.pi / 2

def psi_to_khi(psi):
    return -psi + np.pi / 2

def degree_fixer(degree):
    # ensure degree is between 0 and 360
    while degree < 0:
        degree += 360
    while degree >= 360:
        degree -= 360
    return degree