import redis
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import ctypes
import time

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, db = 0, decode_responses=True)

# Create figure for plotting
fig, ax = plt.subplots()
xs = []  # Store timestamps
ys = []  # Store Var1 values

def save_variables_pandas(debug = False): 
    """
    Reads Variables from Redis and returns it into a Pandas DataFrame
    """
    try:
        keys = r.keys()
        values = r.mget(keys)

        dataList = []
        valueList = []
        for key in keys:           
            dataList.append(key)
            valueList.append(values[keys.index(key)])
            #print(f"{key}")
            #print(f"{key}, {values[keys.index(key)]}")
        
        df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        df = df.sort_values(by=['telem_variables'])        
        #df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        if debug != False:
            print(df)
        return df
        
    except Exception as e:
        print(e)

def save_variables_dict(debug=False):
    """
    Reads Variables from Redis and returns them as a dictionary
    """
    try:
        keys = r.keys()
        values = r.mget(keys)
        result_dict = {}
        for key in keys:
            result_dict[key] = values[keys.index(key)]
        if debug:
            print(result_dict)
        return result_dict
    except Exception as e:
        print(e)

def get_variable_value(variable_name='Var1'):
    try:
        value = r.get(variable_name)
        return value
    except Exception as e:
        print(f"Error retrieving {variable_name}: {e}")
        return None

def record_data(time_seconds = 2, requested = 'Var1'):
    data = []
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < time_seconds:
        data.append(get_variable_value())
        time.sleep(0.5)
    print(data)

def animate(i, telem_var = 'Var1'):
    try:
        global xs, ys

        # Get Var1 value
        df = save_variables_pandas()
        Var1 = df.loc[df['telem_variables'] == telem_var].values[0][1]
        
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

    except AttributeError as e:
        plt.close('all')

        #Error Box
        ctypes.windll.user32.MessageBoxW(0, "Please turn on Data Generator before plotting live data.", "Data Collection Error", 0)
        ##  Styles(Last Number):
        ##  0 : OK
        ##  1 : OK | Cancel
        ##  2 : Abort | Retry | Ignore
        ##  3 : Yes | No | Cancel
        ##  4 : Yes | No
        ##  5 : Retry | Cancel 
        ##  6 : Cancel | Try Again | Continue

def launch_live_graph():
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

if __name__ == '__main__':
    save_variables_dict(True)