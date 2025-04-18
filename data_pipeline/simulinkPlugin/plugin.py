import matlab.engine
# from data_pipeline.simulinkPlugin.config import constants

# Start the MATLAB engine
print("Starting MATLAB Engine...")
eng = matlab.engine.start_matlab()
print("MATLAB engine started.")

def load_constants():
    try:
        for key, value in constants.items():
            eng.workspace[key] = value
            print(f"Set {key} = {value} in MATLAB workspace.")

    except Exception as e:
        print(f"An error occurred: {e}")

def retreive_new():
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
            print(f"{key}: {value}")
    except Exception as e:
        print(f"An error occurred: {e}")   

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")

if __name__ == '__main__':
    from config import constants
    load_constants()
    retreive_new()
    close_workspace()