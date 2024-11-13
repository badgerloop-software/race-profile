# Telemetry to Simulation Integration

This project provides tools to fetch telemetry data from our solar race car and prepare it for use in our Simulink simulation model (Car.slx).

## Project Structure

```
solar_car_telemetry/
│
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py        # Move constants from init.py here
│   │   └── simulation_config.py # Simulation-specific parameters
│   │
│   ├── data_handlers/
│   │   ├── __init__.py
│   │   ├── redis_handler.py    # Your telemetry.py will go here
│   │   └── simulink_prep.py    # Prepare data for Simulink
│   │
│   └── utils/
│       ├── __init__.py
│       └── unit_conversions.py  # Unit conversion functions
│
├── data/
│   ├── raw/                    # Your CSV files
│   │   ├── flat_course.csv
│   │   ├── const_solar.csv
│   │   ├── const_drag.csv
│   │   ├── const_battery.csv
│   │   ├── MotorDataEco.csv
│   │   ├── constTargetSpeed.csv
│   │   └── constDensity.csv
│   │
│   └── processed/              # For processed telemetry data
│
├── simulink/                   # Simulink related files
│   └── Car.slx
│
├── requirements.txt
├── init.py                     # Your existing init file
└── main.py                     # Main script to run everythingdd
```

## Features

- Fetch telemetry data from Redis database
- Convert data into simulation-compatible format
- Create time series objects for Simulink
- Compare telemetry with simulation results
- Calculate error metrics

## Current Assumptions & Requirements

### Database Connectivity
1. **Redis Server Location**
   - Currently assumes Redis runs on localhost
   - Will likely need to be updated with actual server IP on LAN
   - Default port 6379 assumed (standard Redis port)
   - Authentication may be required (currently optional in settings)

2. **Network Requirements**
   - Need to be on same LAN as telemetry server
   - Firewall rules may need to be configured
   - VPN might be needed if accessing from different network
   - Network bandwidth should be sufficient for data volume

### Data Structure Assumptions

1. **Telemetry Parameters**
   - Assumed parameter names (need verification):
     * vehicle_speed
     * motor_power
     * pack_voltage
     * pack_current
     * array_power
     * ambient_temp
   - Units assumed (need verification):
     * Speed in mph
     * Power in Watts
     * Voltage in Volts
     * Current in Amperes
     * Temperature in Celsius

2. **Data Format**
   - Timestamps assumed to be in Unix milliseconds
   - Numeric values assumed to be floats
   - Assumes no missing or null values
   - Assumes continuous time series data

3. **Sampling Rate**
   - Default 1000ms sampling rate assumed
   - May need adjustment based on actual telemetry system
   - Buffer size set to 1000 records by default

### Simulation Integration

1. **Simulink Model (Car.slx)**
   - Assumes specific variable names in model
   - May need mapping configuration for different variable names
   - Assumes time-series input blocks are present
   - Assumes compatible data types

2. **MATLAB Workspace**
   - Assumes MATLAB R2020b or newer
   - Required toolboxes not yet determined
   - Workspace variable naming conventions may need adjustment

## Things to Determine

### Database Configuration
1. **Server Details**
   - [ ] Actual Redis server IP address
   - [ ] Port number if different from default
   - [ ] Authentication credentials if required
   - [ ] Database number if multiple databases exist

2. **Network Setup**
   - [ ] Network architecture diagram
   - [ ] Required firewall configurations
   - [ ] VPN setup if needed
   - [ ] Bandwidth requirements

### Data Requirements
1. **Parameter Verification**
   - [ ] Complete list of available telemetry parameters
   - [ ] Correct units for each parameter
   - [ ] Valid ranges for each parameter
   - [ ] Required sampling rates

2. **Data Quality**
   - [ ] How to handle missing data
   - [ ] Data validation requirements
   - [ ] Error handling procedures
   - [ ] Data backup/recovery process

### Simulation Needs
1. **Model Integration**
   - [ ] Exact Simulink variable names
   - [ ] Required data transformations
   - [ ] Time synchronization requirements
   - [ ] Performance requirements

2. **Analysis Requirements**
   - [ ] Specific metrics needed
   - [ ] Validation criteria
   - [ ] Output format preferences
   - [ ] Visualization requirements

## Usage

1. Configure Redis connection in `src/config/settings.py`:
```python
# Update with actual server details
REDIS_CONFIG = {
    'host': 'actual.server.ip',
    'port': 6379,
    'db': 0,
    'password': 'if_required'
}
```

2. Run Python script to fetch and convert telemetry data:
```python
from src.telemetry.simulation_converter import SimulationConverter

# Create converter
converter = SimulationConverter()

# Convert telemetry data
converter.save_simulation_data(telemetry_data)
```

3. Use the data in MATLAB/Simulink:
```matlab
% Load telemetry data
data = load('telemetry_sim_data.mat');

% Create time series for Simulink
speed_ts = timeseries(data.speed, data.sim_time);

% Run simulation and compare results
simulation_example
```

## Parameter Mapping

Current assumed mapping between telemetry and simulation:

| Telemetry Parameter | Simulation Variable | Unit | Notes |
|-------------------|-------------------|------|-------|
| vehicle_speed | speed | mph | May need conversion |
| motor_power | motor_power | W | Direct mapping |
| pack_voltage | battery_voltage | V | Direct mapping |
| pack_current | battery_current | A | Direct mapping |
| array_power | solar_power | W | Direct mapping |
| ambient_temp | ambient_temperature | °C | Direct mapping |

## Future Development Needs

1. **Configuration Management**
   - System for managing different server configurations
   - Environment-specific settings
   - Configuration validation

2. **Error Handling**
   - Network connectivity issues
   - Data validation failures
   - Simulation integration errors
   - Recovery procedures

3. **Data Processing**
   - Data filtering options
   - Interpolation methods
   - Unit conversion utilities
   - Custom aggregation functions

4. **Testing**
   - Unit tests for each component
   - Integration tests
   - Network connectivity tests
   - Data validation tests

5. **Documentation**
   - API documentation
   - Network setup guide
   - Troubleshooting guide
   - Example configurations

6. **Monitoring**
   - Connection status monitoring
   - Data quality metrics
   - Performance monitoring
   - Error logging

## Contributing

1. Update parameter definitions in settings.py as needed
2. Add new conversion methods in simulation_converter.py
3. Create example scripts demonstrating usage
4. Update documentation

## Support

Contact the simulation team for questions or issues.

## Next Steps

1. **Immediate Actions**
   - [ ] Determine actual Redis server details
   - [ ] Verify parameter names and units
   - [ ] Test network connectivity
   - [ ] Validate data format

2. **Short Term**
   - [ ] Complete configuration setup
   - [ ] Implement basic error handling
   - [ ] Create test dataset
   - [ ] Verify Simulink integration

3. **Long Term**
   - [ ] Develop monitoring system
   - [ ] Create comprehensive tests
   - [ ] Build data validation pipeline
   - [ ] Implement advanced features
