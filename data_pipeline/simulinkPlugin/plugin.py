import matlab.engine
import numpy as np
from data_pipeline.simulinkPlugin.config import constants

import os
_this = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(_this, os.pardir, os.pardir, os.pardir))
sim_folder   = os.path.join(project_root, "race-profile", "Simulation")

# Start the MATLAB engine
print("Starting MATLAB Engine...")
eng = matlab.engine.start_matlab()
eng.addpath(sim_folder, nargout=0)
model_file = os.path.join(sim_folder, "Car.slx")
model = "Car"
eng.load_system(model_file, nargout=0)
print("MATLAB engine started, Car model loaded.")

def load_constants():
    print("Loading input parameters...")
    try:
        for key, value in constants.items():
            eng.workspace[key] = value
            value_str = str(value)
            str_len = len(value_str)
            ## Uncomment below line to see which variables are being loaded.
            #print(f"Set {key} = {(value_str[:40] + "..." + value_str[-40:]) if str_len > 200 else value} in MATLAB workspace.")
        print("Loaded all input parameters to MATLAB workspace.")

    except Exception as e:
        print(f"An error occurred: {e}")


def retreive_constants():
    try:
        # Get all variable names
        print("Retreiving Constants...")
        variable_names = eng.who()
        # Retrieve all variables and their values into a dictionary
        workspace_dict = {}
        for var_name in variable_names:
            value = eng.workspace[var_name]
            # Convert MATLAB arrays to Python lists
            if isinstance(value, matlab.double):
                value = np.array(value).tolist()
            workspace_dict[var_name] = value

        # Print the results
        print("MATLAB workspace variables:")
        for key, value in workspace_dict.items():
            value_str = str(value)
            str_len = len(value_str)
            print(f"{key}: {(value_str[:40] + "..." + value_str[-40:]) if str_len > 200 else value}")
        print("")    
    except Exception as e:
        print(f"An error occurred: {e}")

def run_simulation():
        print("Running the Simulation...")
        sim_out = eng.sim(model, 'StopTime', str(constants['PROFILE_LENGTH']), nargout=1)
        eng.workspace['out'] = sim_out
        print("Simulation Completed.")

        # Extract tout and logsout
        sim_out = eng.workspace['out']
        tout = np.array(eng.getfield(sim_out, 'tout'))
        logsout = eng.getfield(sim_out, 'logsout')

        # Get number of signals
        num_elements = eng.getfield(logsout, 'numElements')
        if num_elements == 0:
            raise ValueError("No signals logged in logsout. Check Simulink model logging settings.")
        print(f"Number of signals in logsout: {num_elements}")

        # Print signal names and indices
        print("Signals in logsout:")
        for i in range(1, int(num_elements) + 1):  # 1-based indexing for MATLAB
            name = eng.eval(f"out.logsout{{{i}}}.Name") or f"Unnamed Signal {i}"
            print(f"Index {i}: {name}")

        # Extract the velocity signal (Signal 35)
        velocity_index = 35  # 1-based indexing for MATLAB
        velocity_data = eng.eval(f"out.logsout{{{velocity_index}}}.Values.Data")
        velocity_data = np.array(velocity_data).flatten()  # Ensure 1D array
        velocity_name = eng.eval(f"out.logsout{{{velocity_index}}}.Name") or "Velocity"

        # Verify data shape
        if velocity_data.shape[0] != tout.shape[0]:
            raise ValueError(f"Velocity data length {velocity_data.shape[0]} does not match tout length {tout.shape[0]}.")

        # Return tout, velocity signal, and name
        return tout, velocity_data, velocity_name

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")

if __name__ == '__main__':
    from config import constants
    load_constants()
    retreive_constants()
    close_workspace()