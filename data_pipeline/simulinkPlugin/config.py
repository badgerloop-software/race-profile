import math
from datetime import datetime
import numpy as np
import pandas as pd
import matlab.engine

constants = {
    # Data Sources
    "COURSE_DATA_FILE": "course_data/ASC_2024/ASC_2024_A.csv",
    "ECO_DATA_FILE": "Data/MotorDataEco.csv",
    "POWER_DATA_FILE": "Data/MotorDataEco.csv",  # Replace later

    #From config.csv
    # courseDataFile,course_data/ASC_2024/ASC_2024_A.csv'
    # weatherDataFile,
    # ecoDataFile,Data/MotorDataEco.csv'
    # powerDataFile,Data/MotorDataEco.csv'


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

course_data_df = pd.read_csv(constants["COURSE_DATA_FILE"], header=0)

# MATLAB‑style fixes (1‐based → 0‐based indices)
course_data_df.iloc[0, 5] = course_data_df.iloc[1, 5]   # first heading = second
course_data_df.iloc[0, 6] = 0                          # first slope = 0
course_data_df.iloc[0, 8] = 0                          # first interval = 0

# Compute NANS on column 7 (zero‑based idx 6)
nans_bool = course_data_df.iloc[:, 6].isna()

# Compute DUPLICATES on column 8 (zero‑based idx 7)
duplicates_bool = course_data_df.iloc[:, 7].diff().eq(0)

# Push boolean arrays into constants (as MATLAB logicals)
constants.update({
    "NANS":      matlab.logical(nans_bool.tolist()),
    "DUPLICATES": matlab.logical(duplicates_bool.tolist()),
})

# Filter out those rows
mask = ~nans_bool & ~duplicates_bool
filtered_df = course_data_df[mask]

# 1) Push the filter mask itself
constants.update({
    "COURSE_FILTER": matlab.logical(mask.tolist()),
})

# 2) Compute and push INT_DISTANCES & INT_GRADE_ANGLE
int_distances   = (filtered_df.iloc[:, 7] / constants["UNIT_TO_KILO"]).tolist()
int_grade_angle = np.degrees(np.arctan(filtered_df.iloc[:, 6] / 100)).tolist()

constants.update({
    "INT_DISTANCES":   matlab.double(int_distances),
    "INT_GRADE_ANGLE": matlab.double(int_grade_angle),
})

# 3) Finally, overwrite COURSE_DATA with the filtered rows
numeric_data = filtered_df.select_dtypes(include=[np.number]).values.astype(float).tolist()
constants.update({
    "COURSE_DATA": matlab.double(numeric_data),
})

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

# --- Motor Eco Mode data -----------------------------------------------
eco_df = pd.read_csv(constants["ECO_DATA_FILE"], header=0)
constants.update({
    "ECO_DATA": matlab.double(eco_df.values.tolist())
})

current_data_eco   = eco_df.iloc[:, 0].astype(float)
torques_data_eco   = eco_df.iloc[:, 1].astype(float)
rpm_data_eco       = eco_df.iloc[:, 2].astype(float)

rpm_breakpoints_eco = rpm_data_eco.iloc[::-1]
max_currents_eco    = current_data_eco.iloc[::-1]

constants.update({
    "REGEN_ON":               0,
    "CURRENT_DATA_ECO":       current_data_eco.tolist(),
    "TORQUES_DATA_ECO":       torques_data_eco.tolist(),
    "RPM_DATA_ECO":           rpm_data_eco.tolist(),
    "RPM_BREAKPOINTS_ECO":    rpm_breakpoints_eco.tolist(),
    "MAX_CURRENTS_ECO":       max_currents_eco.tolist(),
    "NO_TORQUE_CURRENT_ECO":  float(current_data_eco.iloc[0]),
    "MIN_CURRENT_ECO":        float(current_data_eco.min()),
    "MAX_CURRENT_ECO":        float(current_data_eco.max()),
    "MAX_TORQUE_ECO":         float(torques_data_eco.max()),
    "MAX_RPM_ECO":            float(rpm_data_eco.max()),
})

# --- Motor Power Mode data ---------------------------------------------
power_df = pd.read_csv(constants["POWER_DATA_FILE"], header=0)
constants.update({
    "POWER_DATA": matlab.double(power_df.values.tolist())
})

current_data_power   = power_df.iloc[:, 0].astype(float)
torques_data_power   = (power_df.iloc[:, 1].astype(float) * 2.5)
rpm_data_power       = power_df.iloc[:, 2].astype(float)

rpm_breakpoints_power = rpm_data_power.iloc[::-1]
max_currents_power    = current_data_power.iloc[::-1]

constants.update({
    "CURRENT_DATA_POWER":       current_data_power.tolist(),
    "TORQUES_DATA_POWER":       torques_data_power.tolist(),
    "RPM_DATA_POWER":           rpm_data_power.tolist(),
    "RPM_BREAKPOINTS_POWER":    rpm_breakpoints_power.tolist(),
    "MAX_CURRENTS_POWER":       max_currents_power.tolist(),
    "NO_TORQUE_CURRENT_POWER":  float(current_data_power.iloc[0]),
    "MIN_CURRENT_POWER":        float(current_data_power.min()),
    "MAX_CURRENT_POWER":        float(current_data_power.max()),
    "MAX_TORQUE_POWER":         float(torques_data_power.max()),
    "MAX_RPM_POWER":            float(rpm_data_power.max()),
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
