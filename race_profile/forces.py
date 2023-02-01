# forces

from constants import *
from motorData import *

def force(v,I):
    return propulsion(I) - drag(v) # - rolling_Resisitance(v)  

def drag(v):
    area = 1.1 # meter^2
    density_air = 1.2 # kg / meter^3
    C_d = drag_coefficient(v)
    return (1/2) * (C_d * density_air * area) * (v**2)

def propulsion(I):
    torque = calculated_torque_current(current)
    return torque * (WHEEL_DIAMETER_METERS / 2)

#def rollingResistance(v):
#    C_rr = rolling_resistance(v)
#    return C_rr * WEIGHT_VEHICLE 

def drag_coefficient(v):
    return 0.1
    
#def rolling_resistance(v):
#    return 