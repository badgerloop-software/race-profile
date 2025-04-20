import matlab.engine
import numpy as np
from data_pipeline.simulinkPlugin.config import constants

# Start the MATLAB engine
print("Starting MATLAB Engine...")
eng = matlab.engine.start_matlab()
print("MATLAB engine started.")

def load_constants():
    try:
        for key, value in constants.items():
            eng.workspace[key] = value
            value_str = str(value)
            str_len = len(value_str)
            print(f"Set {key} = {(value_str[:40] + "..." + value_str[-40:]) if str_len > 200 else value} in MATLAB workspace.")
        print("")

    except Exception as e:
        print(f"An error occurred: {e}")

def load_model():
    # Change the current working directory to where the model is located
    model_path = 'Simulation/Car.slx'  # Replace with the path to your model
    eng.cd(model_path)

    # Load and simulate the model
    model_name = 'Car'  # Model name without the .slx extension
    eng.load_system(model_name)

    # Allocate res list to hold the results from 4 calls to sim_the_model
    res = [0]*4;

    ## 1st sim: with default parameter values
    res[0] = eng.Car()

    eng.sim(model_name)

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

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")

if __name__ == '__main__':
    from config import constants
    load_constants()
    retreive_constants()
    close_workspace()