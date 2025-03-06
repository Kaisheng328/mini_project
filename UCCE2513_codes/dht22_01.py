import board
import adafruit_dht

# Sensor should be set to DHT11,DHT22 or AM2302
# Select the data pin connected to the DHT22
dhtDevice = adafruit_dht.DHT22(board.D18)

# Try to grab a sensor reading.  Use the object notation method.
temp = dhtDevice.temperature
humi = dhtDevice.humidity

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
if temp is not None and humi is not None:
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, humi))
else:
    print('Failed to get reading. Try again!')

dhtDevice.exit()
