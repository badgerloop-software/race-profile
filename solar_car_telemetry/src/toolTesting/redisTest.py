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

if __name__ == '__main__':
    redis_string()
    redis_integer()