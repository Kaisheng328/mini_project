import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

import board
import adafruit_dht
import time

GPIO.setmode(GPIO.BCM)

dhtDevice = adafruit_dht.DHT22(board.D18)   #change the GPIO pin according to your connection

BLYNK_AUTH_TOKEN = 'token here' #paste your token here

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Create BlynkTimer Instance
timer = BlynkTimer()

# function to connect the Blynk cloud
@blynk.on("connected")
def blynk_connected():
    print("Hi, You have Connected to New Blynk2.0")
    time.sleep(2);
    
# Functon to send collected data to the Blynk cloud
def myData():
    temp = dhtDevice.temperature
    humi = dhtDevice.humidity
    if temp is not None and humi is not None:
        print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temp, humi))
        
        blynk.virtual_write(0, temp,)
        blynk.virtual_write(1, humi)
        print("Values sent to Blynk Server!")
    else:
        print("Sensor failure. Check wiring.");

# Set the timer to automatically call the function every 10s
timer.set_interval(10, myData)

myData()

while True:
    blynk.run()
    timer.run()
