"""
Given a list of parameters and a CSV file input, this function will
output a CSV file only containing the specified parameters.
"""
import pandas as pd

# Set the directories of the and output CSV files here
input_csv_filepath = 'solar_car_telemetry/src/dataProcess/testData/raw_data.csv'
output_csv_filepath = 'solar_car_telemetry/src/dataProcess/testData/sliced_data.csv'

# List of desired parameters in the output CSV file can go here
data_list = ['speed', 'pack_voltage', 'headlights_led_en', 'motor_current', 'fan_speed', 'air_temp', 'pack_power', 'soc']

timeseriesStart = 1559932000
def slice_data(input_file: str, output_file: str, params: list, timeseries: bool = False):
    """
    Args:
        input_file: CSV file containing the logged data
        output_file: CSV file to output the sliced data
        params: List of parameters to keep in the output CSV
        timeseries: If True, adds timestamp column starting from timeseriesStart
    """
    try:
        #Read file and extract desired variables
        data = pd.read_csv(input_file)
        sliced_data = data[params]
        
        if timeseries:
            # Create timestamp column and insert it at front of dataframe
            timestamps = range(timeseriesStart, timeseriesStart + len(sliced_data))
            sliced_data.insert(0, 'timestamp', timestamps)
            
        sliced_data.to_csv(output_file, index=False)
    except Exception as e:
        print(f"Error slicing data: {str(e)}")
        raise

slice_data(input_csv_filepath, output_csv_filepath, data_list, True)