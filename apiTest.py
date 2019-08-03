import requests
import os
import time

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_GATEWAY_KEY")
PLANT_NAME = os.getenv("PLANT_NAME")

payload = {
    "plant": PLANT_NAME,
    "temperature": 23,
    "humidity": 99,
    "moisture": 1,
    "timestamp": int(time.time())
}

r = requests.post(
    API_URL,
    json=payload,
    headers={'x-api-key': API_KEY}
)
print(r.text)
