import lgpio
import time

# GPIO Pins
BLUE_LED = 24
BUZZER = 25

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Configure outputs
lgpio.gpio_claim_output(h, BLUE_LED)
lgpio.gpio_claim_output(h, BUZZER)

try:

    while True:

        print("BLUE LED ON")
        lgpio.gpio_write(h, BLUE_LED, 1)
        time.sleep(2)

        print("BLUE LED OFF")
        lgpio.gpio_write(h, BLUE_LED, 0)
        time.sleep(1)

        print("BUZZER ON")
        lgpio.gpio_write(h, BUZZER, 1)
        time.sleep(2)

        print("BUZZER OFF")
        lgpio.gpio_write(h, BUZZER, 0)
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping...")

    lgpio.gpio_write(h, BLUE_LED, 0)
    lgpio.gpio_write(h, BUZZER, 0)

    lgpio.gpiochip_close(h)

    print("Done")