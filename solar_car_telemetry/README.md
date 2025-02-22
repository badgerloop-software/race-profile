### Data Pipeline and Model Integration Project

We need to find the optimal racing profile given the real-time performance of the car. A vital part to our system, then, is to build a data pipeline from Engineering Dashboard, where all real-time car data are stored, to Simulink Model. 

Spcifically, the system will take the following data measured in our solar car, from our weather API, and initial constants, process it, and prepare it for our Simulink model.

## Project Structure

```
|   EDashboard Start Instructions.txt
|   README.md
|
\---src
    |   config.py
    |   main.py
    |   sim_the_new_model.m
    |
    +---dataProcess
    |   |   constants.py
    |   |   dataProcess.py
    |   |   data_loader.py
    |   |   __init__.py
    |   |
    |   +---testData
    |   |       battery_const.csv
    |   |       drag_const.csv
    |   |       parameter_list.csv
    |   |       raw_data.csv
    |   |       sliced_data.csv
    |   |       speeds.csv
    |   |
    |   \---__pycache__
    |           constants.cpython-312.pyc
    |           dataProcess.cpython-312.pyc
    |           __init__.cpython-312.pyc
    |
    +---redisExtract
    |   |   extractVars.py
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           extractVars.cpython-312.pyc
    |           __init__.cpython-312.pyc
    |
    +---simulinkPlugin
    |   |   simulinkPlugin.py
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           simulinkPlugin.cpython-312.pyc
    |           __init__.cpython-312.pyc
    |
    +---solcast
    |   |   .env
    |   |   .gitignore
    |   |   api.py
    |   |   ASC2022_A.csv
    |   |   ASC2022_FullRoute.txt
    |   |   Makefile
    |   |   output.csv
    |   |   output_old.csv
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           api.cpython-312.pyc
    |           __init__.cpython-312.pyc
    |
    +---toolTesting
    |       dataslicer.py
    |       redisTest.py
    |       variable_gen.py
    |
    \---__pycache__
            config.cpython-312.pyc
```