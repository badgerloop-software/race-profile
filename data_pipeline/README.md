### Data Pipeline and Model Integration Project

We need to find the optimal racing profile given the real-time performance of the car. A vital part to our system, then, is to build a data pipeline from Engineering Dashboard, where all real-time car data are stored, to Simulink Model. 

Specifically, the system will take the following data measured in our solar car, from our weather API, route data, and initial constants, process it, prepare it, and send it to the Simulink model.

## Project Files Details

### Top-level Files
- **race-profile/main.py**: Main entry point for the application. It should orchestrate the data pipeline workflow, start the simulation, and run the optimization scripts.

### sampleMatlab and car2_package folders are part of my testing of the Python-Simulink integration. They should be ignored at the moment.

### dataProcess
This package handles the processing and transformation of raw data:
- **dataProcess.py**: Remove outliers across all the variables requested using the Interquartile Range (IQR) Method (Currently in `remove_outliers()`).

Next, compute a mean average of these variables (Currently in `process_recorded_values()`).

- **constants.py** and **data_loader.py**: These files are a legacy from the setup.m file, and may be used when starting the sumulation. This is to be determined as we are working on integration with Simulink.

- **testData/**: Directory containing CSV files with test data and constants for development and testing:
  - Battery constants, drag coefficients, parameter lists, and sample speed profiles

### dataExtract

There are two things that dataExtract handles. One is the live data in Redis database, and the other is the route data.
- **extractVars.py**: 
Redis Data Extraction (Currently in `record_multiple_data()`):

While one round of the simulation is recording, we are saving the value of each variable for a given unit of time that we can set(like every 0.5 seconds). The result is a numpy array for each variable quereyed holding values collected across the time that the simulation ran.

The Redis python documentation needs to be looked into more as there is a way to just query the variables using Unix timestamps.
The format the data is stored in Redis when engineering dashboard is run is slightly different, and this needs to be handled properly.

Competition Route Data (Currently in `open_route()`):

We open the route data from the file `ASC2022_A.csv` in the `solcast` folder and produce a dictionary with distance travelled as the key, and a tuple of (latitude, longitude) as the value.

- **NearestKeyDict.py**: This is a custom dictionary class that allows us to lookup values that do not exactly match a key in the dictionary. Instead, when you attempt to look up a value that does not match a key, this input value will be matched to the key that is numerically closest to it, and return the approximate lattitude and longitude along the route.

This is crucial as we are expectting the simulation to almost always give intermediate values for simulated distance travelled.

### simulinkPlugin
This package will provide integration with MATLAB/Simulink:
- **simulinkPlugin.py**: Will contain functionality to prepare and export processed data to Simulink and retrieve simulation results.

We are using MathWork's example [here](https://github.com/mathworks/Call-Simulink-from-Python) for integration.

### solcast
This package interfaces with solar forecast APIs to obtain weather and solar irradiance predictions:
- **api.py**: Implements the interface with external solar forecasting services
- **ASC2022_A.csv** and **ASC2022_FullRoute.txt**: Route data for the American Solar Challenge 2022
- **.env**: Contains API keys and configuration for the solar forecast service
- **output.csv**: Processed solar forecast data ready for the simulation

### toolTesting
This folder contains miscellaneous functions that were written before and not being actively used.

## Project Structure
```
│   EDashboard Start Instructions.txt
│   README.md
│
├───car2_package
│   │   GettingStarted.html
│   │   includedSupportPackages.txt
│   │   mccExcludedFiles.log
│   │   pyproject.toml
│   │   readme.txt
│   │   requiredMCRProducts.txt
│   │   setup.py
│   │   unresolvedSymbols.txt
│   │
│   ├───car_sim
│   │       car_sim.ctf
│   │       __init__.py
│   │
│   ├───car_sim_R2024b.egg-info
│   │       dependency_links.txt
│   │       PKG-INFO
│   │       SOURCES.txt
│   │       top_level.txt
│   │
│   └───Lib
│       └───site-packages
│           ├───car_sim
│           │   │   car_sim.ctf
│           │   │   __init__.py
│           │   │
│           │   └───__pycache__
│           │           __init__.cpython-312.pyc
│           │
│           └───car_sim_R2024b-24.2-py3.12.egg-info
│                   dependency_links.txt
│                   PKG-INFO
│                   SOURCES.txt
│                   top_level.txt
│
├───dataExtract
│   │   extractVars.py
│   │   NearestKeyDict.py
│   │   __init__.py
│   │
│   └───__pycache__
│           extractVars.cpython-312.pyc
│           NearestKeyDict.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───dataProcess
│   │   constants.py
│   │   dataProcess.py
│   │   data_loader.py
│   │   __init__.py
│   │
│   ├───testData
│   │       battery_const.csv
│   │       drag_const.csv
│   │       parameter_list.csv
│   │       raw_data.csv
│   │       sliced_data.csv
│   │       speeds.csv
│   │
│   └───__pycache__
│           dataProcess.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───sampleMatlab
│   │   add.m
│   │   add.prj
│   │   adder.m
│   │   mainSample.py
│   │
│   └───add
│       │   PackagingLog.html
│       │
│       ├───for_redistribution
│       │       MyAppInstaller_web.exe
│       │
│       ├───for_redistribution_files_only
│       │   │   adder.py
│       │   │   GettingStarted.html
│       │   │   setup.py
│       │   │
│       │   ├───add
│       │   │       add.ctf
│       │   │       __init__.py
│       │   │
│       │   └───samples
│       │           adder.py
│       │
│       └───for_testing
│           │   includedSupportPackages.txt
│           │   pyproject.toml
│           │   readme.txt
│           │   requiredMCRProducts.txt
│           │   setup.py
│           │   unresolvedSymbols.txt
│           │
│           └───add
│                   add.ctf
│                   __init__.py
│
├───simulinkPlugin
│   │   Car.slx
│   │   Car.slx.r2023b
│   │   Car.slx.r2024a
│   │   Car.slxc
│   │   car_simulation.m
│   │   packagemaker.m
│   │   plugin.py
│   │   setuptest.m
│   │   __init__.py
│   │
│   └───__pycache__
│           plugin.cpython-312.pyc
│           __init__.cpython-312.pyc
│
├───solcast
│   │   .gitignore
│   │   api.py
│   │   api_request_log.csv
│   │   ASC2022_A.csv
│   │   ASC2022_FullRoute.txt
│   │   Makefile
│   │   output.csv
│   │   output_old.csv
│   │   __init__.py
│   │
│   └───__pycache__
│           api.cpython-312.pyc
│           __init__.cpython-312.pyc
│
└───toolTesting
        csvconverter.py
        dataslicer.py
        record.txt
        redisTest.py
        variable_gen.py
        __init__.py 
```