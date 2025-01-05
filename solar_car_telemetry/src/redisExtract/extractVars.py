import redis, config
import pandas as pd
import json
redis_host = 'localhost'
redis_port = 6379



def print_variables():
    try:
        r = redis.StrictRedis(host = config.REDIS_URL, port = config.REDIS_PORT, db = config.REDIS_DB, decode_responses=True)
        keys = r.keys()
        values = r.mget(keys)

        dataList = []
        valueList = []
        for key in keys:           
            dataList.append(key)
            valueList.append(values[keys.index(key)])
            print(f"{key}")
            print(f"{key}, {values[keys.index(key)]})")
        
        #df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        #df = df.sort_values(by=['telem_variables'])
        #df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        
    except Exception as e:
        print(e)

def redis_get_variables():
    r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
    r.hgetall("bps_fault")

if __name__ == '__main__':
    get_variables()