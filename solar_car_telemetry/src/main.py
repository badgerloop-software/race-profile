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
from simulinkPlugin import simulinkPlugin as sp

def main():
    """
    Handle telemetry data pipeline between Redis database and Simulink model.
    """

    #Initialize list of desired parameters to request
    desired_params = ['speed', 'pack_voltage', 'headlights_led_en', 'motor_current', 'fan_speed', 'air_temp', 'pack_power', 'soc']
    
    extractVars.print_variables()
    #extractVars.redis_get_variables()

    data = pd.DataFrame()

    #Specify the range of time to extract data from here
    data = extractVars.request_data(desired_params, 0, '+')

    # Find averages for each of the desired parameters
    averages = dprocess.findAverageValues(data)

    # Initialize and run Simulink simulation
    sp.__init__()
    results = sp.send_to_simulation(averages)
    
    print("Simulation Results: ")
    print(results)
    
    sp.close()




if __name__ == "__main__":
    main()