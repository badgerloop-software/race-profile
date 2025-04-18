import math
from datetime import datetime
import numpy as np

constants = {
    # Data Sources
    "COURSE_DATA_FILE": "course_data/ASC_2024/ASC_2024_A.csv",
    "ECO_DATA_FILE": "Data/MotorDataEco.csv",
    "POWER_DATA_FILE": "Data/MotorDataEco.csv",  # Replace later

    #Constants used for Car Sim

    # Non-Configurable Constants
    "SECONDS_PER_HOUR": 3600,
    "SECONDS_PER_MINUTE": 60,
    "INCH_TO_METER": 0.0254,
    "UNIT_TO_KILO": 1 / 1000,
    "LBF_TO_KG": 0.45359237,

    # Simulation time-window
    "PROFILE_LENGTH": 1800,

    # Configurable Constants
    "TIME_RES": 10,  # Seconds
    # %START_TIME = 9*(SECONDS_PER_HOUR) + 0*(SECONDS_PER_MINUTE); % start time of day
    # %END_TIME = 9.5*(SECONDS_PER_HOUR) + 0*(SECONDS_PER_MINUTE); % end time of day
    # %PROFILE_LENGTH = END_TIME - START_TIME; % Seconds
}

# Adding derived constants

constants.update({
    "CURRENT_TIME": round(datetime.now().second + datetime.now().microsecond / 1_000_000, 4) # Placeholder for current race time
})

# Add constants that depend on previous ones
constants.update({
    "START_TIME": constants["CURRENT_TIME"],
    "END_TIME": constants["CURRENT_TIME"] + constants["PROFILE_LENGTH"],
    
    "HV_PACK_VOLTAGE": 96,  # Volts TEMPORARY until voltage curve is derived
    "HV_PACK_CAPACITY": 80,  # Amp-hours % 57 % Amp-hours
    "WHEEL_DIAMETER_METERS": 22 * constants["INCH_TO_METER"],  # Meters
    "FINAL_KWH": 0,  # KwH, battery level for variable time run to end
    "CAR_MASS": 447.90 * constants["LBF_TO_KG"],  # data from CarWeightCalc.xlsx
    "DRIVER_MASS": 176 * constants["LBF_TO_KG"],
    "AIR_DENSITY": 1.2,  # kg m^-3
    "FRONTAL_AREA": 1,
    "DRAG_COEFFICIENT": 0.25,
    "C_ROLLING_RESISTANCE": 0.0025,
    "GRAVITY": 9.81,  # gravitational acceleration m s^-2
})

# Add speed to RPM conversion constant (depends on wheel diameter)
constants.update({
    "SPEED_TO_RPM": 60 / (constants["WHEEL_DIAMETER_METERS"] * math.pi),
})

# Controls
constants.update({
    #MOTOR_CONSTANT = % CHECK THIS
    "CONTROL_MODE": 1,   # power-control = 1, speed-control = 0
    "TARGET_SPEED": 12,  # Meters / Second
    "ACCEL_TOLERANCE": 1,
    "P_SPEED": 25,    # Speed P
    "I_SPEED": 3,     # Speed I
    "D_SPEED": 40,    # Speed D
    "TARGET_POWER": 700,  # kW
    "P_POWER": 10,
    "I_POWER": 1,
    "D_POWER": 1,
})

# Battery Management System
constants.update({
    "MAX_SOC": 0.99,
    "MIN_SOC": 0.05,
})

# Wether Data
# TEMP = 

# Dependent Constants
constants.update({
    "WHEEL_CIRCUMFRENCE": constants["WHEEL_DIAMETER_METERS"] * math.pi,  # Meters
    "WHEEL_RADIUS": constants["WHEEL_DIAMETER_METERS"] / 2,
    "FULL_PACK_KWH": constants["HV_PACK_VOLTAGE"] * constants["HV_PACK_CAPACITY"] * constants["UNIT_TO_KILO"],  # kWh
})

# More dependent constants
constants.update({
    "STARTING_KWH": constants["FULL_PACK_KWH"] * (1 - 0),  # 100% State of Charge
    "TOTAL_MASS": constants["CAR_MASS"] + constants["DRIVER_MASS"],
})

# Low Voltage
constants.update({
    "FAN_DRAW": 4.8,  # Watts
    "DRIVER_DISPLAY_DRAW": 2.5,  # Watts
    "HEADLIGHT_DRAW": 2,  # Watts
    "REGEN_ON": 0,
})

## Data

## Course Parameters, temporary until course data is included 
## DISTANCE = [1:50e3, (1+50e3):200e3];% distance traveled along course, should be meters
## fronthalf = length(1:50e3);
## backhalf= length((1+50e3):200e3);
## GRADE_ANGLE = -[0*ones(1,fronthalf), 0.03*ones(1,backhalf)];
## GRADE_ANGLE(1, floor(length(DISTANCE)/2):end) = 0.1*ones(1, floor(length(DISTANCE)/2) + 1);
## INPUT COURSE HERE
## INT_DISTANCES = DISTANCE(1):0.25:DISTANCE(end);
## INT_GRADE_ANGLE = interp1(DISTANCE, GRADE_ANGLE, INT_DISTANCES,'spline');

# COURSE_DATA = readmatrix(COURSE_DATA_FILE);
# COURSE_DATA(1,6) = COURSE_DATA(2,6); % Populate first heading val
# COURSE_DATA(1,7) = 0;%COURSE_DATA(2,7); % Populate first slope val
# COURSE_DATA(1,9) = 0; % Populate first interval
# NANS = isnan(COURSE_DATA(:,7));
# DUPLICATES = [0; (diff(COURSE_DATA(:,8)) == 0)];
# COURSE_FILTER = (~NANS) & (~DUPLICATES);
# COURSE_DATA = COURSE_DATA(COURSE_FILTER, :);
# INT_DISTANCES = COURSE_DATA(:, 8) / UNIT_TO_KILO; % Converto to m
# INT_GRADE_ANGLE = rad2deg(atan(COURSE_DATA(:, 7)/100)); % convert % to deg

# Tire Data
constants.update({
    "SPEED_DATA_TIRE": [50, 80, 100],  # km/h
    "ROLLING_RESISTANCE": [2.30/1000, 2.68/1000, 3.02/1000],  # unitless
    "PRESSURE": 500 / constants["UNIT_TO_KILO"],  # Pa
})

# Solar Data - using lambda for dynamic calculation
constants.update({
    "SOLAR_TIME_BREAKPOINTS": np.arange(constants['START_TIME'], constants['END_TIME'] + 1, 900).tolist(),
})

# Function to calculate the forecasted irradiance
def calculate_forecasted_irradiance(time_points, start_time, end_time, profile_length):
    return [-5*((t-start_time)*(t-end_time) / (profile_length/2)**2) for t in time_points]

constants["FORECASTED_IRRADIANCE"] = calculate_forecasted_irradiance(
    constants["SOLAR_TIME_BREAKPOINTS"], 
    constants["START_TIME"], 
    constants["END_TIME"], 
    constants["PROFILE_LENGTH"]
)

# Output file name
constants["outputName"] = 'Outputs/results.csv'
