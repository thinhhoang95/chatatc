from aircraft import Aircraft
from converter import *
import utm 

import numpy as np


# Create an aircraft object
vvts = (10.8188, 106.652)
vvts_utm = utm.from_latlon(vvts[0], vvts[1], force_zone_number=48, force_zone_letter='P')

# VN19: found 60km to the West and 80km to the North of VVTS, at 210 knots
# flying heading 180 (South) and altitude 5,000 ft, with no wind
# c approximates g
# feedback control parameters khe = kmu = kV = 0.1
# noise parameters sigma_he = sigma_mu = sigma_V = 0.1
vn19 = Aircraft('VN19', x=vvts_utm[0] - 60_000, y=vvts_utm[1] + 80_000, z=ft_to_m(5_000),
                Vs=ms_to_fpm(0),
                khi=deg_to_rad(0), mu=deg_to_rad(0), r_phi = 0, V=knots_to_ms(210),
                eta_z=0, eta_khi=0, eta_mu=0, eta_V=0, # integrated error
                c=9.8, # approx g
                kpz=5, kdz=10, kiz=1e-3, # altitude reference control
                kpvs=10, # FPA control
                kpkhi=240.0, kdkhi=1600.0, kikhi=1.0, # heading control 
                kpmu=0.25, kdmu=0.75, kimu=0.01, # roll reference control
                kpV=0.1, kiV=0. # speed control
)

# vn19.heading_to(deg_to_rad(110))
# vn19.altitude_to(ft_to_m(4_000))

#vn19.heading_to(deg_to_rad(45))
vn19.altitude_to(ft_to_m(3_000))
vn19.speed_to(knots_to_ms(170))

# Get the state response for 3s
t, response = vn19.get_response((0, 180), dt=0.05)

# Plot the response
import matplotlib.pyplot as plt
plt.figure(figsize=(8, 5))
plt.subplot(3, 3, 1)
plt.plot(t, response[0, :])
plt.xlabel('Time (s)')
plt.ylabel('East position (m)')
plt.subplot(3, 3, 2)
plt.plot(t, response[1, :])
plt.xlabel('Time (s)')
plt.ylabel('North position (m)')
plt.subplot(3, 3, 3)
plt.plot(t, m_to_ft(response[2, :]))
plt.xlabel('Time (s)')
plt.ylabel('Altitude (ft)')
plt.subplot(3, 3, 4)
plt.plot(t, ms_to_fpm(response[3, :]))
plt.xlabel('Time (s)')
plt.ylabel('Vertical speed (fpm)')
plt.subplot(3, 3, 5)
# plt.plot(t, rad_to_deg(khi_to_psi(response[4, :])))
plt.plot(t, rad_to_deg(response[4, :]))
plt.xlabel('Time (s)')
plt.ylabel('Heading angle (deg)')
plt.subplot(3, 3, 6)
plt.plot(t, rad_to_deg(response[5, :]))
plt.xlabel('Time (s)')
plt.ylabel('Roll angle (deg)')
plt.subplot(3, 3, 7)
plt.plot(t, rad_to_deg(response[6, :]))
plt.xlabel('Time (s)')
plt.ylabel('Roll rate (deg/s)')
plt.subplot(3, 3, 8)
plt.plot(t, ms_to_knots(response[7, :]))
plt.xlabel('Time (s)')
plt.ylabel('Ground speed (knots)')
plt.subplot(3, 3, 9)
plt.scatter(response[0, :], response[1, :], s=1)
plt.xlabel('East position (m)')
plt.ylabel('North position (m)')


plt.tight_layout()
plt.show()
