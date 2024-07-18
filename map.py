import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('compiled_data.csv')

# Convert the 'latitude' and 'longitude' columns to numeric
df['latitude'] = pd.to_numeric(df['latitude'])
df['longitude'] = pd.to_numeric(df['longitude'])

# Mirror the 'latitude' and 'longitude' values


# Create a scatter plot of the latitude and longitude points
plt.scatter(df['longitude'], df['latitude'])

# Set the title and labels for the plot
plt.title('Mirrored Latitude and Longitude Points')

# Set the tick locations for the x and y axes

# Display the plot
plt.show()