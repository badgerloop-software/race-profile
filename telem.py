import redis
import pandas as pd
import numpy as np
import matlab.engine
import time
from typing import List, Dict, Any

class SimulinkTelemetryHandler:
    """
    Handles telemetry data pipeline between Redis database and Simulink model.
    """
    def __init__(self, redis_host='localhost', redis_port=6379):
        # Initialize Redis connection
        self.redis_client = redis.Redis(host=redis_host, port=redis_port)
        # Start MATLAB engine with Simulink support
        self.matlab_eng = matlab.engine.start_matlab()
        # Load Simulink libraries
        self.matlab_eng.eval('load_system(\'simulink\')', nargout=0)
    
    async def fetch_telemetry_dataset(self, param_list: List[str], start_time: int, end_time: int) -> pd.DataFrame:
        """Fetches time series data from Redis"""
        data = {}
        for param in param_list:
            values = self.redis_client.xrange(param, 
                                           min=str(start_time), 
                                           max=str(end_time) if end_time != '+' else '+')
            
            timestamps = []
            measurements = []
            for entry in values:
                timestamp = int(entry[0].decode('utf-8').split('-')[0])
                value = float(entry[1][b'value'])
                timestamps.append(timestamp)
                measurements.append(value)
                
            data[param] = measurements
            
        return pd.DataFrame(data, index=timestamps)

    async def update_simulink_model(self, df: pd.DataFrame, model_name: str, block_paths: Dict[str, str]):
        """
        Updates Simulink model parameters with telemetry data
        
        Args:
            df: pandas DataFrame with telemetry data
            model_name: Name of Simulink model (.slx file)
            block_paths: Dict mapping parameter names to Simulink block paths
        """
        try:
            # Load Simulink model
            self.matlab_eng.eval(f"load_system('{model_name}')", nargout=0)
            
            # Update each parameter in the model
            for param, block_path in block_paths.items():
                if param in df.columns:
                    # Convert data to MATLAB array
                    mat_data = matlab.double(df[param].tolist())
                    # Set block parameter
                    self.matlab_eng.set_param(block_path, 'Value', mat_data, nargout=0)
            
            # Update model
            self.matlab_eng.eval('set_param(gcs, \'SimulationCommand\', \'update\')', nargout=0)
            
        except Exception as e:
            print(f"Error updating Simulink model: {str(e)}")
            raise

    async def run_simulation(self, time_window_minutes: int = 60):
        """
        Main workflow: collects telemetry and updates Simulink simulation
        """
        end_time = '+'
        start_time = round((time.time() - (time_window_minutes * 60)) * 1000)

        # Define parameter mapping to Simulink blocks
        block_paths = {
            'temperature': 'model_name/Temperature_Input',
            'pressure': 'model_name/Pressure_Input',
            'flow_rate': 'model_name/FlowRate_Input'
        }

        try:
            df = await self.fetch_telemetry_dataset(
                param_list=list(block_paths.keys()),
                start_time=start_time,
                end_time=end_time
            )

            if df is not None:
                await self.update_simulink_model(df, 'your_model.slx', block_paths)
                # Run simulation
                self.matlab_eng.eval('set_param(gcs, \'SimulationCommand\', \'start\')', nargout=0)
                return True
            return False
            
        except Exception as e:
            print(f"Simulation error: {str(e)}")
            return False

    def cleanup(self):
        """Closes connections and releases resources"""
        try:
            self.matlab_eng.eval('close_system(gcs)', nargout=0)
        except:
            pass
        self.redis_client.close()
        self.matlab_eng.quit()