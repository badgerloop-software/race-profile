from typing import Dict, Optional
import numpy as np
from scipy.io import savemat
from datetime import datetime
from ..config.settings import TELEMETRY_PARAMETERS

class SimulationConverter:
    """Converts telemetry data into formats suitable for simulation"""
    
    def __init__(self):
        self.supported_types = (np.ndarray, list, float, int)
        
    def to_matlab_workspace(self, data: Dict, include_metadata: bool = True) -> Dict:
        """
        Converts telemetry data to MATLAB workspace variables
        
        Args:
            data: Dictionary of parameter arrays
            include_metadata: Whether to include metadata
            
        Returns:
            Dictionary of MATLAB workspace variables
        """
        matlab_dict = {}
        
        # Convert timestamps to simulation time vector
        timestamps = data['timestamps']
        t0 = timestamps[0]
        matlab_dict['sim_time'] = (timestamps - t0) / 1000  # Convert to seconds
        
        # Convert parameters to simulation variables
        for param_name, param_data in data.items():
            if param_name != 'timestamps':
                # Get the corresponding Simulink variable name
                sim_var = TELEMETRY_PARAMETERS[param_name]['simulink_variable']
                matlab_dict[sim_var] = np.array(param_data)
        
        # Add metadata if requested
        if include_metadata:
            matlab_dict['metadata'] = {
                'start_time': datetime.fromtimestamp(t0/1000).isoformat(),
                'duration_seconds': (timestamps[-1] - t0) / 1000,
                'sample_count': len(timestamps),
                'parameters': list(data.keys())
            }
        
        return matlab_dict
    
    def save_simulation_data(
        self,
        data: Dict,
        output_file: str = 'telemetry_sim_data.mat'
    ) -> None:
        """
        Saves telemetry data in a format ready for simulation
        
        Args:
            data: Dictionary of parameter arrays
            output_file: Output .mat file path
        """
        # Convert to simulation format
        sim_data = self.to_matlab_workspace(data)
        
        # Save to .mat file
        savemat(output_file, sim_data)
        
    def create_simulink_dataset(
        self,
        data: Dict,
        output_file: str = 'telemetry_dataset.m'
    ) -> None:
        """
        Creates a MATLAB script that loads telemetry data into Simulink
        
        Args:
            data: Dictionary of parameter arrays
            output_file: Output .m file path
        """
        sim_data = self.to_matlab_workspace(data)
        
        # Create MATLAB script content
        script_lines = [
            "% Telemetry data for Simulink simulation",
            f"% Generated on {datetime.now().isoformat()}",
            "",
            "% Time vector",
            "sim_time = {};".format(repr(sim_data['sim_time'].tolist())),
            ""
        ]
        
        # Add each parameter
        for var_name, values in sim_data.items():
            if var_name not in ['sim_time', 'metadata']:
                script_lines.extend([
                    f"% {var_name}",
                    f"{var_name} = {};".format(repr(values.tolist())),
                    ""
                ])
        
        # Write the script
        with open(output_file, 'w') as f:
            f.write('\n'.join(script_lines))
