import redis
import pandas as pd
import json
from typing import Dict, Any, Optional

class TelemetryReader:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """Initialize the telemetry reader with Redis connection parameters.

        Args:
            host (str): Redis host address
            port (int): Redis port number
            db (int): Redis database number
        """
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        
        # Load the telemetry configuration
        self.config = self._load_telemetry_config()
        
    def _load_telemetry_config(self) -> Dict[str, Any]:
        """Load the telemetry configuration from the JSON file."""
        with open('telemetry_config.json', 'r') as f:
            return json.load(f)
    
    def get_latest_data(self) -> Optional[pd.DataFrame]:
        """Retrieve the latest telemetry data from Redis.

        Returns:
            Optional[pd.DataFrame]: DataFrame containing the latest telemetry data,
                                  or None if no data is available
        """
        try:
            # Attempt to get the latest data from Redis
            data = self.redis_client.get('telemetry_data')
            if data is None:
                return None
            
            # Convert the Redis data back to DataFrame
            df = pd.read_json(data)
            return df
            
        except Exception as e:
            print(f"Error reading from Redis: {e}")
            return None
    
    def get_data_range(self, start_time: int, end_time: int) -> Optional[pd.DataFrame]:
        """Retrieve telemetry data for a specific time range.

        Args:
            start_time (int): Start timestamp in Unix milliseconds
            end_time (int): End timestamp in Unix milliseconds

        Returns:
            Optional[pd.DataFrame]: DataFrame containing the telemetry data for the specified range,
                                  or None if no data is available
        """
        try:
            # Attempt to get the time-range data from Redis
            data = self.redis_client.get(f'telemetry_data:{start_time}:{end_time}')
            if data is None:
                return None
            
            # Convert the Redis data back to DataFrame
            df = pd.read_json(data)
            return df
            
        except Exception as e:
            print(f"Error reading from Redis: {e}")
            return None

    def get_variable_metadata(self, variable_name: str) -> Optional[Dict]:
        """Get metadata for a specific telemetry variable.

        Args:
            variable_name (str): Name of the telemetry variable

        Returns:
            Optional[Dict]: Dictionary containing variable metadata or None if not found
        """
        return self.config.get(variable_name)
