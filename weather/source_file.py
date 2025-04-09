import requests
import csv
url = "https://api.solcast.com.au/data/live/radiation_and_weather?latitude=43.073051&longitude=-89.401230&period=PT5M&output_parameters=air_temp,surface_pressure,relative_humidity,dni,cloud_opacity,wind_speed_10m&format=csv&api_key=7e-I4ydW4DcmcYFSE1AEfkGycWQTPQcC"

payload = {}
headers = {
  'Authorization': 'Bearer {{api_key}}',
  'Cookie': 'ss-id=8SElFVj7tRQB6MOFSib5; ss-opt=temp; ss-pid=GiNtGf5t9YWQ7wztBvMZ'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Split the text into lines
lines = response.text.strip().split('\n')

# Write the lines to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    for line in lines:
        # Strip the newline character before splitting
        line = line.strip()
        csvwriter.writerow(line.split(','))

print("CSV file saved successfully.")
with open('ASC2022_FullRoute.txt', 'r') as file:
    data = file.read()

lines = data.split('\n')
result = [[float(line.split('\t')[1]), float(line.split('\t')[2])] for line in lines if len(line.split('\t')) >= 3]
print(len(result))
with open('ASC2022_FullRoute.txt', 'r') as file:
    data = file.read()

lines = data.split('\n')
coordinates = set()
result = []
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 3:
        coord = (float(parts[1]), float(parts[2]))
        if coord not in coordinates:
            result.append(coord)
            coordinates.add(coord)

print(len(result))

with open('ASC2022_FullRoute.txt', 'r') as file:
    data = file.read()

lines = data.split('\n')
result = []
prev = None
for line in lines:
    parts = line.split('\t')
    if len(parts) >= 3:
        coord = [float(parts[1]), float(parts[2])]
        if coord != prev:
            result.append(coord)
            prev = coord

print(len(result))
# import requests
# params = "air_temp,albedo,azimuth,clearsky_dhi,clearsky_dni,clearsky_ghi,clearsky_gti,cloud_opacity,dewpoint_temp,dni,ghi,gti,precipitable_water,precipitation_rate,relative_humidity,surface_pressure,snow_depth,snow_soiling_rooftop,snow_soiling_ground,snow_water_equivalent,wind_direction_100m,wind_direction_10m,wind_speed_100m,wind_speed_10m,zenith"
#
# url = "https://api.solcast.com.au/data/historic_forecast/radiation_and_weather?latitude=43.073051&longitude=-89.401230&period=PT30M&output_parameters=" + params + "&start=2024-04-14T12:00:00.000-05:00&end=2024-04-14T20:00:00.000-05:00&format=csv&time_zone=utc&lead_time=PT1H&api_key=7e-I4ydW4DcmcYFSE1AEfkGycWQTPQcC"
#
# payload = {}
# headers = {
#   'Authorization': 'Bearer {{api_key}}',
#   'Cookie': 'ss-opt=temp; ss-pid=GiNtGf5t9YWQ7wztBvMZ'
# }
#
# response = requests.request("GET", url, headers=headers, data=payload)
#
# print(response.text)


