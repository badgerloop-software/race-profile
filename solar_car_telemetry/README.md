### Data Pipeline and Model Integration Project

We need to find the optimal racing profile given the real-time performance of the car. A vital part to our system, then, is to build a data pipeline from Engineering Dashboard, where all real-time car data are stored, to Simulink Model. 

Spcifically, the system will take the following data measured in our solar car, from our weather API, and initial constants, process it, and prepare it for our Simulink model.

## Project Structure

```
├───Data
├───data_generator
├───elevation-data
├───Outputs
├───Python Code (OLD)
├───resources
│   └───project
│       ├───EEtUlUb-dLAdf0KpMVivaUlztwA
│       ├───EEUS99fOfNmnYjcnepENULz4jxk
│       ├───fjRQtWiSIy7hIlj-Kmk87M7s21k
│       ├───NjSPEMsIuLUyIpr2u1Js5bVPsOs
│       ├───qaw0eS1zuuY1ar9TdPn1GMfrjbQ
│       └───root
├───slprj
│   ├───accel
│   │   └───Car
│   │       └───tmwinternal
│   ├───grt
│   │   └───Car
│   │       └───tmwinternal
│   ├───modeladvisor
│   │   ├───Car
│   │   └───com_2emathworks_2ecgo_2egroup_
│   │       └───Car
│   └───sim
│       └───varcache
│           └───Car
│               └───tmwinternal
├───solar_car_telemetry
│   └───src
│       ├───dataProcess
│       │   ├───testData
│       │   └───__pycache__
│       ├───redisExtract
│       │   └───__pycache__
│       ├───simulinkPlugin
│       │   └───__pycache__
│       ├───toolTesting
│       └───__pycache__
└───TestDataAnalysis
```