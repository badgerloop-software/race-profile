import redis, config
import numpy as np
#import matlab
import pandas as pd
import time
import ctypes

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

from redisExtract import extractVars
from dataProcess import dataProcess as dprocess
from simulinkPlugin import simulinkPlugin as sp
from dataProcess import constants as const
from solcast import get_weather_data

if __name__ == "__main__":
    #Obtaining weather data from the Grand Canyon
    get_weather_data(36.099763, -112.112485, 5)

    #extractVars.launch_live_graph()

    print("Finished.")