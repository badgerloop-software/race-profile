import redis
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

redis_host = 'localhost'
redis_port = 6379

r = redis.StrictRedis(host = redis_host, port = redis_port, db = 0, decode_responses=True)

def save_variables(debug = False): 
    """
    Reads Variables from Redis and returns it into a Pandas DataFrame
    """
    try:
        keys = r.keys()
        values = r.mget(keys)

        dataList = []
        valueList = []
        for key in keys:           
            dataList.append(key)
            valueList.append(values[keys.index(key)])
            #print(f"{key}")
            #print(f"{key}, {values[keys.index(key)]}")
        
        df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        df = df.sort_values(by=['telem_variables'])        
        #df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        if debug != False:
            print(df)
        return df
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    save_variables(True)