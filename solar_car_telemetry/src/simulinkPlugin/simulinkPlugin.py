"""
Send data to Simulink and launch the Simulink model.
"""

def launchSimulink():
    """
    Launch the Simulink model.
    """
    eng = matlab.engine.start_matlab()
    eng.sim('Car.slx')
    pass

if __name__ == '__main__':
    launchSimulink()