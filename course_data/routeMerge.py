import pandas as pd
import os

def merge_csv_files(csv_files):
    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()
    last_distance = 0  # Keep track of the last distance from the previous file

    for file in csv_files:
        # Read the current CSV file
        current_data = pd.read_csv(file)
        
        # Check if the DataFrame is not empty
        if not current_data.empty:
            # Adjust distances for all rows except for the first CSV file
            if not merged_data.empty:
                current_data.iloc[:, 0] += last_distance
            
            # Update the last_distance to be the last entry of the current file's distance
            last_distance = current_data.iloc[-1, 0]
            
            # Concatenate the current data to the merged data
            merged_data = pd.concat([merged_data, current_data], ignore_index=True)
    
    # Define the output file name
    output_file = 'merged_route_data.csv'
    
    # Save the merged data to a new CSV file
    merged_data.to_csv(output_file, index=False)
    
    # Get the absolute path of the output file
    output_path = os.path.abspath(output_file)
    print(f"Merged data saved to {output_path}")

# List of CSV files to merge - replace these with your actual file paths or names
csv_files = ['ASC2022_A.csv', 'ASC2022_B.csv', 'ASC2022_C.csv','ASC2022_D.csv','ASC2022_E.csv','ASC2022_F.csv','ASC2022_G.csv','ASC2022_H.csv']  # Add as many as needed

merge_csv_files(csv_files)
