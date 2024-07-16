import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('TestDataAnalysis\\coastDownAnalysis\\ReynoldsNum\\combined_data_with_air_params.csv')

# Define constants
characteristic_length = 5.0  # Assume 5 meters as characteristic length for a car

# Calculate Reynolds number
# Convert density from g/m^3 to kg/m^3 by dividing by 1000
df['Reynolds_number'] = (df.iloc[:, 1] * characteristic_length * (df.iloc[:, 5] / 1000)) / df.iloc[:, 6]

# Save the results
df.to_csv('TestDataAnalysis\\coastDownAnalysis\\ReynoldsNum\\output_with_reynolds.csv', index=False)

print("Reynolds numbers calculated and saved to 'output_with_reynolds.csv'")