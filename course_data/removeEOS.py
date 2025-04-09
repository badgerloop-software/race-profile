import os

# Set the directory paths and the search/replace strings
original_directory = 'F:/Code/Badgerloop/race-profile/course_data/ASC_2024/ASC2024GPX'
modified_directory = 'F:/Code/Badgerloop/race-profile/course_data/ASC_2024/ASC2024ModdedGPX'
search_text = '    </trkseg>\n    <trkseg>\n      '
replace_text = '      '

# Create the modified directory if it doesn't exist
if not os.path.exists(modified_directory):
    os.makedirs(modified_directory)

# Walk through the original directory and replace text in GPX files
for root, dirs, files in os.walk(original_directory):
    for file in files:
        if file.endswith('.gpx'):  # Only process GPX files
            file_path = os.path.join(root, file)
            modified_file_path = os.path.join(modified_directory, file)  # New file path

            try:
                with open(file_path, 'r') as f:
                    file_contents = f.read()
                    new_contents = file_contents.replace(search_text, replace_text)
                    
                with open(modified_file_path, 'w') as f:
                    f.write(new_contents)
                    
                print(f"Processed file: {file_path}")

            except Exception as e:
                print(f"Failed to process file: {file_path}. Error: {e}")
