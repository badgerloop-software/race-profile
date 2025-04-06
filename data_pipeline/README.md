### Data Pipeline and Model Integration Project

We need to find the optimal racing profile given the real-time performance of the car. A vital part to our system, then, is to build a data pipeline from Engineering Dashboard, where all real-time car data are stored, to Simulink Model. 

Specifically, the system will take the following data measured in our solar car, from our weather API, and initial constants, process it, prepare it, and send it to the Simulink model.

## Project Structure

```
data_pipeline/
│
├── EDashboard Start Instructions.txt
├── README.md
│
└── src/
    ├── config.py
    ├── main.py
    ├── sim_the_new_model.m
    │
    ├── dataProcess/
    │   ├── constants.py
    │   ├── dataProcess.py
    │   ├── data_loader.py
    │   ├── __init__.py
    │   │
    │   └── testData/
    │       ├── battery_const.csv
    │       ├── drag_const.csv
    │       ├── parameter_list.csv
    │       ├── raw_data.csv
    │       ├── sliced_data.csv
    │       └── speeds.csv
    │
    ├── redisExtract/
    │   ├── extractVars.py
    │   └── __init__.py
    │
    ├── simulinkPlugin/
    │   ├── simulinkPlugin.py
    │   └── __init__.py
    │
    ├── solcast/
    │   ├── .env
    │   ├── .gitignore
    │   ├── api.py
    │   ├── ASC2022_A.csv
    │   ├── ASC2022_FullRoute.txt
    │   ├── Makefile
    │   ├── output.csv
    │   ├── output_old.csv
    │   └── __init__.py
    │
    └── toolTesting/
        ├── dataslicer.py
        ├── redisTest.py
        └── variable_gen.py
```


## Project Files Details

### Top-level Files
- **main.py**: Main entry point for the application that orchestrates the data pipeline workflow

### dataProcess
This package handles the processing and transformation of raw data:
- **constants.py**: Defines physical and mathematical constants used in data processing
- **dataProcess.py**: Contains functions to transform, clean, and prepare data for the simulation model
- **data_loader.py**: Utilities to load data from various file formats and sources
- **testData/**: Directory containing CSV files with test data and constants for development and testing:
  - Battery constants, drag coefficients, parameter lists, and sample speed profiles

### dataExtract
This package interfaces with the Engineering Dashboard's Redis database:
- **extractVars.py**: Functions to extract real-time telemetry data from Redis and convert it to formats usable by the data processing pipeline

### sampleMatlab
This folder serves as an initial testing ground for the MathWorks library compiler capabilities. The final integration will take place in **simuLinkPlugin**:
- Contains sample code and configuration for interfacing between Python and MATLAB/Simulink
- Provides proof-of-concept implementations demonstrating how to call compiled MATLAB functions from Python
- Tests bidirectional data transfer between the Python pipeline and MATLAB/Simulink models
- Helps resolve integration issues before implementing the full solution in the simulinkPlugin package

### simulinkPlugin
This package will provide integration with MATLAB/Simulink:
- **simulinkPlugin.py**: Will contain functionality to prepare and export processed data to Simulink and retrieve simulation results

### solcast
This package interfaces with solar forecast APIs to obtain weather and solar irradiance predictions:
- **api.py**: Implements the interface with external solar forecasting services
- **ASC2022_A.csv** and **ASC2022_FullRoute.txt**: Route data for the American Solar Challenge 2022
- **.env**: Contains API keys and configuration for the solar forecast service
- **output.csv**: Processed solar forecast data ready for the simulation

### toolTesting
This folder contains miscellaneous functions that were written before and not being actively used.