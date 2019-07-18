#!/usr/bin/env python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from time import sleep
import json
import sys
from gpiozero import InputDevice
from packages.dht11 import dht11
# import pdb

# A random programmatic shadow client ID.
SHADOW_CLIENT = "myShadowClient2"

# The unique hostname that &IoT; generated for
# this device.
HOST_NAME = "a2yfgt4hfda289-ats.iot.us-east-2.amazonaws.com"

# The relative path to the correct root CA file for &IoT;,
# which you have already saved onto this device.
ROOT_CA = "./aws/AmazonRootCA1.pem"

# The relative path to your private key file that
# &IoT; generated for this device, which you
# have already saved onto this device.
PRIVATE_KEY = "./aws/e3146f33fd-private.pem.key"

# The relative path to your certificate file that
# &IoT; generated for this device, which you
# have already saved onto this device.
CERT_FILE = "./aws/e3146f33fd-certificate.pem.crt"

# A programmatic shadow handler name prefix.
SHADOW_HANDLER = "MyRPi"


def myShadowUpdateCallback(payload, responseStatus, token):
    # Automatically called whenever the shadow is updated.
    print()
    print('UPDATE: $aws/things/' + SHADOW_HANDLER +
          '/shadow/update/#')
    print("payload = " + payload)
    print("responseStatus = " + responseStatus)
    print("token = " + token)
    #myShadowClient.disconnect()


# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY, CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
    SHADOW_HANDLER, True)

# get plant name from ARGV
# plant name should correspond to plant in db
plant_name = sys.argv[1] or "default_plant"

# setup devices
moisture_sensor = InputDevice(4)
temp_humidity_sensor = dht11.DHT11(pin=23)

def log(report_data):
    print()
    print("Water sensor: ", report_data["moisture"])
    print("Humidity %: ", report_data["humidity"])
    print("Temperature C: ", report_data["temperature"])


def update_iot_shadow(report_data):
    # data format for AWS IoT
    data = {
        "state": {
            "reported": report_data
        }
    }

    # update IoT shadow
    try:
        myDeviceShadow.shadowUpdate(json.dumps(data), myShadowUpdateCallback, 5)
    except:
        print("AWS update error")

valid_reading = False

while valid_reading != True:
    temp_humidity_value = temp_humidity_sensor.read()

    # prevent bad readings? this might be a wiring issue...
    if (temp_humidity_value.temperature > 0):
        valid_reading = True

        aws_log_timer = 0
        report_data = {
            "plant": plant_name,
            "temperature": temp_humidity_value.temperature,
            "humidity": temp_humidity_value.humidity,
            "moisture": moisture_sensor.value
        }

        # Logging
        log(report_data)

        # update IoT
        update_iot_shadow(report_data)
