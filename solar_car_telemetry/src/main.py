import numpy as np
import datetime
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

    # extracted_variables = extractVars.record_multiple_data(3, input_variables)
    # means = dprocess.process_recorded_values(extracted_variables, input_variables)

    # print(type(means))
    # print(means)

    today = datetime.date.today().isoformat()
    print(today)

    print("Finished.")