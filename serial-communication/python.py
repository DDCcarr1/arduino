import serial                           # pip install pyserial
import time
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo           # pip install tzdata
import requests                         # pip install requests

port = 'COM3'
#port = '/dev/cu.usbserial-1420'
baud = 9600
api_url = "https://api.open-meteo.com/v1/forecast?latitude=38.8922&longitude=-77.0708&current=temperature_2m,weather_code&timezone=America%2FNew_York&timeformat=unixtime&wind_speed_unit=ms"
sample = {
  "latitude": 38.89,
  "longitude": -77.06,
  "generationtime_ms": 0.138521194458008,
  "utc_offset_seconds": -14400,
  "timezone": "America/New_York",
  "timezone_abbreviation": "GMT-4",
  "elevation": 32,
  "current_units": {
    "time": "unixtime",
    "interval": "seconds",
    "temperature_2m": "°C",
    "weather_code": "wmo code"
  },
  "current": {
    "time": 1780424100,
    "interval": 900,
    "temperature_2m": 23.8,
    "weather_code": 0
  }
}

wmo_codes = {
    "0": "Clear",
    "1": "Cloudy", "2": "Cloudy", "3": "Cloudy",
    "45": "Fog", "48": "Fog",
    "51": "Drizzle", "53": "Drizzle", "55": "Drizzle", "56": "Drizzle", "57": "Drizzle",
    "61": "Rain", "63": "Rain", "65": "Rain", "66": "Rain", "67": "Rain",
    "71": "Snow", "73": "Snow", "75": "Snow", "77": "Snow",
    "80": "Rain", "81": "Rain", "82": "Rain",
    "85": "Snow", "86": "Snow",
    "95": "Storm", "96": "Storm", "99": "Storm"
}


print("----- PROGRAM START -----\n")

try:
    print(f"Locating Arduino at {port}.")
    arduino = serial.Serial(port, baud, timeout=1)
    print(f"Arduino located at {port}. Attempting to connect...")
    time.sleep(2)
    print(f"Connected to Arduino at {port}.")

    while True:
        incoming_json = requests.get(api_url).json()

        outgoing_timestamp = time.time()

        dt = datetime.fromtimestamp(outgoing_timestamp, tz=ZoneInfo('America/New_York'))

        outgoing_dict = {
            "time": f"{dt.strftime('%Y.%m.%d %H.%M')}",
            "temp": incoming_json["current"]["temperature_2m"],
            "weather": wmo_codes[str(incoming_json["current"]["weather_code"])]
        }
        outgoing_json = json.dumps(outgoing_dict) + "\n"
        print(f"Sending JSON payload of\n{outgoing_json.strip()}\nto Arduino at {port}.")
        arduino.write(outgoing_json.encode('utf-8'))

        time.sleep(0.5)
        response_text = arduino.readline().decode('utf-8').strip()
        if response_text != "":
            print(response_text)
        else:
            print(f"Error: Timeout on Arduino at {port}.")

        print()
        time.sleep(2.5)

except Exception as error:
    print(f"Error: {error}")
finally:
    print(f"Closing connection to Arduino at {port}.")
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print(f"Closed connection to Arduino at {port}.")
    else:
        print(f"The connection to Arduino at {port} was not found.")

    print("\n----- PROGRAM COMPLETE -----")
