"""
This is a Python adaptation of a Matlab file (init.m) that
initializes all variables and data for running the "Car.slx"
Simulink model of a solar car using spreadsheet data.
"""

#Import statements:
import pandas as pd
import numpy as np

# UNIT CONVERSIONS:
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
INCH_TO_METER = 0.0254
UNIT_TO_KILO = 1 / 1000
LBF_TO_KG = 0.45359237
WHEEL_DIAMETER_METERS = 22 * INCH_TO_METER # Meters
SPEED_TO_RPM = 60 / (WHEEL_DIAMETER_METERS * np.pi)

# SIMULATION PARAMETERS
# Time
MAX_TIME_STEP = 300  # seconds, time step will never be longer than this
START_TIME = 0  # seconds,
END_TIME = 0  # seconds
PROFILE_LENGTH = END_TIME - START_TIME  # seconds, duration of sim
TIME_RES = 10  # seconds

# Rolling resistance and gravitational acceleration
C_ROLLING_RESISTANCE = 0.0025  # coefficient of rolling resistance
GRAVITY = 9.81  # m/s^2, gravitational acceleration

# Power control constants (PID control)
TARGET_POWER = 500
P_POWER = 1
I_POWER = 0.01
D_POWER = 0.01

#CAR PROPERTIES:
#Mass Properties
CAR_MASS = 447.90 * LBF_TO_KG  # data from CarWeightCalc.xlsx
DRIVER_MASS = 176 * LBF_TO_KG  # driver plus ballast
TOTAL_MASS = CAR_MASS + DRIVER_MASS  # total mass of the vehicle
FRONTAL_AREA = 1.262  # meters^2, Source: Ben Colby

# Dimensions
# Wheel properties
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER_METERS * np.pi  # meters
WHEEL_RADIUS = WHEEL_DIAMETER_METERS / 2  # meters
WHEEL_DIAMETER_METERS = 22 * INCH_TO_METER
REGEN_ON = 1  # flag to indicate regeneration is enabled

# Misc Electronics
Fan_draw = 4.8  # Watts
Driver_display_draw = 2.5  # Watts
Headlight_draw = 2  # Watts

# Load in data from sheets (constant values also included for testing):
# ELEVATION DATA:
Elevation_filename = 'Data/flat_course.csv'

Course = pd.read_csv(Elevation_filename)
distance = Course.distance
elevation = Course.elevation
slope = Course.slope

#SOLAR DATA
solar_filename = 'Data/const_solar.csv'
Solar = pd.read_csv(solar_filename)
times = Solar.Time
irradiance = Solar.Irradiance

#AERODYNAMIC DATA
drag_filename = 'Data/const_drag.csv'
Drag = pd.read_csv(drag_filename)
speeds = Drag.velocity

# TIRE DATA - we may treat this with a best fit line instead
C_RR = 0.0017 * np.exp(0.0054 * speeds)  # SOURCE: Ben Colby
PRESSURE = 500 / UNIT_TO_KILO  # Pa, tire pressure

#BATTERY DATA
#Voltage and Capacity
HV_PACK_VOLTAGE = 96  # Volts; TEMPORARY until voltage curve is derived
HV_PACK_CAPACITY = 80  # 57 # Amp-hours
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO  # kWh
STARTING_KWH = FULL_PACK_KWH * (1 - 0.00)  # 100% State of Charge
FINAL_KWH = 0  # kWh, battery level for variable time run to end
# Battery Management System
MAX_SOC = 0.99  # maximum state of charge
MIN_SOC = 0.1  # minimum state of charge

battery_filename = 'Data/const_battery.csv'
Battery = pd.read_csv(battery_filename)
SOC = Battery.SOC
voltage = Battery.Voltage

#MOTOR DATA
motorEco_filename = 'Data/MotorDataEco.csv'
Motor = pd.read_csv(motorEco_filename)
currents_eco = Motor.Current
Torque_eco = Motor.Torque
RPM_eco = Motor.RPM

# TARGET SPEED
# Control system and speed control constants
TARGET_SPEED = 20  # meters/second
ACCEL_TOLERANCE = 1  # tolerance for acceleration
P_SPEED = 1  # Speed P
I_SPEED = 0.01  # Speed I
D_SPEED = 0.01  # Speed D

CruiseSpeed_filename = 'Data/constTargetSpeed.csv'
Cruise = pd.read_csv(CruiseSpeed_filename)
distance = Cruise.distance
speeds = Cruise.TargetSpeed

# AIR DENSITY
# Air properties and drag coefficient
AIR_DENSITY = 1.2  # kg/m^3, air density
DRAG_COEFFICIENT = 0.25  # drag coefficient, TEMPORARY until drag curve is derived (CFD)

density_filename = 'Data/constDensity.csv'
Density = pd.read_csv(density_filename)
density_elevation = Density.Elevation
density = Density.density

# We will run our simulation, take the resulting data and output this, ideally as a CSV.
# simulation = sim("Car.slx")
# out = extractTimetable(simulation)
# out.to_csv("output.csv")

# Save Data: