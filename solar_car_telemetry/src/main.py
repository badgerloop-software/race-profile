"""
Read telemetry data from Redis and 
provide access to the data in a structured
format for the simulation.
"""
import redis, config
import numpy as np
import matlab
import pandas as pd

from redisExtract import extractVars
from dataProcess import dataProcess as dprocess

def main():
    """
    Handle telemetry data pipeline between Redis database and Simulink model.
    """

    #Initialize list of desired parameters to request
    desired_params = ['speed', 'pack_voltage', 'headlights_led_en', 'motor_current', 'fan_speed', 'air_temp', 'pack_power', 'soc']
    
    extractVars.print_variables()
    #extractVars.redis_get_variables()

    data = pd.DataFrame()
    data = extractVars.request_data(desired_params, 0, '+')

    averages = dprocess.findAverageValues(data)

    print(averages)



if __name__ == "__main__":
    main()