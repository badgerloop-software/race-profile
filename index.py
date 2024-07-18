import pandas as pd
import os
# Specify the directory path
directory_path = 'course_data/ASC_2024'

# Get a list of all CSV files in the directory
all_files = [f for f in os.listdir(directory_path) if f.startswith("ASC_2024_") and f.endswith(".csv")]

# Initialize a list to store DataFrames
dfs = []

# Loop through the list of files
for file in all_files:
    # Read the file into a DataFrame
    data = pd.read_csv(os.path.join(directory_path, file))

    # Append this data to the list of DataFrames
    dfs.append(data)

# Concatenate all the dataframes in the list into a single DataFrame
df = pd.concat(dfs)
df = df[['latitude', 'longitude']]
# Now df contains all the data
df.to_csv('compiled_data.csv', index=False)