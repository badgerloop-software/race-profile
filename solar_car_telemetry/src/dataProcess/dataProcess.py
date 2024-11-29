import pandas as pd

"""
Extract data from the various dataframes for each relevant variable and prepare it to send to Simulink.
"""
batteryFile = 'solar_car_telemetry/src/dataProcess/testData/battery_const.csv'

def loadIntoPandas(csv_filename):
    """
    Given a csv file, load data into a Pandas dataframe.
    """
    df1 = pd.read_csv(csv_filename)
    return df1 

def extractDFfromTimeSeries():
    """
    Extract data from the time series data and return a Pandas dataframe.
    """
    pass

def findAvgValue(dfp):
    """
    Given data in a Pandas Dataframe, find the average value of the second column and return.
    """
    avg = dfp.iloc[:, 1].mean()
    return avg

if __name__ == '__main__':
    batteryDF = loadIntoPandas(batteryFile)
    print(findAvgValue(batteryDF))