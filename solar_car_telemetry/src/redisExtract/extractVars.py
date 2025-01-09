import redis, solar_car_telemetry.src.config as config
import pandas as pd
import json
redis_host = 'localhost'
redis_port = 6379
r = redis.StrictRedis(host = config.REDIS_URL, port = config.REDIS_PORT, db = config.REDIS_DB, decode_responses=True)


def print_variables(): 
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
        
        #df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        #df = df.sort_values(by=['telem_variables'])
        #df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        
    except Exception as e:
        print(e)

    
async def request_data(keys: list, starting_time, ending_time):
    try:
        df = pd.DataFrame()
        min_length = float('inf')

        for i in range(len(keys)):
            #Retreive the data from the redis database
            data = r.execute_command('TS.RANGE', keys[i], starting_time, ending_time)

            #Parse the data into a list of tuples
            value = [float(x[1]) for x in data]
            index = [x[0] for x in data]
            column_name = keys[i]

            #Create a dataframe from the data
            df2 = pd.DataFrame({column_name: value}, index=index)

            #If a shorter array is found, update the min_length
            if len(value) < min_length:
                min_length = len(value)

            if df.empty:
                df = df2
            else:
                df.pd.concat([df, df2], axis=1)
        
        df = df.iloc[:min_length]
        return df

    except Exception as e:
        print(e)

if __name__ == '__main__':
    print_variables()