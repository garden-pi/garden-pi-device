import requests 
import time
from dotenv import load_dotenv
import os

payload = {
            "plant": "api_test",
            "temperature": 33,
            "humidity": 45,
            "moisture": 0,
            "timestamp": int(time.time())
        }

r = requests.post(
  "https://p71p6yuahb.execute-api.us-east-2.amazonaws.com/Staging/GardenPiUpdate", 
  json=payload,
  headers={'x-api-key': os.getenv("API_GATEWAY_KEY")}
)
print(r.text)