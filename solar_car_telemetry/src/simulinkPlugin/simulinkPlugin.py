"""
Use this to send the data to the Simulink model
"""

import numpy as np
#import matlab.engine

def __init__(self):
    self.mle = matlab.engine.start_matlab()
    
def send_to_simulation(self, averaged_params):
    # Convert averages dict to MATLAB-compatible format
    tunable_params = {
        'speed': float(averaged_params['speed']),
        'pack_voltage': float(averaged_params['pack_voltage']),
        'motor_current': float(averaged_params['motor_current']),
        'fan_speed': float(averaged_params['fan_speed']),
        'air_temp': float(averaged_params['air_temp']),
        'pack_power': float(averaged_params['pack_power']),
        'soc': float(averaged_params['soc'])
    }
    
    # Run simulation with parameters
    result = self.mle.car2('TunableParameters', tunable_params,
                            'ConfigureForDeployment', 0)
    
    return result

def close(self):
    self.mle.quit()