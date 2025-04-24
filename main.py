# import numpy as np
# import pandas as pd
# import time
# import ctypes
from data_pipeline.simulinkPlugin.config import constants
import matlab.engine
import numpy as np
# import logging

# from data_pipeline.dataExtract import extractVars, NearestKeyDict
# from dataProcess import dataProcess as dprocess
from data_pipeline.simulinkPlugin import plugin
# from dataProcess import constants as const
# from solcast import get_weather_data


if __name__ == "__main__":
#     # logging.basicConfig(
#     # level=logging.INFO,
#     # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     # )
#     # logger = logging.getLogger(__name__)
#     # logger.info("Initializing...")

#     print("--- Debugging Constants ---")
#     keys_to_check = [
#         "MAX_CURRENTS_ECO",
#         "MAX_CURRENTS_POWER",
#         "SOLAR_TIME_BREAKPOINTS",
#         "REGEN_ON"  # Add REGEN_ON to debug output
#     ]
    
#     # Add type checking/conversion before simulation
#     if "REGEN_ON" in constants:
#         # Convert to MATLAB logical type if it's not already
#         if not isinstance(constants["REGEN_ON"], matlab.logical):
#             constants["REGEN_ON"] = matlab.logical([bool(constants["REGEN_ON"])])
#     else:
#         # Set default value if not present
#         constants["REGEN_ON"] = matlab.logical([False])

#     # Existing debugging code
#     for key in keys_to_check:
#         if key in constants:
#             value = constants[key]
#             print(f"Key: {key}")
#             print(f"  Type: {type(value)}")
#             if isinstance(value, (list, np.ndarray, matlab.double)):
#                 if isinstance(value, matlab.double):
#                     print(f"  Value: {value}")
#                 else:
#                     print(f"  Length/Shape: {len(value) if isinstance(value, list) else value.shape}")
#                     print(f"  Sample Value: {value[:5] if isinstance(value, list) else value[:5,:]}")
#             else:
#                 print(f"  Value: {value}")
#         else:
#             print(f"Key: {key} - NOT FOUND in constants")
#     print("--- End Debugging ---")
    
    plugin.load_constants()
    plugin.retreive_constants()
#     plugin.run_simulation()

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