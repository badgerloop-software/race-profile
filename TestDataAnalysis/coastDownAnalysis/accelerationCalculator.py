# python
import os
import glob
import pandas as pd

def convert_velocity(velocity_mph):
    """Convert velocity from miles per hour to meters per second."""
    return velocity_mph * 0.44704

def calculate_acceleration(timestamps, velocities):
    """Calculate acceleration from discrete velocities."""
    accelerations = []
    avg_velocities = []
    
    for i in range(1, len(velocities)):
        delta_v = velocities[i] - velocities[i - 1]
        delta_t = timestamps[i] - timestamps[i - 1]
        
        if delta_t != 0:
            acceleration = delta_v / delta_t
            avg_velocity = (velocities[i] + velocities[i - 1]) / 2
            
            if acceleration < 0:
                accelerations.append(acceleration)
                avg_velocities.append(avg_velocity)
    
    return avg_velocities, accelerations

def process_csv_files():
    """Process all CSV files starting with 'coast'."""
    input_files = glob.glob("coast*.csv")
    output_dir = "acc_vel"
    os.makedirs(output_dir, exist_ok=True)
    
    for input_file in input_files:
        data = pd.read_csv(input_file)
        timestamps = data.iloc[:, 0].values
        velocities_mph = data.iloc[:, 2].values
        
        velocities_ms = [convert_velocity(v) for v in velocities_mph]
        
        # Handle velocity plateaus
        filtered_timestamps = []
        filtered_velocities = []
        
        i = 0
        while i < len(velocities_ms):
            start = i
            while i < len(velocities_ms) - 1 and velocities_ms[i] == velocities_ms[i + 1]:
                i += 1
            end = i
            midpoint = (timestamps[start] + timestamps[end]) / 2
            filtered_timestamps.append(midpoint)
            filtered_velocities.append(velocities_ms[start])
            i += 1
        
        avg_velocities, accelerations = calculate_acceleration(filtered_timestamps, 
                                                               filtered_velocities)
        
        output_data = pd.DataFrame({
            'velocity_m/s': avg_velocities,
            'acceleration_m/s^2': accelerations
        })
        
        output_file = os.path.join(output_dir, "acc_vel_" + os.path.basename(input_file))
        output_data.to_csv(output_file, index=False)

if __name__ == "__main__":
    process_csv_files()