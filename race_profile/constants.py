import numpy as np

# Non-Configurable Constants
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
INCH_TO_METER = 0.0254
UNIT_TO_KILO = 1 / 1000
LONG_TIME = 10000 # Seconds, big number to limit variable time runs

# Configurable Constants
TIME_RES = 10 # Seconds
PROFILE_LENGTH = 4000 # Seconds
HV_PACK_VOLTAGE = 96 # Volts
HV_PACK_CAPACITY = 80 #57 # Amp-hours
WHEEL_DIAMETER_METERS = 16.75 * INCH_TO_METER # Meters
FINAL_KWH = 0 # KwH, battery level for variable time run to end
FIXED_TIME_RUN = False # runs to PROFILE_LENGTH if true, FINAL_PACK_ENERGY if false

# Dependant Constants
WHEEL_CIRCUMFRENCE = WHEEL_DIAMETER_METERS * np.pi # Meters
FULL_PACK_KWH = HV_PACK_VOLTAGE * HV_PACK_CAPACITY * UNIT_TO_KILO # kWh
STARTING_KWH = FULL_PACK_KWH # 100% State of Charge


