import requests
import csv
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.solcast.com.au/data/live/radiation_and_weather?latitude=43.073051&longitude=-89.401230&period=PT5M&output_parameters=air_temp,surface_pressure,relative_humidity,dni,cloud_opacity,wind_speed_10m,azimuth,zenith&format=csv&api_key=" + api_key

payload = {}
headers = {
  'Authorization': 'Bearer ' + api_key,
  'Cookie': 'ss-id=8SElFVj7tRQB6MOFSib5; ss-opt=temp; ss-pid=GiNtGf5t9YWQ7wztBvMZ'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Check the status code of the response
print(f"Status code: {response.status_code}")

# Check the response text
print(f"Response text: {response.text}")

# Split the text into lines
lines = response.text.strip().split('\n')

# Write the lines to a CSV file
try:
    with open('output.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for line in lines:
            # Write the entire line to the CSV
            csvwriter.writerow([line])
except Exception as e:
    print(f"Error writing to file: {e}")