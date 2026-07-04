
from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)
GYRO_Z_BIAS = 0.2092213740458015

TURN_SPEED = 50
BRAKE_SPEED = 35

yaw = 0
last_time = time.time()


def reset_yaw():
    global yaw, last_time
    yaw = 0
    last_time = time.time()


def get_yaw():
    global yaw, last_time

    gyro = sensor.get_gyro_data()

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    gz = gyro['z'] - GYRO_Z_BIAS

    yaw += gz * dt

    return yaw


def turn_left_90(robot):

    print("\nLEFT 90")

    reset_yaw()

    robot.left(TURN_SPEED)

    while True:

        angle = get_yaw()

        if angle >= 80:
            break

        time.sleep(0.005)

    # Active brake
    robot.right(BRAKE_SPEED)
    time.sleep(0.07)

    robot.stop()
    time.sleep(0.2)

    print(f"Final Angle: {angle:.1f}")


def turn_right_90(robot):

    print("\nRIGHT 90")

    reset_yaw()

    robot.right(TURN_SPEED)

    while True:

        angle = get_yaw()

        if angle <= -80:
            break

        time.sleep(0.005)

    # Active brake
    robot.left(BRAKE_SPEED)
    time.sleep(0.07)

    robot.stop()
    time.sleep(0.2)

    print(f"Final Angle: {angle:.1f}")


def turn_180(robot):

    print("\nTURN AROUND")

    reset_yaw()

    robot.right(TURN_SPEED)

    while True:

        angle = get_yaw()

        if angle <= -170:
            break

        time.sleep(0.005)

    # Active brake
    robot.left(BRAKE_SPEED)
    time.sleep(0.1)

    robot.stop()
    time.sleep(0.2)

    print(f"Final Angle: {angle:.1f}")