import csv
import time

"""
Uses logged data to simulate the car.
Data originates from the CSV file 'coasts2024-04-141655.csv'
"""

def read_csv_data(filename):
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip header row if present
        next(csv_reader, None)
        
        for row in csv_reader:
            # Process each row here
            yield row

def start_generator(speed: int):
    for row in read_csv_data('solar_car_telemetry/src/dataProcess/testData/sliced_data.csv'):
        print(row)
        time.sleep(speed)

start_generator(1)