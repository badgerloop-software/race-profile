import pandas as pd
import redis
import numpy as np
import time

"""
Extract data for each relevant variable in the list and prepare it to send to Simulink.
"""

def loadIntoPandas(csv_filename = 'solar_car_telemetry/src/dataProcess/testData/battery_const.csv'):
    """
    Given a csv file, load data into a Pandas dataframe.
    """
    df1 = pd.read_csv(csv_filename)
    return df1 

# def extractTimeSeries(startTime: int, endTime: int):
#     """
#     Extract data from the time series data (and return a Pandas dataframe).
#     """
#     r = redis.Redis()
#     data = r.ts().range('time_series', startTime, endTime)
#     df = pd.DataFrame(data, columns=['timestamp', 'value'])
#     return df

def remove_outliers(numpy_array: np.array):
    """
    Given a numpy array, remove any outliers.
    """
    q1 = np.percentile(numpy_array, 25) 
    q2 = np.percentile(numpy_array, 50) 
    q3 = np.percentile(numpy_array, 75) 
    iqr = q3 - q1
    
    # print(f"25th percentile(Q1): {q1}")
    # print(f"50th percentile((Median): {q2}")
    # print(f"75th percentile(Q3): {q3}")

    high = q3 + (1.5 * iqr)
    low = q1 - (1.5 * iqr)

    removed_outliers = np.array([])

    for i in range(len(numpy_array)):
        if(numpy_array[i] <= high and numpy_array[i] >= low):
            removed_outliers = np.append(removed_outliers, numpy_array[i])
    
    #print(removed_outliers)
    return removed_outliers

def process_recorded_values(numpy_dict, input_variables):
    """
    Given a dictionary which includes input variables as a key 
    and the numpy array of the corresponding variables recorded, remove outliers from the numpy
    array and find the mean.
    """
    averaged_values = np.array([])
    for variable in input_variables:
        #Remove outliers from this numpy array and calculate the average.
        averaged_values = np.append(averaged_values, np.mean(remove_outliers(numpy_dict[variable])))
    #print(averaged_values)
    return(averaged_values)
    
def test_process_recorded_values(var_list_length = 20, npy_arr_length = 300):
    """
    Creates test data for multiple variables (20 total by default), each with about
    300 random values by default, then invokes process_recorded_values.
    """
    start_time = time.perf_counter()
    import numpy as np

    # Generate sample dictionary with 20 variables
    variable_names = [f"Var{i}" for i in range(1, var_list_length + 1)]
    sample_data = {}
    for var in variable_names:
        sample_data[var] = np.random.randn(npy_arr_length)  # 300 random values

    # print(f"Variable names: {variable_names}")
    # print("Sample data")
    # print(sample_data)

    # Process recorded values
    means = process_recorded_values(sample_data, variable_names)
    print("Processed means:")
    print(means)
    # print(len(means))
    elapsed_time = time.perf_counter() - start_time
    print(f"Function execution time: {elapsed_time:.6f} seconds")

if __name__ == '__main__':
    # batteryDF = loadIntoPandas()
    # print( "batteryDF: ")
    # print(batteryDF)

    test_process_recorded_values(50, 600)