# import numpy as np
# import pandas as pd
# import time
# import ctypes
from data_pipeline.simulinkPlugin.config import constants
import matlab.engine
# import logging

# from data_pipeline.dataExtract import extractVars, NearestKeyDict
# from dataProcess import dataProcess as dprocess
from data_pipeline.simulinkPlugin import plugin
# from dataProcess import constants as const
# from solcast import get_weather_data


if __name__ == "__main__":
    # logging.basicConfig(
    # level=logging.INFO,
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # )
    # logger = logging.getLogger(__name__)
    # logger.info("Initializing...")
    
    plugin.load_constants()
    plugin.run_simulation()

    # #Take note of Input variables
    # input_variables=['soc', 'pack_power', 'air_temp']
    # #Open Route data into lookup table
    # route = extractVars.open_route()
    # # print(route)

    # enhanced_route = NearestKeyDict(route)
    # print(enhanced_route[200000][0]) 
    # print(enhanced_route[200000][1])
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

    print("Finished.")