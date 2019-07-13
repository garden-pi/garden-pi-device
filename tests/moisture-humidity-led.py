from gpiozero import LED, InputDevice
from packages.dht11 import dht11
import time

green_led = LED(17)
red_led = LED(22)
moisture_sensor = InputDevice(4)
temp_humidity_sensor = dht11.DHT11(pin=23)

def on_moist():
	green_led.on()
	red_led.off()

def on_dry():
	green_led.off()
	red_led.on()

while True:
	temp_humidity_value = temp_humidity_sensor.read()
	# prevent false negatives? might be a wiring issue...
	if (temp_humidity_value.temperature > 0):
		print("Water sensor: ", moisture_sensor.value)
		print("Humidity: ", temp_humidity_value.temperature)
		print("Temperature: ", temp_humidity_value.humidity)
		if moisture_sensor.value == 1:
			on_moist()
		else:
			on_dry()
		time.sleep(1)
