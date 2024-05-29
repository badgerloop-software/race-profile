# python
import os
import glob
import pandas as pd

def filter_acceleration_trend(file_path):
    """Filter data pairs to maintain a downward trend in acceleration."""
    data = pd.read_csv(file_path)
    data = data.sort_values(by='velocity_m/s').reset_index(drop=True)
    
    filtered_data = []
    previous_acceleration = float('inf')
    
    for index, row in data.iterrows():
        current_acceleration = row['acceleration_m/s^2']
        if current_acceleration <= previous_acceleration:
            filtered_data.append(row)
            previous_acceleration = current_acceleration
    
    return pd.DataFrame(filtered_data)

def process_filtered_files(input_folder):
    """Process all CSV files starting with 'acc_vel' in the specified folder."""
    input_files = glob.glob(os.path.join(input_folder, "acc_vel*.csv"))
    
    for input_file in input_files:
        filtered_data = filter_acceleration_trend(input_file)
        
        output_file = os.path.join(input_folder, 
                                   "filtered_" + os.path.basename(input_file))
        filtered_data.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_folder = "."  # Current directory; change as needed
    process_filtered_files(input_folder)