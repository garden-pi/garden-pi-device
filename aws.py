from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import datetime, time, json
import RPi.GPIO as GPIO
from packages.dht11 import dht11

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

# Automatically called whenever the shadow is updated.
def myShadowUpdateCallback(payload, responseStatus, token):
  print()
  print('UPDATE: $aws/things/' + SHADOW_HANDLER + 
    '/shadow/update/#')
  print("payload = " + payload)
  print("responseStatus = " + responseStatus)
  print("token = " + token)

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,
  CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(
  SHADOW_HANDLER, True)

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
instance = dht11.DHT11(pin=17)

# Keep generating random test data until this script 
# stops running.
# To stop running this script, press Ctrl+C.
while True:
  result = instance.read()
  temperature = result.temperature
  humidity = result.humidity

  data = {
    "state": {
      "reported": {
	"plant": "actual_rpi",
        "temperature": temperature,
        "humidity": humidity
      }
    }
  }
  
  myDeviceShadow.shadowUpdate(
    json.dumps(data),
    myShadowUpdateCallback, 5)

  # Wait for this test value to be added.
  time.sleep(10)
