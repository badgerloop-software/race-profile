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
    # Run the simulation
    sim_out = eng.sim(model, 'StopTime', str(constants['PROFILE_LENGTH']), nargout=1)
    
    # Assign the raw output to the MATLAB workspace variable 'out' (optional, but might be useful for debugging in MATLAB)
    eng.workspace['out'] = sim_out 
    
    print("--- Inspecting Simulation Output from MATLAB Workspace ---")
    processed_output = {} # Dictionary to hold extracted data
    try:
        # Access the 'out' variable directly from the returned object or workspace
        # Note: sim_out might be the same as eng.workspace['out'] depending on MATLAB Engine behavior
        matlab_out = eng.workspace['out'] # Or potentially use sim_out directly if it works

        print(f"Type of 'out' in MATLAB workspace: {type(matlab_out)}")
        
        # Check for logsout (common for signal logging)
        if hasattr(matlab_out, 'logsout'):
            logsout_data = matlab_out.logsout
            print(f"Found 'logsout': {type(logsout_data)}")
            signal_names = eng.eval("get(out.logsout,'ElementNames')", nargout=1)
            print(f"  Logged signal names: {signal_names}")
            
            processed_output['logsout'] = {}
            if signal_names: # Ensure signal_names is not empty
                 for name in signal_names:
                    try:
                        # Access signal data: signal_object.Values.Data
                        # Access time: signal_object.Values.Time
                        signal_object = eng.eval(f"out.logsout.get('{name}')", nargout=1)
                        signal_data = np.array(eng.getProperty(signal_object.Values, 'Data')).flatten().tolist() # Convert to numpy array then list
                        signal_time = np.array(eng.getProperty(signal_object.Values, 'Time')).flatten().tolist() # Convert to numpy array then list
                        processed_output['logsout'][name] = {'time': signal_time, 'data': signal_data}
                        print(f"    Extracted '{name}' (Length: {len(signal_data)})")
                    except Exception as e:
                        print(f"    Error extracting data for signal '{name}': {e}")

        # Check for yout (common for 'To Workspace' blocks)
        elif hasattr(matlab_out, 'yout'):
             yout_data = matlab_out.yout
             print(f"Found 'yout': {type(yout_data)}")
             try:
                 # Attempt conversion to numpy array
                 np_yout = np.array(yout_data)
                 processed_output['yout'] = np_yout
                 print(f"  'yout' converted to numpy array shape: {np_yout.shape}")
             except Exception as e:
                 print(f"  Could not convert 'yout' to numpy array: {e}")
                 processed_output['yout'] = yout_data # Store raw object if conversion fails

        # Add checks for other potential output structures if needed

        # Store the raw MATLAB object as well, if desired
        processed_output['raw_matlab_object'] = sim_out 

    except Exception as e:
        print(f"Error inspecting or processing output from MATLAB workspace: {e}")
        processed_output['error'] = str(e)
        processed_output['raw_matlab_object'] = sim_out # Still return raw object on error

    print("--- End Workspace Inspection ---")
    
    # Return the processed dictionary instead of the raw MATLAB object
    return processed_output

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")

if __name__ == '__main__':
    from config import constants
    load_constants()
    retreive_constants()
    close_workspace()