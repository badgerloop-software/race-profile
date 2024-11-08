import time
from scipy.io import savemat
import asyncio

# Vehicle Dynamics
DYNAMICS_PARAMS = [
    'speed',              # mph
    'accelerator_pedal',  # %
    'foot_brake',        # boolean
    'regen_brake',       # %
]

# Power System
POWER_PARAMS = [
    'pack_voltage',      # V
    'pack_current',      # A
    'pack_power',        # W
    'motor_power',       # W
    'motor_current',     # A
]

# Thermal Management
THERMAL_PARAMS = [
    'pack_temp',         # degC
    'motor_temp',        # degC
    'air_temp',         # degC
]

# Solar Array
SOLAR_PARAMS = [
    'string1_V_in',      # V
    'string1_I_in',      # A
    'string1_temp',      # degC
    # ... other strings
]


async def fetch_telemetry_dataset(param_list, start_time, end_time):
    """
    Fetches a set of parameters for a given time window

    Args:
        param_list: List of parameter names from the database
        start_time: Unix timestamp in milliseconds
        end_time: Unix timestamp in milliseconds or '+' for current time
    """
    # All parameters use 'AVG' aggregation for now
    agg_methods = ['AVG'] * len(param_list)

    try:
        df = await query(param_list, start_time, end_time, agg_methods)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


async def collect_simulation_data(time_window_minutes=60):
    """
    Collects all necessary data for simulation
    """
    # Calculate time window
    end_time = '+'  # current time
    start_time = round((time.time() - (time_window_minutes * 60)) * 1000)

    # Collect all parameter groups
    datasets = {}
    for name, params in [
        ('dynamics', DYNAMICS_PARAMS),
        ('power', POWER_PARAMS),
        ('thermal', THERMAL_PARAMS),
        ('solar', SOLAR_PARAMS)
    ]:
        df = await fetch_telemetry_dataset(params, start_time, end_time)
        if df is not None:
            datasets[name] = df

    # Save to MATLAB format
    matlab_dict = {}
    for category, df in datasets.items():
        for column in df.columns:
            # Create valid MATLAB variable names
            matlab_name = f"{category}_{column}"
            matlab_dict[matlab_name] = df[column].values

        # Add timestamp
        matlab_dict[f"{category}_time"] = df.index.values

    savemat('simulation_data.mat', matlab_dict)