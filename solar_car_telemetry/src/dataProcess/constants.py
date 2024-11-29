"""
This file contains all the relevant constants used in the simulation.
It originated from a Matlab file called init.m.
"""

# UNIT CONVERSIONS
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
INCH_TO_METER = 0.0254
UNIT_TO_KILO = 1 / 1000
LBF_TO_KG = 0.45359237
WHEEL_DIAMETER_METERS = 22 * INCH_TO_METER  # Meters
SPEED_TO_RPM = 60 / (WHEEL_DIAMETER_METERS * np.pi)

# SIMULATION PARAMETERS
MAX_TIME_STEP = 300  # seconds, time step will never be longer than this
START_TIME = 0  # seconds
END_TIME = 0  # seconds
PROFILE_LENGTH = END_TIME - START_TIME  # seconds, duration of sim
TIME_RES = 10  # seconds

# PHYSICS CONSTANTS
C_ROLLING_RESISTANCE = 0.0025  # coefficient of rolling resistance
GRAVITY = 9.81  # m/s^2, gravitational acceleration

# POWER CONTROL
TARGET_POWER = 500
P_POWER = 1          # Power P
I_POWER = 0.01       # Power I
D_POWER = 0.01       # Power D

# CAR PROPERTIES
CAR_MASS = 447.90 * LBF_TO_KG  # data from CarWeightCalc.xlsx
DRIVER_MASS = 176 * LBF_TO_KG  # driver plus ballast
TOTAL_MASS = CAR_MASS + DRIVER_MASS  # total mass of the vehicle
FRONTAL_AREA = 1.262  # meters^2, Source: Ben Colby

# WHEEL PROPERTIES
WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER_METERS * np.pi  # meters
WHEEL_RADIUS = WHEEL_DIAMETER_METERS / 2  # meters
REGEN_ON = 1  # flag to indicate regeneration is enabled

# ELECTRONICS
Fan_draw = 4.8  # Watts
Driver_display_draw = 2.5  # Watts
Headlight_draw = 2  # Watts

# BATTERY PROPERTIES
HV_PACK_VOLTAGE = 96  # Volts; TEMPORARY until voltage curve is derived
HV_PACK_CAPACITY = 80  # Amp-hours
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO  # kWh
STARTING_KWH = FULL_PACK_KWH * (1 - 0.00)  # 100% State of Charge
FINAL_KWH = 0  # kWh, battery level for variable time run to end
MAX_SOC = 0.99  # maximum state of charge
MIN_SOC = 0.1  # minimum state of charge

# SPEED CONTROL
TARGET_SPEED = 20  # meters/second
ACCEL_TOLERANCE = 1  # tolerance for acceleration
P_SPEED = 1      # Speed P
I_SPEED = 0.01   # Speed I
D_SPEED = 0.01   # Speed D

# AIR PROPERTIES
AIR_DENSITY = 1.2  # kg/m^3, air density
DRAG_COEFFICIENT = 0.25  # drag coefficient, TEMPORARY until drag curve is derived (CFD)