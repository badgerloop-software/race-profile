"""
This file will just connect and read to the redis server.
"""
from redis import Redis

# Create a connection
redis_client = Redis(
    host='localhost',    # Redis server host
    port=6379,          # Default Redis port
    decode_responses=True  # Automatically decode responses to Python strings
)

# Test connection
redis_client.ping()  # Should return True if connected

# Set a string value
redis_client.set('user:name', 'John Doe')

# Get a string value
name = redis_client.get('user:name')
print(f"user:name = {name}")

# Sample keys from the Redis database and print their values
cursor, keys = redis_client.scan()
for key in keys:
    value = redis_client.get(key)
    print(f"{key} = {value}")