import redis
import pandas as pd
import json
redis_host = 'localhost'
redis_port = 6379

def redis_string():
    try:
        r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
        r.set('foo', 'bar')
        msg = r.get('foo')
        print(msg)
    except Exception as e:
        print(e)

def redis_integer():
    try:
        r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
        r.set('foo', 1)
        msg = r.get('foo')
        r.incr('foo')
        msg_incr = r.get('foo')
        print(msg)
        print(msg_incr)
    except:
        print("Something went wrong!")
def print_variables():
    try:
        r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
        keys = r.keys()
        values = r.mget(keys)

        dataList = []
        valueList = []
        for key in keys:           
            dataList.append(key)
            valueList.append(values[keys.index(key)])
            #print(f"{key}")
            #print(f"{key}, {values[keys.index(key)]})"
        
        df = pd.DataFrame({'telem_variables': dataList, 'data': valueList})
        df = df.sort_values(by=['telem_variables'])
        df.to_csv('solar_car_telemetry/src/telemetry/Data/parameter_list.csv', index=False)
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print_variables()