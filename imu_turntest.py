from motors import Motors
from imu import *

robot = Motors()

try:

    input("Press ENTER for LEFT 90...")
    turn_left_90(robot)

    input("\nPress ENTER for RIGHT 90...")
    turn_right_90(robot)

    input("\nPress ENTER for 180...")
    turn_180(robot)

except KeyboardInterrupt:

    print("\nStopping Robot...")

    robot.stop()
    robot.cleanup() 

    print("Robot Stopped")