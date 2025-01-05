"""
Call the compile simulink function from Python and display results.
"""



def launchSimulink():
    """
    Launch the Simulink model.
    """
    eng = m.start_matlab()
    eng.sim('Car.slx')
    pass

if __name__ == '__main__':
    launchSimulink()