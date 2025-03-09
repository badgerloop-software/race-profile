import requests, requests.exceptions
import csv
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta

"""
    The CSV columns in the response to the API request should include (as observed in output.csv):

    - **ghi (W/m2)**  
      Global Horizontal Irradiance (GHI).  
      Total irradiance on a horizontal surface. The sum of direct and diffuse irradiance components received on a horizontal surface.

    - **ebh**  
      Beam Horizontal Irradiance (EBH).  
      Beam (direct) irradiance on a horizontal surface. (Not explicitly documented by Solcast, but often interpreted similar to DNI projected onto a horizontal plane.)

    - **dni (W/m2)**  
      Direct Normal Irradiance (DNI).  
      Irradiance received from the direction of the sun. Also referred to as beam radiation.

    - **dhi (W/m2)**  
      Diffuse Horizontal Irradiance (DHI).  
      The diffuse irradiance received on a horizontal surface. Also referred to as Diffuse Sky Radiation. The diffuse component is irradiance that is scattered by the atmosphere.

    - **cloud_opacity (%)**  
      Cloud Opacity.  
      The attenuation of incoming sunlight due to cloud. Varies from 0% (no cloud) to 100% (full attenuation).

    - **period_end (datetime)**  
      End time of the measurement period in ISO8601 format (e.g., 2025-02-20T02:00:00Z).

    - **period (string)**  
      Specifies the time interval duration in ISO8601 duration format (e.g., PT30M for a 30-minute period).
"""

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "output.csv")
api_calls_path = os.path.join(current_dir, "api_request_log.csv")

def track_api_calls(status_code: int):
    """
    Helper method for get_weather_data() to keep track of sucessfull API calls within a 24 hour period. 
    Helps us understand how many requests we can send in a 24-hour time period. All values except the last
    attempted request timestamp reset after 24 hours.

    Parameters:
      status_code (int): The status code that Solcast API returns

    Returns:
      None. Writes request data to api_request_log.csv.
    """
    now = datetime.now()
    one_day_ago = now - timedelta(hours=24)

    try:
        with open(api_calls_path, 'r') as file:
            csv_reader = csv.reader(file)
            existing_data = list(csv_reader)
    except FileNotFoundError:
        print(f"Error: The file '{api_calls_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    initial_sucessfull_call = datetime.strptime(existing_data[1][0], '%Y-%m-%d %H:%M:%S.%f')
    last_attempted_request = datetime.strptime(existing_data[1][1], '%Y-%m-%d %H:%M:%S.%f')
    time_last_requested_sucessfully = datetime.strptime(existing_data[1][2], '%Y-%m-%d %H:%M:%S.%f')
    successful_calls = int(existing_data[1][3])
    calls_429 = int(existing_data[1][4])
    other_failed_calls = int(existing_data[1][5])

    # print("Before...")
    # print(f"Initial Sucessfull Call: {initial_sucessfull_call}")
    # print(f"Last Attempted Request: {last_attempted_request}")
    # print(f"Time Last Requested Sucessfully: {time_last_requested_sucessfully}")
    # print(f"Successful Calls: {successful_calls}")
    # print(f"429 Calls: {calls_429}")
    # print(f"Other failed calls: {other_failed_calls}")

    last_attempted_request = now

    if status_code == 200:
      if time_last_requested_sucessfully < one_day_ago:
        print("Resetting Initial request timestamp...")
        successful_calls = 0
        calls_429 = 0
        other_failed_calls = 0
        initial_sucessfull_call = now
        print("Reset")

      successful_calls += 1
      time_last_requested_sucessfully = now
    elif status_code == 429:
        calls_429 += 1
    else:
        other_failed_calls += 1

    # print("After...")
    # print(f"Initial Sucessfull Call: {initial_sucessfull_call}")
    # print(f"Last Attempted Request: {last_attempted_request}")
    # print(f"Time Last Requested Sucessfully: {time_last_requested_sucessfully}")
    # print(f"Successful Calls: {successful_calls}")
    # print(f"429 Calls: {calls_429}")
    # print(f"Other failed calls: {other_failed_calls}")

    data = [
    ['Initial Sucessful Call', 'Last Attempted Request', 'Time Last Requested Sucessfully' ,'Sucessful API Calls', '429 Calls', 'Other Failed Calls'],
    [initial_sucessfull_call, last_attempted_request, time_last_requested_sucessfully, successful_calls, calls_429, other_failed_calls]
    ]

    with open(api_calls_path, 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerows(data)

def get_weather_data(latitude = -33.86882, longitude = 151.209295, hours=168):
    """
    Fetches Solcast data using the "estimated_actuals" endpoint and writes the CSV output.

    Parameters:
        latitude (float): The desired latitude, default -33.86882 (Sydney Opera Hourse).
        longitude (float): The desired longitude, default 151.209295 (Sydney Opera House).
        hours (int): Number of hours to retrieve, default 168 (7 days).

    Returns:
        Response data in Pandas Dataframe and writes same data to output.csv in the same directory as api.py.
    """
    
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = (
        "https://api.solcast.com.au/world_radiation/estimated_actuals?"
        f"latitude={latitude}&"
        f"longitude={longitude}&"
        f"hours={hours}&"
        "format=csv"
    )

    payload = {}
    headers = {
      'Authorization': 'Bearer ' + api_key,
      'Cookie': 'ss-id=8SElFVj7tRQB6MOFSib5; ss-opt=temp; ss-pid=GiNtGf5t9YWQ7wztBvMZ'
    }

    error_codes = {
        200: "OK: A successful response.",
        202: "The request was accepted but does not include any data in the response. Refer to the message returned in the body of the response for more information.",
        404: "Bad Request: The request may have included invalid parameters. For more information, refer to the message returned in the response's body.",
        401: "Unauthorized: The request did not correctly include a valid API Key. Check the API Key used in the request is correct, active, and properly added to the request using one of the available authentication methods.",
        402: "Payment Required: You may have exceeded the available transaction limit or the requested endpoint is not available on your current plan. Check the response body for the exact reason.",
        403: "Forbidden: The request may include a parameter not available at your current subscription level.",
        429: "Too Many Requests: The request exceeds the available rate limit at your current subscription level.",
        500: "Internal Server Error: An internal error has prevented the request from processing."
    }

    try:
      response = requests.request("GET", url, headers=headers, data=payload)
      track_api_calls(response.status_code)
    except requests.exceptions.ConnectionError:
       print("\n Error: No internet connection or unable. Please check connection and try again.\n")
    except Exception as e:
       print(f"An error occured: {e}")

    print(f"Status code: {response.status_code}")
    print(f"Status message: {error_codes[response.status_code]}")
    print(f"Location requested: ({latitude}, {longitude}).")
    print(f"Response text:\n{response.text}")

    # Split the text into lines and write them to CSV file
    lines = response.text.strip().split('\n')
    if response.status_code == 200:
      try:
          with open(csv_path, 'w', newline='') as csvfile:
              csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=' ')
              for row in csv.reader(lines):
                  csvwriter.writerow(row)
          return pd.read_csv(csv_path)
      except Exception as e:
          print(f"Error writing to file: {e}")
    else:
        print(f"API output not saved, status code {response.status_code}.")

if __name__ == '__main__':
    get_weather_data()