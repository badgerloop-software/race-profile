"""
Read telemetry data from Redis and 
provide access to the data in a structured
format for the simulation.
"""
import redis, config
import numpy as np
#import matlab
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

from redisExtract import extractVars
from dataProcess import dataProcess as dprocess
from simulinkPlugin import simulinkPlugin as sp
from dataProcess import constants as const
from solcast import get_weather_data
    
# Create figure for plotting
fig, ax = plt.subplots()
xs = []  # Store timestamps
ys = []  # Store Var1 values

def animate(i):
    global xs, ys

    # Get Var1 value
    df = extractVars.save_variables()
    Var1 = df.loc[df['telem_variables'] == 'Var1'].values[0][1]
    
    # Add x and y to lists
    xs.append(datetime.now())
    ys.append(Var1)
    
    # Limit lists to 50 items
    xs = xs[-50:]
    ys = ys[-50:]
    
    # Clear axis
    ax.clear()
    
    # Plot data
    ax.plot(xs, ys)
    
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Var1 Over Time')
    plt.ylabel('Var1 Value')


if __name__ == "__main__":
    weather_data = get_weather_data()
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()