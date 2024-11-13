# Telemetry to MATLAB Integration Guide

## Introduction

Hey team! This guide will walk you through how to get telemetry data from our solar race car into MATLAB for analysis. 

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
└── main.py                     # Main script to run everythingd
```

## Getting Started

1. Clone the repository and install dependencies:
```bash
git clone [repository-url]
cd telemetry_matlab_integration
pip install -r requirements.txt
```

2. Copy the configuration template and update with your settings:
```bash
cp src/config/settings.py.template src/config/settings.py
# Edit settings.py with your Redis credentials
```

3. Run the example script:
```bash
python examples/basic_usage.py
```

4. Open MATLAB and run the analysis template:
```matlab
cd examples
analysis_example
```

## Contributing

1. Create a new branch for your feature
2. Implement your changes
3. Add tests in the tests/ directory
4. Update documentation if needed
5. Submit a pull request

## Support

- Check the #telemetry-support Slack channel
- Review the example scripts
- Contact the telemetry team lead

Happy analyzing! 🚗☀️
