import sys
sys.path.append("/usr/lib/python3/dist-packages")

import lgpio
import time

START_BTN = 18
STOP_BTN = 19

h = lgpio.gpiochip_open(0)

lgpio.gpio_claim_input(h, START_BTN, lgpio.SET_PULL_UP)
lgpio.gpio_claim_input(h, STOP_BTN, lgpio.SET_PULL_UP)

print("Button Test Started...")

try:

    while True:

        if lgpio.gpio_read(h, START_BTN) == 0:
            print("START BUTTON PRESSED")
            time.sleep(0.3)

        if lgpio.gpio_read(h, STOP_BTN) == 0:
            print("STOP BUTTON PRESSED")
            time.sleep(0.3)

        time.sleep(0.01)

except KeyboardInterrupt:

    lgpio.gpiochip_close(h)
    print("Done")