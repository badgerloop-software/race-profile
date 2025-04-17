import math
from datetime import datetime

config = {
    # Data Sources
    "COURSE_DATA_FILE": "course_data/ASC_2024/ASC_2024_A.csv",
    "ECO_DATA_FILE": "Data/MotorDataEco.csv",
    "POWER_DATA_FILE": "Data/MotorDataEco.csv",  # Replace later

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

# Adding derived constants - using references to existing keys

config.update({
    "CURRENT_TIME": round(datetime.now().second + datetime.now().microsecond / 1_000_000, 4) # Placeholder for current race time
})

# Add constants that depend on previous ones
config.update({
    "START_TIME": config["CURRENT_TIME"],
    "END_TIME": config["CURRENT_TIME"] + config["PROFILE_LENGTH"],
    
    "HV_PACK_VOLTAGE": 96,  # Volts TEMPORARY until voltage curve is derived
    "HV_PACK_CAPACITY": 80,  # Amp-hours % 57 % Amp-hours
    "WHEEL_DIAMETER_METERS": 22 * config["INCH_TO_METER"],  # Meters
    "FINAL_KWH": 0,  # KwH, battery level for variable time run to end
    "CAR_MASS": 447.90 * config["LBF_TO_KG"],  # data from CarWeightCalc.xlsx
    "DRIVER_MASS": 176 * config["LBF_TO_KG"],
    "AIR_DENSITY": 1.2,  # kg m^-3
    "FRONTAL_AREA": 1,
    "DRAG_COEFFICIENT": 0.25,
    "C_ROLLING_RESISTANCE": 0.0025,
    "GRAVITY": 9.81,  # gravitational acceleration m s^-2
})

# Add speed to RPM conversion constant (depends on wheel diameter)
config.update({
    "SPEED_TO_RPM": 60 / (config["WHEEL_DIAMETER_METERS"] * math.pi),
})

# Controls
config.update({
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
config.update({
    "MAX_SOC": 0.99,
    "MIN_SOC": 0.05,
})

# Wether Data
# TEMP = 

# Dependent Constants
config.update({
    "WHEEL_CIRCUMFRENCE": config["WHEEL_DIAMETER_METERS"] * math.pi,  # Meters
    "WHEEL_RADIUS": config["WHEEL_DIAMETER_METERS"] / 2,
    "FULL_PACK_KWH": config["HV_PACK_VOLTAGE"] * config["HV_PACK_CAPACITY"] * config["UNIT_TO_KILO"],  # kWh
})

# More dependent constants
config.update({
    "STARTING_KWH": config["FULL_PACK_KWH"] * (1 - 0),  # 100% State of Charge
    "TOTAL_MASS": config["CAR_MASS"] + config["DRIVER_MASS"],
})

# Low Voltage
config.update({
    "FAN_DRAW": 4.8,  # Watts
    "DRIVER_DISPLAY_DRAW": 2.5,  # Watts
    "HEADLIGHT_DRAW": 2,  # Watts
    "REGEN_ON": 0,
})

# Tire Data
config.update({
    "SPEED_DATA_TIRE": [50, 80, 100],  # km/h
    "ROLLING_RESISTANCE": [2.30/1000, 2.68/1000, 3.02/1000],  # unitless
    "PRESSURE": 500 / config["UNIT_TO_KILO"],  # Pa
})

# Solar Data - using lambda for dynamic calculation
# config.update({
#     "SOLAR_TIME_BREAKPOINTS": list(range(config["START_TIME"], config["END_TIME"] + 1, 900)),
# })

# Function to calculate the forecasted irradiance
# def calculate_forecasted_irradiance(time_points, start_time, end_time, profile_length):
#     return [-5*((t-start_time)*(t-end_time) / (profile_length/2)**2) for t in time_points]

# config["FORECASTED_IRRADIANCE"] = calculate_forecasted_irradiance(
#     config["SOLAR_TIME_BREAKPOINTS"], 
#     config["START_TIME"], 
#     config["END_TIME"], 
#     config["PROFILE_LENGTH"]
# )

# Output file name
config["outputName"] = 'Outputs/results.csv'
