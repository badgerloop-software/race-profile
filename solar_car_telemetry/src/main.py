"""
Read telemetry data from Redis and 
provide access to the data in a structured
format for the simulation.
"""
import redis
from redisExtract import extractVars

def main():
    """
    Handle telemetry data pipeline between Redis database and Simulink model.
    """

    #Initialize list of desired parameters to request
    desired_params = ['speed', 'pack_voltage', 'headlights_led_en', 'motor_current', 'fan_speed', 'air_temp', 'pack_power', 'soc']
    
    extractVars.print_variables()
    #extractVars.redis_get_variables()

    # Start MATLAB engine with Simulink support
    # self.matlab_eng = matlab.engine.start_matlab()
    # # Load Simulink libraries
    # self.matlab_eng.eval('load_system(\'simulink\')', nargout=0)

    

    # async def update_simulink_model(self, df: pd.DataFrame, model_name: str, block_paths: Dict[str, str]):
    #     """
    #     Updates Simulink model parameters with telemetry data
    #     
    #     Args:
    #         df: pandas DataFrame with telemetry data
    #         model_name: Name of Simulink model (.slx file)
    #         block_paths: Dict mapping parameter names to Simulink block paths
    #     """
    #     try:
    #         # Load Simulink model
    #         self.matlab_eng.eval(f"load_system('{model_name}')", nargout=0)
    #         
    #         # Update each parameter in the model
    #         for param, block_path in block_paths.items():
    #             if param in df.columns:
    #                 # Convert data to MATLAB array
    #                 mat_data = matlab.double(df[param].tolist())
    #                 # Set block parameter
    #                 self.matlab_eng.set_param(block_path, 'Value', mat_data, nargout=0)
    #         
    #         # Update model
    #         self.matlab_eng.eval('set_param(gcs, \'SimulationCommand\', \'update\')', nargout=0)
    #         
    #     except Exception as e:
    #         print(f"Error updating Simulink model: {str(e)}")
    #         raise

    # async def run_simulation(self, time_window_minutes: int = 60):
    #     """
    #     Main workflow: collects telemetry and updates Simulink simulation
    #     """
    #     end_time = '+'
    #     start_time = round((time.time() - (time_window_minutes * 60)) * 1000)
    # 
    #     # Define parameter mapping to Simulink blocks
    #     block_paths = {
    #         'temperature': 'model_name/Temperature_Input',
    #         'pressure': 'model_name/Pressure_Input',
    #         'flow_rate': 'model_name/FlowRate_Input'
    #     }
    # 
    #     try:
    #         df = await self.fetch_telemetry_dataset(
    #             param_list=list(block_paths.keys()),
    #             start_time=start_time,
    #             end_time=end_time
    #         )
    # 
    #         if df is not None:
    #             await self.update_simulink_model(df, 'your_model.slx', block_paths)
    #             # Run simulation
    #             self.matlab_eng.eval('set_param(gcs, \'SimulationCommand\', \'start\')', nargout=0)
    #             return True
    #         return False
    #         
    #     except Exception as e:
    #         print(f"Simulation error: {str(e)}")
    #         return False

    #def cleanup(self):
    #    """Closes connections and releases resources"""
        # try:
        #     self.matlab_eng.eval('close_system(gcs)', nargout=0)
        # except:
        #     pass
        #self.redis_client.close()
        # self.matlab_eng.quit()



if __name__ == "__main__":
    main()