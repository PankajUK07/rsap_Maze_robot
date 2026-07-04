from motors import Motors

from ultrasonic import (
    get_front_distance,
    get_left_distance,
    get_right_distance
)

from imu import (
    turn_left_90,
    turn_right_90,
    turn_180
)

from rgb_sensor import (
    is_black,
    is_blue,
    is_silver,
    get_values
)

from indicators import (
    blue_led_on,
    blue_led_off,
    buzzer_on,
    buzzer_off,
    cleanup as indicator_cleanup
)

from time import sleep, time


# =========================
# Robot Initialization
# =========================

robot = Motors()

# Distance thresholds (cm)
FRONT_LIMIT = 18
SIDE_LIMIT = 15

# Speeds (%)
FORWARD_SPEED = 30
REVERSE_SPEED = 30

# Tile timings
BLUE_WAIT_TIME = 5
BLACK_BUZZ_TIME = 2

# Anti-repeat timers
last_blue_time = 0
last_black_time = 0


try:

    while True:

        current_time = time()
        r, g, b, c = get_values()

        # =========================
        # BLUE TILE
        # =========================

        if is_blue(r, g, b, c) and current_time - last_blue_time > 8:

            print("\n🔵 BLUE TILE DETECTED")

            last_blue_time = current_time

            robot.stop()

            blue_led_on()

            print("Waiting 5 seconds...")
            sleep(BLUE_WAIT_TIME)

            blue_led_off()

            # Move off the tile
            robot.forward(25)
            sleep(0.5)
            robot.stop()

            continue


        # =========================
        # BLACK TILE
        # =========================

        if is_black(r, g, b, c) and current_time - last_black_time > 5:

            print("\n⚫ BLACK TILE DETECTED")

            last_black_time = current_time

            robot.stop()

            buzzer_on()
            sleep(BLACK_BUZZ_TIME)
            buzzer_off()

            turn_180(robot)

            continue


        # =========================
        # SILVER TILE
        # =========================

        if is_silver(r, g, b, c):

            print("⚪ SILVER TILE DETECTED")


        # =========================
        # ULTRASONIC READINGS
        # =========================

        front = get_front_distance()
        left = get_left_distance()
        right = get_right_distance()


        if front == 999:
            front = 300

        if left == 999:
            left = 0

        if right == 999:
            right = 0


        print(
            f"F:{front:5.1f}  "
            f"L:{left:5.1f}  "
            f"R:{right:5.1f}  "
            f"RGB=({r},{g},{b},{c})"
        )


        # =========================
        # MOVE FORWARD
        # =========================

        if front > FRONT_LIMIT:

            robot.forward(FORWARD_SPEED)


        # =========================
        # WALL DETECTED
        # =========================

        else:

            print("WALL DETECTED")

            robot.stop()
            sleep(0.05)

            robot.backward(REVERSE_SPEED)
            sleep(0.10)

            robot.stop()
            sleep(0.05)


            # LEFT PRIORITY

            if left > SIDE_LIMIT:

                print("TURN LEFT")

                turn_left_90(robot)


            elif right > SIDE_LIMIT:

                print("TURN RIGHT")

                turn_right_90(robot)


            else:

                print("TURN AROUND")

                turn_180(robot)

        sleep(0.01)


except KeyboardInterrupt:

    print("\nStopping Robot...")

    robot.stop()
    robot.cleanup()

    indicator_cleanup()

    print("Robot Stopped Successfully")