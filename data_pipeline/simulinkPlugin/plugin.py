import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_pipeline.simulinkPlugin.config import constants

eng = None
model = "Car"

import os
_this = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(_this, os.pardir, os.pardir, os.pardir))
sim_folder   = os.path.join(project_root, "race-profile", "Simulation")
model_file = os.path.join(sim_folder, model + ".slx")

def start_matlab_engine():
    """Starts the MATLAB engine, adds path, and loads the Simulink model."""
    global eng # Declare intention to modify the global 'eng' variable
    if eng is not None:
        print("MATLAB engine already started.")
        return True

    try:
        print("Starting MATLAB Engine...")
        eng = matlab.engine.start_matlab()
        print("Adding Simulink model path to MATLAB...")
        eng.addpath(sim_folder, nargout=0)
        print(f"Loading Simulink model '{model}' from {model_file}...")
        eng.load_system(model_file, nargout=0)
        print("MATLAB engine started, Car model loaded.")
        return True
    except Exception as e:
        print(f"Error starting MATLAB engine or loading model: {e}")
        eng = None # Ensure eng is None if startup failed
        return False

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

def run_simulation(signalsList):
    """
    Runs the Simulink simulation and processes specified output signals.

    Args:
        signalsList (list): A list of integers representing the 1-based indices
                           of the signals to extract from logsout.
    """
    if not signalsList:
        print("Warning: No signal indices provided in signalsList. Skipping data extraction.")
        return None # Or return an empty DataFrame/dict

    print("Running the Simulation...")
    sim_out = eng.sim(model, 'StopTime', str(constants['PROFILE_LENGTH']), nargout=1)
    eng.workspace['out'] = sim_out
    print("Simulation Completed.")
#    print("---------------------------------------------")

    # Extract tout and logsout
    try:
        sim_out_ws = eng.workspace['out']
        tout = np.array(eng.getfield(sim_out_ws, 'tout')).flatten()
        logsout = eng.getfield(sim_out_ws, 'logsout')
        num_elements = int(eng.getfield(logsout, 'numElements'))
    except Exception as e:
        raise RuntimeError(f"Failed to extract 'tout' or 'logsout' from simulation output: {e}")

    if num_elements == 0:
        raise ValueError("No signals logged in logsout. Check Simulink model logging settings.")
    # print(f"Total signals available in logsout: {num_elements}")


    # --- Print all available signal names and indices ---
    # print("--- Available Logged Signals (Index: Name) ---")
    all_signals = {}
    for i in range(1, num_elements + 1):
        try:
            name = eng.eval(f"out.logsout{{{i}}}.Name", nargout=1) or f"[Unnamed Signal {i}]"
            all_signals[i] = name
            # print(f"  {i}: {name}")
        except Exception as e:
            print(f"  Error retrieving name for index {i}: {e}")
    # print("---------------------------------------------") 

    # --- Extract requested signals ---
    extracted_data = {}
    extracted_names = {}
    print("--- Extracting Requested Signals ---")
    for signal_index in signalsList:
        if not isinstance(signal_index, int) or signal_index <= 0:
             print(f"Warning: Invalid signal index '{signal_index}' provided. Skipping.")
             continue
        if signal_index > num_elements:
             print(f"Warning: Signal index {signal_index} is out of bounds (max: {num_elements}). Skipping.")
             continue

        try:
            signal_data_raw = eng.eval(f"out.logsout{{{signal_index}}}.Values.Data", nargout=1)
            signal_data = np.array(signal_data_raw).flatten()
            signal_name = all_signals.get(signal_index, f"Signal_{signal_index}") # Use fetched name

            # Verify shape
            if signal_data.shape[0] != tout.shape[0]:
                # Attempt to handle potential dimension mismatches if appropriate (e.g., scalar expansion)
                # Or raise a more specific error
                raise ValueError(f"'{signal_name}' (Index {signal_index}) data length {signal_data.shape[0]} does not match tout length {tout.shape[0]}.")

            extracted_data[signal_index] = signal_data
            extracted_names[signal_index] = signal_name
            print(f"Successfully extracted '{signal_name}' (Index {signal_index})")

        except Exception as e:
            print(f"Error extracting data for index {signal_index}: {e}. Skipping this signal.")
            # Continue to next signal instead of raising immediately? Or re-raise if critical.
            # raise ValueError(f"Error extracting data at index {signal_index}. Check index/signal. Original error: {e}")

    if not extracted_data:
        print("No data was successfully extracted for the requested indices.")
        return None


    # --- Save data to CSV ---
    try:
        data_to_save = {'Time (s)': tout}
        # Add extracted signals using their names as keys
        for idx, name in extracted_names.items():
            data_to_save[name] = extracted_data[idx]

        df = pd.DataFrame(data_to_save)
        output_csv_path = 'Outputs/simulation_output.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        df.to_csv(output_csv_path, index=False)
        print(f"Simulation data saved to {output_csv_path}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")
        # Decide if you should still proceed to plotting

    # --- Plot Combined Signals ---
    # Note: Plotting many signals with different scales on multiple y-axes can become cluttered.
    print("--- Plotting Requested Signals ---")
    try:
        num_signals_to_plot = len(extracted_data)
        if num_signals_to_plot == 0:
             print("No signals to plot.")
        else:
            fig, ax1 = plt.subplots(figsize=(12, 6 + num_signals_to_plot * 0.5)) # Adjust height slightly for more axes
            axes = [ax1] # Store all axes
            lines = [] # Store line handles for legend
            colors = plt.cm.tab10(np.linspace(0, 1, num_signals_to_plot)) # Get distinct colors

            # Plot first signal on ax1
            first_idx = list(extracted_data.keys())[0]
            first_name = extracted_names[first_idx]
            first_data = extracted_data[first_idx]
            color = colors[0]
            ax1.set_xlabel('Time (s)')
            ax1.set_ylabel(first_name, color=color)
            line, = ax1.plot(tout, first_data, color=color, label=first_name)
            lines.append(line)
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.grid(True)

            # Plot subsequent signals on new twin axes
            axis_offset = 60 # Offset for additional y-axes labels
            for i, signal_index in enumerate(list(extracted_data.keys())[1:], start=1):
                ax_new = ax1.twinx()
                axes.append(ax_new)
                signal_name = extracted_names[signal_index]
                signal_data = extracted_data[signal_index]
                color = colors[i]

                # Position the new axis spine to prevent overlap
                ax_new.spines['right'].set_position(('outward', (i-1) * axis_offset))

                ax_new.set_ylabel(signal_name, color=color)
                line, = ax_new.plot(tout, signal_data, color=color, label=signal_name)
                lines.append(line)
                ax_new.tick_params(axis='y', labelcolor=color)
                # Only keep the spine for the new axis visible
                # ax_new.spines['left'].set_visible(False) # Keep left spine from ax1
                # ax_new.spines['top'].set_visible(False)

            plt.title(f'Race Strategy Simulation: {", ".join(extracted_names.values())} Over Time')

            # Add combined legend
            labels = [l.get_label() for l in lines]
            # Place legend carefully, maybe outside the plot
            ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=min(3, num_signals_to_plot), fancybox=True, shadow=True)

            fig.tight_layout(rect=[0, 0.05, 1, 1]) # Adjust layout to make space for legend below axes

            # Save the combined plot
            combined_plot_path = 'Outputs/simulation_combined_graph.png'
            plt.savefig(combined_plot_path, bbox_inches='tight') # Use bbox_inches='tight' to include legend
            print(f"Combined plot saved to {combined_plot_path}")
            # print("---------------------------------------------")
            plt.close(fig) # Close the figure

    except Exception as e:
        print(f"Error plotting combined graph: {e}")

    # # Return the DataFrame containing the extracted data
    # return df if 'df' in locals() else 
    
def run_optimization():
    print("Running Optimization Script...")
    return eng.run('Optimization/fminconWrapper.m', nargout=0)

def close_workspace():
    # Close the MATLAB engine
    eng.quit()
    print("MATLAB engine closed.")