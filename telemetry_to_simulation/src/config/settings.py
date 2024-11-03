from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None

@dataclass
class TelemetryConfig:
    redis: RedisConfig
    sampling_rate: int = 1000  # ms
    batch_size: int = 1000     # records
    timeout: int = 30          # seconds

# Parameter definitions with units and valid ranges
# These parameters are specific to the solar car simulation
TELEMETRY_PARAMETERS: Dict[str, Dict] = {
    # Vehicle Dynamics
    'vehicle_speed': {
        'unit': 'mph',
        'min_value': 0,
        'max_value': 100,
        'aggregation': 'AVG',
        'simulink_variable': 'speed'  # Corresponding variable in Car.slx
    },
    'motor_power': {
        'unit': 'W',
        'min_value': -5000,  # Negative for regen
        'max_value': 5000,
        'aggregation': 'AVG',
        'simulink_variable': 'motor_power'
    },
    
    # Battery System
    'pack_voltage': {
        'unit': 'V',
        'min_value': 0,
        'max_value': 150,
        'aggregation': 'AVG',
        'simulink_variable': 'battery_voltage'
    },
    'pack_current': {
        'unit': 'A',
        'min_value': -50,  # Negative for charging
        'max_value': 50,
        'aggregation': 'AVG',
        'simulink_variable': 'battery_current'
    },
    
    # Solar Array
    'array_power': {
        'unit': 'W',
        'min_value': 0,
        'max_value': 1000,
        'aggregation': 'AVG',
        'simulink_variable': 'solar_power'
    },
    
    # Environmental
    'ambient_temp': {
        'unit': 'C',
        'min_value': -10,
        'max_value': 50,
        'aggregation': 'AVG',
        'simulink_variable': 'ambient_temperature'
    }
}
