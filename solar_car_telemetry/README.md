# Telemetry to Simulation Integration

This project will enable us to fetch telemetry data from our solar race car and prepare it for use in our Simulink simulation model (Car.slx).

## Project Structure

```
├── README.md
└── src
    ├── config
    │   └── settings.py
    ├── dataProcess
    │   ├── constants.py
    │   ├── data_loader.py
    │   ├── dataProcess.py
    │   ├── __init__.py
    │   └── testData
    │       ├── battery_const.csv
    │       ├── drag_const.csv
    │       ├── parameter_list.csv
    │       ├── raw_data.csv
    │       ├── sliced_data.csv
    │       └── speeds.csv
    ├── main.py
    ├── redisExtract
    │   ├── config.py
    │   ├── extractVars.py
    │   ├── __init__.py
    │   └── __pycache__
    │       ├── config.cpython-312.pyc
    │       ├── extractVars.cpython-312.pyc
    │       └── __init__.cpython-312.pyc
    ├── simulinkPlugin
    │   ├── __init__.py
    │   └── simulinkPlugin.py
    └── toolTesting
        ├── dataslicer.py
        ├── redisTest.py
        └── variable_gen.py
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
   - [x] Determine actual Redis server details
   - [x] Verify parameter names and units
   - [x] Test network connectivity
   - [ ] Validate data format

2. **Short Term**
   - [ ] Complete configuration setup
   - [ ] Implement basic error handling
   - [x] Create test dataset
   - [ ] Verify Simulink integration

3. **Long Term**
   - [ ] Develop monitoring system
   - [ ] Create comprehensive tests
   - [ ] Build data validation pipeline
   - [ ] Implement advanced features
