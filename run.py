#!/usr/bin/env python3
import time
import sys
import os
import requests 
from dotenv import load_dotenv
from gpiozero import InputDevice
from packages.dht11 import dht11

API_URL = "https://p71p6yuahb.execute-api.us-east-2.amazonaws.com/Staging/GardenPiUpdate"
API_KEY = os.getenv("API_GATEWAY_KEY")

# get plant name from ARGV
# plant name should correspond to plant in db
plant_name = sys.argv[1] or "default_plant"

# setup devices
moisture_sensor = InputDevice(4)
temp_humidity_sensor = dht11.DHT11(pin=23)

def log(payload):
    print()
    print("Water sensor: ", payload["moisture"])
    print("Humidity %: ", payload["humidity"])
    print("Temperature C: ", payload["temperature"])

def api_post(payload):
    try:
        r = requests.post(
          API_URL, 
          json=payload,
          headers={'x-api-key': API_KEY}
        )
        print(r.text)

        valid_reading = True
    except:
        print("AWS update error")

# loop until we get a valid reading
valid_reading = False
while valid_reading != True:
    temp_humidity_value = temp_humidity_sensor.read()

    # prevent bad readings? this might be a wiring issue...
    if (temp_humidity_value.temperature > 0):
        payload = {
            "plant": plant_name,
            "temperature": temp_humidity_value.temperature,
            "humidity": temp_humidity_value.humidity,
            "moisture": moisture_sensor.value,
            "timestamp": int(time.time())
        }

        # Logging
        log(payload)

        # post to AWS
        api_post(payload)
