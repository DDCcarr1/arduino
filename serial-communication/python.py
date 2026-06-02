import serial                           # pip install pyserial
import time
import json
from datetime import datetime, timezone
from zoneinfo import ZoneInfo           # pip install tzdata

port = 'COM4'
#port = '/dev/cu.usbserial-1420'
baud = 9600
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

print("----- PROGRAM START -----\n")

try:
    print(f"Locating Arduino at {port}.")
    arduino = serial.Serial(port, baud, timeout=1)
    print(f"Arduino located at {port}. Attempting to connect...")
    time.sleep(2)
    print(f"Connected to Arduino at {port}.")

    while True:
        outgoing_timestamp = sample["current"]["time"]

        dt = datetime.fromtimestamp(outgoing_timestamp, tz=ZoneInfo('America/New_York'))

        outgoing_dict = {
            "time": f"{dt.strftime('%Y.%m.%d %H.%M')}",
            "temp": sample["current"]["temperature_2m"],
            "weather": sample["current"]["weather_code"]
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
        time.sleep(2)

except Exception as error:
    print(f"Error: {error}")
finally:
    print(f"Closing connection to Arduino at {port}.")
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Closed connection to Arduino at {port}.")
    else:
        print(f"The connection to Arduino at {port} was not found.")

    print("\n----- PROGRAM COMPLETE -----")
