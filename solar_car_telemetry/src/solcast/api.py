import requests
import csv
from dotenv import load_dotenv
import os
import pandas as pd

"""
    The CSV columns should include (as observed in output.csv):

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

def get_weather_data(latitude = -33.86882, longitude = 151.209295, hours=168):
    """
    Fetches Solcast data using the "estimated_actuals" endpoint and writes the CSV output.

    Parameters:
        latitude (float): The desired latitude, default -33.86882 (Sydney Opera Hourse).
        longitude (float): The desired longitude, default 151.209295 (Sydney Opera House).
        hours (int): Number of hours to retrieve, default 168 (7 days).

    Returns:
        None. Writes data to output1.csv in the same directory as api.py.
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

    response = requests.request("GET", url, headers=headers, data=payload)

    # Check the status code of the response
    print(f"Status code: {response.status_code}")

    # Print status message
    print(f"Status message: {error_codes[response.status_code]}")

    # Check the response text
    print(f"Response text: {response.text}")

    # Split the text into lines
    lines = response.text.strip().split('\n')

    # Write the lines to a CSV file
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