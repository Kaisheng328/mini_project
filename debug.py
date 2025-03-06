import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
import mpu6050

def test_leds():
    leds = [17, 27, 22]  # Red, Blue, Green
    print("Testing LEDs...")
    for led in leds:
        GPIO.output(led, 1)
        print(f"LED {led} ON")
        time.sleep(1)
        GPIO.output(led, 0)
        print(f"LED {led} OFF")
    print("LED test completed.")

def test_buttons():
    buttons = {10: "Button 1", 9: "Button 2"}
    print("Testing buttons...")
    for pin, name in buttons.items():
        state = GPIO.input(pin)
        print(f"{name} is {'PRESSED' if state == 0 else 'NOT PRESSED'}")
    print("Button test completed.")

def test_dht22():
    dht_device = adafruit_dht.DHT22(board.D18)
    print("Testing DHT22 sensor...")
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature:.2f}C, Humidity: {humidity:.2f}%")
        else:
            print("Failed to read DHT22 sensor!")
    except Exception as e:
        print(f"Error reading DHT22: {e}")
    print("DHT22 test completed.")

def test_mpu6050():
    mpu = mpu6050.mpu6050(0x68)
    print("Testing MPU6050 sensor...")
    try:
        accel_data = mpu.get_accel_data()
        gyro_data = mpu.get_gyro_data()
        print(f"Acceleration: {accel_data}")
        print(f"Gyroscope: {gyro_data}")
    except Exception as e:
        print(f"Error reading MPU6050: {e}")
    print("MPU6050 test completed.")

def run_diagnostics():
    print("Starting component verification...")
    test_leds()
    test_buttons()
    test_dht22()
    test_mpu6050()
    print("Component verification completed.")

if __name__ == "__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT, initial=0)
    GPIO.setup(27, GPIO.OUT, initial=0)
    GPIO.setup(22, GPIO.OUT, initial=0)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    run_diagnostics()
    GPIO.cleanup()
