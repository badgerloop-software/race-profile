"""
This file allows us to read the fake data that we have into Pandas dataframes.
It originated from a Matlab file called init.m.
"""

import pandas as pd
import numpy as np
import constants as const

def load_data():
    # ELEVATION DATA - from flat_course.csv
    Course = pd.read_csv('Data/flat_course.csv')
    distance = Course.distance
    elevation = Course.elevation
    slope = Course.slope

    # SOLAR DATA - from const_solar.csv
    Solar = pd.read_csv('Data/const_solar.csv')
    times = Solar.Time
    irradiance = Solar.Irradiance

    # AERODYNAMIC DATA - from const_drag.csv
    Drag = pd.read_csv('Data/const_drag.csv')
    speeds = Drag.velocity
    C_RR = 0.0017 * np.exp(0.0054 * speeds)  # SOURCE: Ben Colby
    PRESSURE = 500 / const.UNIT_TO_KILO  # Pa, tire pressure

    # BATTERY DATA - from const_battery.csv
    Battery = pd.read_csv('Data/const_battery.csv')
    SOC = Battery.SOC
    voltage = Battery.Voltage

    # MOTOR DATA - from MotorDataEco.csv
    Motor = pd.read_csv('Data/MotorDataEco.csv')
    currents_eco = Motor.Current
    Torque_eco = Motor.Torque
    RPM_eco = Motor.RPM

    # CRUISE SPEED DATA - from constTargetSpeed.csv 
    Cruise = pd.read_csv('Data/constTargetSpeed.csv')
    cruise_distance = Cruise.distance
    target_speeds = Cruise.TargetSpeed

    # AIR DENSITY DATA - from constDensity.csv
    Density = pd.read_csv('Data/constDensity.csv')
    density_elevation = Density.Elevation
    density = Density.density

    print(density)

    return {
        'course': Course,
        'solar': Solar,
        'drag': Drag,
        'battery': Battery,
        'motor': Motor,
        'cruise': Cruise,
        'density': Density,
        'c_rr': C_RR
    }