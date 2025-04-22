import matlab.engine
import numpy as np
from data_pipeline.simulinkPlugin.config import constants

import os
_this = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(_this, os.pardir, os.pardir, os.pardir))
sim_folder   = os.path.join(project_root, "race-profile", "Simulation")

# print(f"Project_root: {project_root}")
# print(f"sim_folder: {sim_folder}")

# Start the MATLAB engine
print("Starting MATLAB Engine...")
eng = matlab.engine.start_matlab()
eng.addpath(sim_folder, nargout=0)
model_file = os.path.join(sim_folder, "Car.slx")
model = "Car"
eng.load_system(model_file, nargout=0)
print("MATLAB engine started, Car model loaded.")

def load_constants():
    print("Loading input variables...")
    try:
        for key, value in constants.items():
            eng.workspace[key] = value
            value_str = str(value)
            str_len = len(value_str)
            ## Uncomment below line to see which variables are being loaded.
            #print(f"Set {key} = {(value_str[:40] + "..." + value_str[-40:]) if str_len > 200 else value} in MATLAB workspace.")
        print("Loaded all variables to MATLAB workspace.")

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
    # 2  Kick off the simulation
    print("Running the Simulation...")
    sim_out = eng.sim(model,'StopTime', str(constants['PROFILE_LENGTH']), nargout=1)
    return sim_out

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")

if __name__ == '__main__':
    from config import constants
    load_constants()
    retreive_constants()
    close_workspace()