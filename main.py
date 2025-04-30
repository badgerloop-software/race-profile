# import numpy as np
# import pandas as pd
import time
# import ctypes
from data_pipeline.simulinkPlugin.config import constants
import matlab.engine
import numpy as np
# import matplotlib.pyplot as plt
# import logging

from data_pipeline.dataExtract import extractVars, NearestKeyDict
from data_pipeline.dataProcess import dataProcess
from data_pipeline.simulinkPlugin import plugin
# from dataProcess import constants as const
# from solcast import get_weather_data


if __name__ == "__main__":
    start_time = time.time()

    #Make changes to input parameters here before loading.

    # #Take note of Input variables
    # input_variables=['soc', 'pack_power', 'air_temp']

    power_extracted = extractVars.get_variable_value('pack_power')

    # power_extracted = extractVars.record_multiple_data(2, 0.5, ['pack_power'])
    # power_extracted = dataProcess.remove_outliers(power_extraxted)
    # power_extracted = dataProcess.process_recorded_values(power_extraxted)

    constants.update({
        "initialguess": power_extracted
    })

    constants.update({
        "initialguess": 500
    })

    #Open Route data into lookup table
    route = extractVars.open_route()

    # print(route[200000][0]) 
    # print(route[200000][1])

    plugin.start_matlab_engine()

    plugin.load_constants()

    plugin.retreive_constants()

    # Run simulation --- Available Logged Signals (Index: Name) ---
    # 1: power[kW]
    # 2: [A]
    # 3: [V]
    # 4: Motor Current Draw [A]
    # 5: Net Power
    # 6: Pow1
    # 7: pow2
    # 8: S.O.C
    # 9: [Unnamed Signal 9]
    # 10: [W]
    # 11: Control Signal [A]
    # 12: PowerMode
    # 13: [Unnamed Signal 13]
    # 14: [Unnamed Signal 14]
    # 15: [Unnamed Signal 15]
    # 16: controlPowerSignal
    # 17: powerError
    # 18: ControlSpeedSignal
    # 19: SpeedError
    # 20: Air Density [kg/m^3]
    # 21: Irradiance [W/m^2]
    # 22: Surface Grade
    # 23: Net Force [N]
    # 24: brakeForce
    # 25: Normal Force [N]
    # 26: Parallel Gravitational Force [N]
    # 27: Motor Propulsion Force [N]
    # 28: maxCurrent
    # 29: Resistive Forces [N]
    # 30: Drag Force [N]
    # 31: Rolling Resistance [N]
    # 32: Solar Power [W]
    # 33: Acceleration [m/s^2]
    # 34: Position [m]
    # 35: Velocity [m/s]
    # ---------------------------------------------
    # plugin.run_simulation([35, 30, 8])
    
    plugin.run_optimization()

    #Close Workspace
    plugin.close_workspace()


    # #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # #Run the sumulation and time how long it takes.
    # # Create simulator instance
    # simulator = CarSimulator()

    # # Then use it where needed
    # results = simulator.run_simulation(target_speed=20, target_power=500)

    #With the total time the first simuation took, query the corresponsing data from redis and do data process to remove outliers and copmute means.

    #Feed new values into simulation and run again.

    #Repeat.

    #Every 30 minutes, when the car it leaves certain radius distance, all of the weather data queryed from the API is irrelavant. 
    #So we pull the predicted distance travelled, and look up the approximate position in the lookup table, and feed that position into the API function and feed the resulting irridance data into the simulation.
    #SOC, Pack_power, ghi, cloud_opacity.
    #When we look up weather data, our total irridance will be the Global Horizontal Irridance (ghi) multiplied by the Cloud Opacity(cloud_opacity).
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    
    #Obtaining weather data from the Grand Canyon
    #get_weather_data(36.099763, -112.112485, 5)
    #extractVars.launch_live_graph()

    # extracted_variables = extractVars.record_multiple_data(3, input_variables)
    # means = dprocess.process_recorded_values(extracted_variables, input_variables)

    # print(type(means))
    # print(means)

    # df = pd.read_csv("solar_car_telemetry/src/solcast/output.csv")
    # print(df)

    end_time = time.time()
    print(f"Finished in {end_time-start_time:.2f} seconds.")