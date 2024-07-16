import os
import pandas as pd
import glob
from datetime import datetime, timezone
import pytz

# Constants
WEATHER_DATA_PATH = 'TestDataAnalysis\\weatherTrackDay041424.csv'
OUTPUT_DIR = 'TestDataAnalysis\\coastDownAnalysis\\ReynoldsNum'
OUTPUT_FILE = 'combined_data.csv'
MPH_TO_MPS = 0.44704  # Conversion factor from mph to m/s

def list_coast_files(directory):
    """Find all files starting with 'coasts2024' in the given directory."""
    return glob.glob(os.path.join(directory, 'coasts2024*.csv'))

def read_coast_file(file_path):
    """
    Read a coast file, extracting unix timestamp and speed.
    Convert speed from mph to m/s.
    """
    df = pd.read_csv(file_path, usecols=[0, 2], names=['unix_timestamp', 'speed_mph'])
    
    # Convert unix_timestamp to numeric, replacing any non-numeric values with NaN
    df['unix_timestamp'] = pd.to_numeric(df['unix_timestamp'], errors='coerce')
    
    # Convert speed_mph to numeric, replacing any non-numeric values with NaN
    df['speed_mph'] = pd.to_numeric(df['speed_mph'], errors='coerce')
    
    # Drop any rows where unix_timestamp or speed_mph is NaN
    df = df.dropna(subset=['unix_timestamp', 'speed_mph'])
    
    # Convert speed to m/s
    df['speed_mps'] = df['speed_mph'] * MPH_TO_MPS
    
    return df[['unix_timestamp', 'speed_mps']]

def read_weather_data(file_path):
    """
    Read weather data file, extract relevant columns, and convert timestamp to UTC.
    """
    df = pd.read_csv(file_path, usecols=[0, 15, 16, 26])
    df.columns = ['temperature', 'relative_humidity', 'surface_pressure', 'timestamp']
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%SZ')
    df['timestamp'] = df['timestamp'].dt.tz_localize('US/Central').dt.tz_convert('UTC')
    
    # Convert humidity from percentage to decimal
    df['relative_humidity'] = df['relative_humidity'] / 100
    
    return df

def convert_unix_to_utc(unix_timestamp):
    """Convert Unix timestamp to UTC datetime."""
    return pd.to_datetime(unix_timestamp.astype(int) // 1000, unit='s', utc=True)

def process_data(coast_files, weather_data):
    """
    Process coast files and merge with weather data.
    Match each coast data point with the nearest weather data point.
    """
    all_data = []
    
    for coast_file in coast_files:
        try:
            coast_data = read_coast_file(coast_file)
            if coast_data.empty:
                print(f"Warning: No valid data in {coast_file}")
                continue
            
            coast_data['timestamp'] = convert_unix_to_utc(coast_data['unix_timestamp'])
            
            # Merge coast data with weather data
            merged_data = pd.merge_asof(coast_data, weather_data, 
                                        left_on='timestamp', right_on='timestamp',
                                        direction='nearest', tolerance=pd.Timedelta('5min'))
            
            all_data.append(merged_data)
        except Exception as e:
            print(f"Error processing file {coast_file}: {str(e)}")
            print(f"First few rows of problematic data:\n{coast_data.head()}")
    
    if not all_data:
        raise ValueError("No valid data found in any of the coast files")
    
    combined_data = pd.concat(all_data, ignore_index=True)
    return combined_data[['unix_timestamp', 'speed_mps', 'temperature', 'relative_humidity', 'surface_pressure']]

def test_file_reading():
    """
    Test function to read a specific coast file and print the first timestamp and speed data.
    """
    test_file = 'TestDataAnalysis\\coastDownAnalysis\\coasts2024-04-141530(5).csv'
    
    try:
        df = read_coast_file(test_file)
        if df.empty:
            print("The file is empty or contains no valid data.")
        else:
            first_row = df.iloc[0]
            print(f"First row of data from {test_file}:")
            print(f"Timestamp: {first_row['unix_timestamp']}")
            print(f"Speed (m/s): {first_row['speed_mps']:.2f}")
            
            # Optional: Print original speed in mph if available
            if 'speed_mph' in df.columns:
                print(f"Original Speed (mph): {df.iloc[0]['speed_mph']:.2f}")
    except Exception as e:
        print(f"Error reading test file: {str(e)}")

def main():
    """Main function to orchestrate the data processing and file creation."""
    # Run the test function
    test_file_reading()
    
    # Rest of your main function...
    coast_directory = 'TestDataAnalysis\\coastDownAnalysis'
    coast_files = list_coast_files(coast_directory)
    
    if not coast_files:
        print("No coast files found. Please check the directory.")
        return
    
    try:
        weather_data = read_weather_data(WEATHER_DATA_PATH)
        combined_data = process_data(coast_files, weather_data)
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        combined_data.to_csv(output_path, index=False)
        print(f"Combined data saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()