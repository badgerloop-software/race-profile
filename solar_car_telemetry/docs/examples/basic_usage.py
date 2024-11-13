"""
Basic example of fetching telemetry data and converting to MATLAB format
"""

import asyncio
from datetime import datetime, timedelta
from telemetry_reader import TelemetryReader
from matlab_converter import MatlabConverter

async def main():
    # Create our reader and converter
    reader = TelemetryReader()
    converter = MatlabConverter()
    
    # Calculate time window (last 30 minutes)
    end_time = round(datetime.now().timestamp() * 1000)
    start_time = end_time - (30 * 60 * 1000)
    
    # Parameters we want to collect
    parameters = [
        'vehicle_speed',    # Vehicle speed in mph
        'pack_voltage',     # Battery pack voltage
        'pack_current',     # Battery pack current
        'battery_temp',     # Battery temperature
        'motor_temp'        # Motor temperature
    ]
    
    try:
        # Fetch the data
        print("Fetching telemetry data...")
        data = await reader.get_historical_data(
            parameter_list=parameters,
            start_time=start_time,
            end_time=end_time,
            use_aggregation=True,    # Use aggregation for smoother data
            agg_interval=1000        # 1 second intervals
        )
        
        # Convert to MATLAB format
        print("Converting to MATLAB format...")
        output_file = 'race_data.mat'
        converter.convert_telemetry(data, output_file)
        
        print(f"Data saved to {output_file}")
        print("You can now load this file in MATLAB!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your connection and try again")

if __name__ == "__main__":
    asyncio.run(main())
