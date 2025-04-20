import matlab.engine

# Start the MATLAB engine
eng = matlab.engine.start_matlab()
print("MATLAB engine started.")

try:
    # Step 1: Put a value into the MATLAB workspace
    variable_name = "my_value"
    variable_value = 42.0  # Example value (a double)
    eng.workspace[variable_name] = variable_value
    print(f"Set {variable_name} = {variable_value} in MATLAB workspace.")

    # Step 2: Retrieve and print the value from the MATLAB workspace
    retrieved_value = eng.workspace[variable_name]
    print(f"Retrieved {variable_name} from MATLAB workspace: {retrieved_value}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")