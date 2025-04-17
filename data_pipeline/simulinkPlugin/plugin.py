"""Interface to the car simulation MATLAB package"""

import os
import sys

# Add the package directory to Python path
car_sim_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           "car_package", "Lib", "site-packages")
if car_sim_path not in sys.path:
    sys.path.append(car_sim_path)

import car1_sim

class CarSimulator:
    """Wrapper for the MATLAB-generated car simulation"""
    
    def __init__(self):
        """Initialize the MATLAB runtime and simulation"""
        self.matlab_instance = car1_sim.initialize()
    
    def run_simulation(self, target_speed=20, target_power=500, control_mode=1, start_soc=1.0):
        """
        Run the car simulation with the given parameters
        
        Parameters:
        - target_speed: Target speed in m/s
        - target_power: Power in kW
        - control_mode: 0 for speed control, 1 for power control
        - start_soc: Starting battery state of charge (0-1)
        
        Returns:
            Simulation results or None if error
        """
        try:
            # Use the car_simulation function (not setuptest)
            results = self.matlab_instance.car_simulation(
                TargetSpeed=target_speed,
                TargetPower=target_power,
                ControlMode=control_mode,
                StartSoc=start_soc
            )
            return results
        except Exception as e:
            print(f"Error running simulation: {e}")
            return None
    
    def __del__(self):
        """Clean up MATLAB runtime"""
        if hasattr(self, 'matlab_instance'):
            try:
                self.matlab_instance.terminate()
            except:
                pass

# Example usage
if __name__ == "__main__":
    # Initialize the package
    instance = car1_sim.initialize()
    
    # Print all available methods (excluding private ones)
    print("Available methods:")
    methods = [m for m in dir(instance) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")
        
    # Clean up
    instance.terminate()