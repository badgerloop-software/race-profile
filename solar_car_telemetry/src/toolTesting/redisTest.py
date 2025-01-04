import redis
from redis.commands.json.path import Path
import redis.commands.search.aggregation as aggregations
import redis.commands.search.reducers as reducers
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query


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

def redis_json():
    """Example for index and querying JSON documents in Redis"""
    try:
        r = redis.StrictRedis(host = redis_host, port = redis_port, decode_responses=True)
        user1 = {
            "name": "Paul John",
            "email": "paul.john@example.com",
            "age": 42,
            "city": "London"
        }
        user2 = {
            "name": "Eden Zamir",
            "email": "eden.zamir@example.com",
            "age": 29,
            "city": "Tel Aviv"
        }
        user3 = {
            "name": "Paul Zamir",
            "email": "paul.zamir@example.com",
            "age": 35,
            "city": "Tel Aviv"
        }

        schema = (
            TextField("$.name", as_name="name"), 
            TagField("$.city", as_name="city"), 
            NumericField("$.age", as_name="age")
        )

        rs = r.ft("idx:users")
        rs.create_index(
            schema,
            definition=IndexDefinition(
                prefix=["user:"], index_type=IndexType.JSON
            )
        )

        r.json().set("user:1", Path.root_path(), user1)
        r.json().set("user:2", Path.root_path(), user2)
        r.json().set("user:3", Path.root_path(), user3)

        res = rs.search(
        Query("Paul @age:[30 40]")
        )

        rs.search(
        Query("Paul").return_field("$.city", as_field="city")
        ).docs

        req = aggregations.AggregateRequest("*").group_by('@city', reducers.count().alias('count'))
        print(rs.aggregate(req).rows)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    redis_json()