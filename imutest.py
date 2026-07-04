from imu import get_yaw, reset_yaw
import time

reset_yaw()

print("MPU6050 Test Started")
print("Rotate the robot slowly...\n")

while True:

    yaw = get_yaw()

    print(f"Yaw: {yaw:.2f}°")

    time.sleep(0.05)