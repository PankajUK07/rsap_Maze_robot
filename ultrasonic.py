import lgpio
import time

h = lgpio.gpiochip_open(0)

# Correct pin mapping
FRONT_TRIG, FRONT_ECHO = 5, 6
LEFT_TRIG, LEFT_ECHO   = 16, 20
RIGHT_TRIG, RIGHT_ECHO = 21, 26


for pin in [FRONT_TRIG, LEFT_TRIG, RIGHT_TRIG]:
    lgpio.gpio_claim_output(h, pin)
    lgpio.gpio_write(h, pin, 0)

for pin in [FRONT_ECHO, LEFT_ECHO, RIGHT_ECHO]:
    lgpio.gpio_claim_input(h, pin)


def get_distance(trig, echo):

    # Clear trigger
    lgpio.gpio_write(h, trig, 0)
    time.sleep(0.0002)

    # 10 µs pulse
    lgpio.gpio_write(h, trig, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(h, trig, 0)

    # Wait for echo HIGH
    timeout = time.time() + 0.05
    while lgpio.gpio_read(h, echo) == 0:
        if time.time() > timeout:
            return 999

    start = time.time()

    # Wait for echo LOW
    timeout = time.time() + 0.05
    while lgpio.gpio_read(h, echo) == 1:
        if time.time() > timeout:
            return 999

    end = time.time()

    distance = (end - start) * 34300 / 2
    return round(distance, 1)


def get_front_distance():
    return get_distance(FRONT_TRIG, FRONT_ECHO)


def get_left_distance():
    time.sleep(0.06)   # Prevent cross-talk
    return get_distance(LEFT_TRIG, LEFT_ECHO)


def get_right_distance():
    time.sleep(0.06)   # Prevent cross-talk
    return get_distance(RIGHT_TRIG, RIGHT_ECHO)


if __name__ == "__main__":

    print("3-Ultrasonic Test\n")

    while True:

        front = get_front_distance()
        left = get_left_distance()
        right = get_right_distance()

        print(
            f"Front: {front:6.1f} cm | "
            f"Left: {left:6.1f} cm | "
            f"Right: {right:6.1f} cm"
        )

        time.sleep(0.3)