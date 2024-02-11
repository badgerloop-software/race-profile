def split_file_by_headers(input_file_path):
    start_letter = ord('A')  # Starting ASCII code for 'A'
    current_file = None
    file_open = False
    file_count = 0  # Keep track of how many files are created
    
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            if line.startswith("type"):
                if file_open:
                    current_file.close()
                    print(f"Finished writing to {current_file.name}")
                file_name = f"ASC2022_{chr(start_letter)}_Dirty.txt"
                current_file = open(file_name, 'w')
                file_open = True
                start_letter += 1
                file_count += 1
                print(f"Started writing to {file_name}")
            if file_open:
                current_file.write(line)
        
        # Close the last file if it's open
        if file_open:
            current_file.close()
            print(f"Finished writing to {current_file.name}")
    
    if file_count == 0:
        print("No sections starting with 'type' found. No files were created.")
    else:
        print(f"Total files created: {file_count}")

# Example usage
input_file_path = 'C:\\Users\\26790\\Documents\\1classes\\badgerloop\\race-profile\\simulink\\elevation data\\ASC2022_FullRoute.txt'
split_file_by_headers(input_file_path)
