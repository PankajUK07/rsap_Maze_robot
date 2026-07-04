from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)

print("Keep the robot completely still...")
print("Calibrating for 10 seconds...\n")

samples = 1000
total = 0

for i in range(samples):

    gyro = sensor.get_gyro_data()
    total += gyro['z']

    if i % 100 == 0:
        print(f"{i}/{samples}")

    time.sleep(0.01)

bias = total / samples

print("\n====================")
print(f"GYRO_Z_BIAS = {bias}")
print("====================")