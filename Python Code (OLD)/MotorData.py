# Motor Data

import numpy as np

from constants import *


# Mathematical function to output expected Torgue from an input current
# Units are:
#   Current: Amps
#   Torque: Newton-meters
# Based on fit performed on manufacturer data sheet
# Must be updated after motor test has been completed
def calculated_torque_current(current):
    torque = (1.097)*current -0.5933
    return torque


# Mathematical function to output expected RPM from an input current
# Units are:
#   Current: Amps
#   Revs: Revolutions per minute
# Based on fit performed on manufacturer data sheet
# Must be updated after motor test has been completed
def calculated_RPM_current(current):
    rpm = (-4.114)*current + 888.5
    return rpm

def calculated_speed_current(current):
    rpm = calculated_RPM_current(current)
    speed = rpm * WHEEL_CIRCUMFRENCE / SECONDS_PER_MINUTE
    return speed


# Mathematical function to output expected efficiency from an input current
# Units are:
#   Current: Amps
#   Efficiency: Percent
# Based on fit performed on manufacturer data sheet
# Must be updated after motor test has been completed
def calculated_efficiency_current(current):
    a = -7441
    b = 133.3
    c = -31.09
    d = 98.39
    efficiency = a*((b*current+c)**(-1))+d
    return efficiency 
