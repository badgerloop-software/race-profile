import pandas as pd
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def save_variables(): 
    try:
        keys = r.keys()
        values = r.mget(keys)

        dataList = []
        valueList = []
        for key in keys:           
            dataList.append(key)
            valueList.append(values[keys.index(key)])
            print(f"{key}")
            print(f"{key}, {values[keys.index(key)]}")
        
        df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        print(df)
        #df = df.sort_values(by=['telem_variables'])
        #df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        
    except Exception as e:
        print(e)