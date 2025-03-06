import time
import mpu6050

mpu6050 = mpu6050.mpu6050(0x68) #0x68 is the i2c address

while True:
    accelerometer_data = mpu6050.get_accel_data()
    gyro_data = mpu6050.get_gyro_data()
    
    print("accelerometer data")
    print("------------------")
    print("accel_xout: ", accelerometer_data['x'])
    print("accel_yout: ", accelerometer_data['y'])
    print("accel_zout: ", accelerometer_data['z'])
    
    print("gyro data")
    print("------------------")
    print("gyro_xout: ", gyro_data['x'])
    print("gyro_youtt: ", gyro_data['y'])
    print("gyro_zout: ", gyro_data['z'])
    
    time.sleep(1)
