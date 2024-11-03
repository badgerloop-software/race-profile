# Telemetry to MATLAB Integration Guide

## Introduction

Hey team! This guide will walk you through how to get telemetry data from our solar race car into MATLAB for analysis. Whether you're working on vehicle dynamics, power systems, or just want to analyze race performance, this guide has you covered.

## Project Structure

```
telemetry_matlab_integration/
├── src/
│   ├── telemetry/
│   │   ├── __init__.py
│   │   ├── reader.py          # Data fetching from Redis
│   │   ├── converter.py       # Data conversion utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validation.py      # Data validation
│   │   └── formatting.py      # Data formatting
│   └── config/
│       ├── __init__.py
│       └── settings.py        # Configuration
├── tests/
│   ├── test_reader.py
│   ├── test_converter.py
│   └── test_validation.py
├── examples/
│   ├── basic_usage.py
│   └── analysis_example.m
└── docs/
    └── telemetry_matlab_integration.md
```

## Complete Implementation Guide

### 1. Configuration (src/config/settings.py)

```python
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None

@dataclass
class TelemetryConfig:
    redis: RedisConfig
    sampling_rate: int = 1000  # ms
    batch_size: int = 1000     # records
    timeout: int = 30          # seconds

# Parameter definitions with units and valid ranges
TELEMETRY_PARAMETERS: Dict[str, Dict] = {
    'vehicle_speed': {
        'unit': 'mph',
        'min_value': 0,
        'max_value': 100,
        'aggregation': 'AVG'
    },
    'pack_voltage': {
        'unit': 'V',
        'min_value': 0,
        'max_value': 150,
        'aggregation': 'AVG'
    },
    # Add more parameters...
}
```

### 2. Custom Exceptions (src/telemetry/exceptions.py)

```python
class TelemetryError(Exception):
    """Base exception for telemetry operations"""
    pass

class ConnectionError(TelemetryError):
    """Redis connection errors"""
    pass

class ValidationError(TelemetryError):
    """Data validation errors"""
    pass

class ConversionError(TelemetryError):
    """Data conversion errors"""
    pass
```

### 3. Data Validation (src/utils/validation.py)

```python
from typing import Any, Dict, List, Optional
from ..telemetry.exceptions import ValidationError
from ..config.settings import TELEMETRY_PARAMETERS

class DataValidator:
    @staticmethod
    def validate_timestamp(timestamp: int) -> bool:
        """Validate timestamp is reasonable"""
        current_time = time.time() * 1000
        return 0 <= timestamp <= current_time

    @staticmethod
    def validate_parameter(name: str, value: float) -> bool:
        """Validate parameter value against defined ranges"""
        if name not in TELEMETRY_PARAMETERS:
            raise ValidationError(f"Unknown parameter: {name}")
            
        param_config = TELEMETRY_PARAMETERS[name]
        return param_config['min_value'] <= value <= param_config['max_value']

    @classmethod
    def validate_dataset(cls, data: Dict[str, List[float]]) -> bool:
        """Validate entire dataset"""
        try:
            for param_name, values in data.items():
                if param_name == 'timestamps':
                    valid = all(cls.validate_timestamp(t) for t in values)
                else:
                    valid = all(cls.validate_parameter(param_name, v) 
                              for v in values)
                if not valid:
                    return False
            return True
        except Exception as e:
            raise ValidationError(f"Validation failed: {str(e)}")
```

### 4. Telemetry Reader (src/telemetry/reader.py)

```python
from typing import Dict, List, Optional, Union
import redis
import numpy as np
from datetime import datetime
from ..config.settings import TelemetryConfig
from ..utils.validation import DataValidator
from .exceptions import ConnectionError, ValidationError

class TelemetryReader:
    def __init__(self, config: TelemetryConfig):
        self.config = config
        self.validator = DataValidator()
        self._connect()

    def _connect(self) -> None:
        """Establish Redis connection"""
        try:
            self.redis = redis.StrictRedis(
                host=self.config.redis.host,
                port=self.config.redis.port,
                db=self.config.redis.db,
                password=self.config.redis.password,
                decode_responses=True
            )
            self.redis.ping()  # Test connection
        except redis.RedisError as e:
            raise ConnectionError(f"Redis connection failed: {str(e)}")

    async def get_latest_values(
        self, 
        parameters: List[str]
    ) -> Dict[str, float]:
        """Fetch latest values for specified parameters"""
        try:
            result = {}
            for param in parameters:
                data = self.redis.execute_command('TS.GET', param)
                result[param] = float(data[1])
            return result
        except Exception as e:
            raise ConnectionError(f"Failed to fetch latest values: {str(e)}")

    async def get_historical_data(
        self,
        parameters: List[str],
        start_time: int,
        end_time: int,
        use_aggregation: bool = True,
        agg_interval: int = 1000
    ) -> Dict[str, np.ndarray]:
        """
        Fetch historical data with optional aggregation
        
        Args:
            parameters: List of parameter names to fetch
            start_time: Start timestamp (ms)
            end_time: End timestamp (ms)
            use_aggregation: Whether to use aggregation
            agg_interval: Aggregation interval in ms
            
        Returns:
            Dictionary of parameter arrays with timestamps
        """
        try:
            result = {}
            for param in parameters:
                if use_aggregation:
                    agg_type = TELEMETRY_PARAMETERS[param]['aggregation']
                    response = self.redis.execute_command(
                        'TS.RANGE', param, start_time, end_time,
                        'AGGREGATION', agg_type, agg_interval
                    )
                else:
                    response = self.redis.execute_command(
                        'TS.RANGE', param, start_time, end_time
                    )
                
                # Split timestamps and values
                timestamps, values = zip(*response)
                result['timestamps'] = np.array(timestamps)
                result[param] = np.array([float(v) for v in values])
            
            # Validate the dataset
            if not self.validator.validate_dataset(result):
                raise ValidationError("Dataset validation failed")
                
            return result
            
        except Exception as e:
            raise ConnectionError(f"Failed to fetch historical data: {str(e)}")
```

### 5. MATLAB Converter (src/telemetry/converter.py)

```python
from typing import Dict, Optional
import numpy as np
from scipy.io import savemat
from datetime import datetime
from .exceptions import ConversionError

class MatlabConverter:
    def __init__(self):
        self.supported_types = (np.ndarray, list, float, int)

    def _validate_data(self, data: Dict) -> bool:
        """Validate data is MATLAB-compatible"""
        try:
            for key, value in data.items():
                if not isinstance(value, self.supported_types):
                    return False
            return True
        except Exception:
            return False

    def _prepare_metadata(self, data: Dict) -> Dict:
        """Prepare metadata for MATLAB"""
        return {
            'creation_time': datetime.now().isoformat(),
            'parameters': list(data.keys()),
            'sampling_rate': np.diff(data['timestamps']).mean()
        }

    def convert_telemetry(
        self,
        data: Dict,
        output_file: str,
        include_metadata: bool = True
    ) -> None:
        """
        Convert telemetry data to MATLAB format
        
        Args:
            data: Dictionary of parameter arrays
            output_file: Output .mat file path
            include_metadata: Whether to include metadata
        """
        try:
            # Validate data
            if not self._validate_data(data):
                raise ConversionError("Invalid data format for MATLAB")

            # Prepare MATLAB dictionary
            matlab_dict = {}
            
            # Convert timestamps to MATLAB serial date numbers
            timestamps = data['timestamps'] / 1000  # ms to seconds
            matlab_dict['time'] = timestamps
            
            # Convert parameter data
            for param_name, param_data in data.items():
                if param_name != 'timestamps':
                    matlab_dict[param_name] = np.array(param_data)
            
            # Add metadata
            if include_metadata:
                matlab_dict['metadata'] = self._prepare_metadata(data)
            
            # Save to .mat file
            savemat(output_file, matlab_dict)
            
        except Exception as e:
            raise ConversionError(f"Failed to convert data: {str(e)}")
```

### 6. Main Integration Script (src/main.py)

```python
import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from .telemetry.reader import TelemetryReader
from .telemetry.converter import MatlabConverter
from .config.settings import TelemetryConfig, RedisConfig

async def collect_and_convert(
    parameters: List[str],
    duration_minutes: int = 60,
    output_file: str = 'telemetry.mat',
    use_aggregation: bool = True,
    agg_interval: int = 1000
) -> None:
    """
    Main function to collect telemetry data and convert to MATLAB
    
    Args:
        parameters: List of parameters to collect
        duration_minutes: Time window in minutes
        output_file: Output .mat file path
        use_aggregation: Whether to use data aggregation
        agg_interval: Aggregation interval in ms
    """
    # Initialize configuration
    config = TelemetryConfig(
        redis=RedisConfig(
            host="localhost",
            port=6379,
            db=0
        )
    )
    
    # Create reader and converter
    reader = TelemetryReader(config)
    converter = MatlabConverter()
    
    try:
        # Calculate time window
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = end_time - (duration_minutes * 60 * 1000)
        
        # Fetch data
        print(f"Fetching {len(parameters)} parameters...")
        data = await reader.get_historical_data(
            parameters=parameters,
            start_time=start_time,
            end_time=end_time,
            use_aggregation=use_aggregation,
            agg_interval=agg_interval
        )
        
        # Convert to MATLAB format
        print("Converting to MATLAB format...")
        converter.convert_telemetry(
            data=data,
            output_file=output_file,
            include_metadata=True
        )
        
        print(f"Data successfully saved to {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
```

### 7. Usage Example

```python
import asyncio
from src.main import collect_and_convert

async def main():
    # Define parameters to collect
    parameters = [
        'vehicle_speed',
        'pack_voltage',
        'pack_current',
        'battery_temp',
        'motor_temp'
    ]
    
    # Collect last 30 minutes of data
    await collect_and_convert(
        parameters=parameters,
        duration_minutes=30,
        output_file='race_data.mat',
        use_aggregation=True,
        agg_interval=1000  # 1 second intervals
    )

if __name__ == "__main__":
    asyncio.run(main())
```

### 8. MATLAB Analysis Template

```matlab
% Load the telemetry data
data = load('race_data.mat');

% Extract metadata
metadata = data.metadata;
fprintf('Data collected at: %s\n', metadata.creation_time);
fprintf('Sampling rate: %.2f ms\n', metadata.sampling_rate);

% Convert timestamps to datetime
timestamps = datetime(data.time, 'ConvertFrom', 'posixtime');

% Create analysis class
classdef TelemetryAnalysis
    properties
        data
        timestamps
    end
    
    methods
        function obj = TelemetryAnalysis(data, timestamps)
            obj.data = data;
            obj.timestamps = timestamps;
        end
        
        function energy = calculateEnergy(obj)
            % Calculate total energy consumption
            power = obj.data.pack_voltage .* obj.data.pack_current;
            energy = trapz(obj.data.time/3600, power);  % Wh
        end
        
        function plotTemperatures(obj)
            % Plot temperature data
            figure;
            plot(obj.timestamps, obj.data.battery_temp, 'r', ...
                 obj.timestamps, obj.data.motor_temp, 'b');
            title('System Temperatures');
            xlabel('Time');
            ylabel('Temperature (°C)');
            legend('Battery', 'Motor');
            grid on;
        end
        
        function stats = calculateStats(obj)
            % Calculate basic statistics
            stats.avg_speed = mean(obj.data.vehicle_speed);
            stats.max_speed = max(obj.data.vehicle_speed);
            stats.avg_power = mean(obj.data.pack_voltage .* ...
                                 obj.data.pack_current);
            stats.max_temp = max([obj.data.battery_temp; ...
                                obj.data.motor_temp]);
        end
    end
end

% Create analysis object
analysis = TelemetryAnalysis(data, timestamps);

% Perform analysis
stats = analysis.calculateStats();
energy = analysis.calculateEnergy();
analysis.plotTemperatures();

% Display results
fprintf('\nRace Statistics:\n');
fprintf('Average Speed: %.1f mph\n', stats.avg_speed);
fprintf('Maximum Speed: %.1f mph\n', stats.max_speed);
fprintf('Average Power: %.1f W\n', stats.avg_power);
fprintf('Maximum Temperature: %.1f °C\n', stats.max_temp);
fprintf('Total Energy Used: %.1f Wh\n', energy);
```

## Getting Started

1. Clone the repository and install dependencies:
```bash
git clone [repository-url]
cd telemetry_matlab_integration
pip install -r requirements.txt
```

2. Copy the configuration template and update with your settings:
```bash
cp src/config/settings.py.template src/config/settings.py
# Edit settings.py with your Redis credentials
```

3. Run the example script:
```bash
python examples/basic_usage.py
```

4. Open MATLAB and run the analysis template:
```matlab
cd examples
analysis_example
```

## Contributing

1. Create a new branch for your feature
2. Implement your changes
3. Add tests in the tests/ directory
4. Update documentation if needed
5. Submit a pull request

## Support

- Check the #telemetry-support Slack channel
- Review the example scripts
- Contact the telemetry team lead

Happy analyzing! 🚗☀️
