import redis
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import requests
import time
import numpy as np
from .NearestKeyDict import NearestKeyDict
import tkinter as tk
from tkinter import messagebox

r = redis.StrictRedis(host = 'localhost', port = 6379, db = 0, decode_responses=True)

# Create figure for plotting
fig, ax = plt.subplots()
xs = []  # Store timestamps
ys = []  # Store Var1 values

def get_variable_value(variable_name='Var1'):
    try:
        value = r.get(variable_name)
        return value
    except Exception as e:
        print(f"Error retrieving {variable_name}: {e}")
        return None
    
#We should ideally be using the API from the dashboard to get the data instead of going directly through Redis
def edashboard_extract():
    url = 'http://localhost:3000/single-values'
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Response: {response.text}")
        response.raise_for_status()

        data = response.json()

        result = {
            'timestamp': data['response']['timestamp'],
            'data_format': data['response']['Dataformat']
        }
        
        return result
        
    except requests.RequestException as e:
        print(f"Error fetching dashboard data: {e}")
        if hasattr(e, 'response'):
            print(f"Response content: {e.response.text}")
        return None
    except KeyError as e:
        print(f"Error parsing response data: {e}")
        return None

def record_data(time_seconds = 2, requested = 'Var1'):
    global features 
    features = np.array([])

    start_time = time.perf_counter()
    print(f"Recording for {time_seconds} seconds...")
    while time.perf_counter() - start_time < time_seconds:
        features = np.append(features, float(get_variable_value()))
        time.sleep(0.5)
    print(features)
    return features

def record_multiple_data(time_seconds=2, sampling_frequency = 0.5, variables=['soc', 'pack_power', 'air_temp']):
    """
    Records multiple variables from Redis over a specified time period using numpy arrays
    Args:
        time_seconds (int): Duration to record data
        sampling_frequency (int): save the value of each variable every ___ seconds
        variables (list): List of variable names to record
    Returns:
        dict: Dictionary with variable names as keys and numpy arrays of values as values
    """
    data = {var: np.array([]) for var in variables}
    
    start_time = time.perf_counter()
    print(f"Recording {len(variables)} variables for {time_seconds} seconds...")
    while time.perf_counter() - start_time < time_seconds:
        for var in variables:
            value = get_variable_value(var)
            if value is not None:
                data[var] = np.append(data[var], float(value))
        time.sleep(sampling_frequency)
    return data

def open_route(route_file="course_data/ASC_2022/ASC2022_A.csv"):
    """
    Opens route data from file to produce dictionary.

    Args:
        route_file (string): path of the route file.

    Returns:
        dict: Dictionary with distance travelled as the key, and a tuple of (latitude, longitude) as the value.
    """
    route_dict = {}
    with open(route_file, "r", newline="") as file:
        for row in file:
            if not row.strip():
                continue
            spliced = row.split(",")
            try:
                lat, lon = float(spliced[4]), float(spliced[5])
                distance_travelled = float(spliced[0])
            except ValueError:
                continue
            route_dict[distance_travelled] = (lat, lon)
    enhanced_route_dict = NearestKeyDict(route_dict)
    return enhanced_route_dict

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
        # ctypes.windll.user32.MessageBoxW(0, "Please turn on Data Generator before plotting live data.", "Data Collection Error", 0)
        ##  Styles(Last Number):
        ##  0 : OK
        ##  1 : OK | Cancel
        ##  2 : Abort | Retry | Ignore
        ##  3 : Yes | No | Cancel
        ##  4 : Yes | No
        ##  5 : Retry | Cancel 
        ##  6 : Cancel | Try Again | Continue

        root = tk.Tk()
        root.withdraw()

        def show_error():
            messagebox.showerror("Data Collection Error", "Please turn on Data Generator before plotting live data.")
            root.quit()
        show_error()

        root.mainloop()


def launch_live_graph():
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

if __name__ == '__main__':
    # Example usage
    dashboard_data = edashboard_extract()
    if dashboard_data:
        print(f"Timestamp: {dashboard_data['timestamp']}")
        print(f"Data Format: {dashboard_data['data_format']}")