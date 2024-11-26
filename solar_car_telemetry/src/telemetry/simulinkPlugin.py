import pandas as pd
#import matlab.engine

"""
Extract data from the various dataframes for each car and plug in the appropriate values(averages) to plug into MATLAB.
"""
batteryFile = 'Data\const_battery.csv'
def loadIntoPandas(csv_filename):
    """
    Given a csv file, load data into a Pandas dataframe.
    """
    df1 = pd.read_csv(csv_filename)
    return df1

def findAvgValue(dfp):
    """
    Given data in a Pandas Dataframe, find the average value of the second column and return.
    """
    avg = dfp.iloc[:, 1].mean()
    return avg

def launchSimulink():
    """
    Launch the Simulink model.
    """
    eng = matlab.engine.start_matlab()
    eng.sim('Car.slx')
    pass

if __name__ == '__main__':
    batteryDF = loadIntoPandas(batteryFile)
    print(findAvgValue(batteryDF))