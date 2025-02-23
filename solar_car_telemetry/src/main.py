import numpy as np
# import matlab
# import pandas as pd
# import time
# import ctypes

from redisExtract import extractVars
from dataProcess import dataProcess as dprocess
# from simulinkPlugin import simulinkPlugin as sp
# from dataProcess import constants as const
from solcast import get_weather_data

if __name__ == "__main__":
    input_variables=['Var1', 'dcdc_current', 'regen_brake']
    #Obtaining weather data from the Grand Canyon
    #get_weather_data(36.099763, -112.112485, 5)
    #extractVars.launch_live_graph()

    extracted_variables = extractVars.record_multiple_data(3, input_variables)
    means = dprocess.process_recorded_values(extracted_variables, input_variables)

    print(type(means))
    print(means)

    #arr = np.array([-50, 10, 15, 18, 20, 22, 25, 30, 150])
    #dprocess.remove_outliers(arr)

    # # Example 2D array
    # arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    # print(arr)
    # # axis=1 - means of each row
    # print(np.mean(arr, axis=1))  # Output: [2. 5. 8.]

    print("Finished.")