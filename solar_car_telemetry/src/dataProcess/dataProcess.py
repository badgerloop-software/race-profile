import pandas as pd
import redis

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

def extractTimeSeries(startTime: int, endTime: int):
    """
    Extract data from the time series data (and return a Pandas dataframe).
    """
    r = redis.Redis()
    data = r.ts().range('time_series', startTime, endTime)
    df = pd.DataFrame(data, columns=['timestamp', 'value'])
    return df

def findAvgValue(dfp):
    """
    Compute the rolling average of the time series data and store it in Redis.
    """
    r = redis.Redis()
    rolling_avg = dfp['value'].rolling(window=5).mean()
    # Create a new time series in Redis for the rolling average
    r.ts().create('rolling_average')
    # Add the rolling average data points to Redis
    for ts, val in zip(dfp['timestamp'], rolling_avg):
        if not pd.isna(val):
            r.ts().add('rolling_average', ts, val)
    return rolling_avg

if __name__ == '__main__':
    batteryDF = loadIntoPandas(batteryFile)
    print(findAvgValue(batteryDF))