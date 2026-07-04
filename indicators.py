import sys
sys.path.insert(0, "/usr/lib/python3/dist-packages")

import lgpio

BLUE_LED = 24
BUZZER = 25

h = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(h, BLUE_LED)
lgpio.gpio_claim_output(h, BUZZER)


def blue_led_on():
    lgpio.gpio_write(h, BLUE_LED, 1)


def blue_led_off():
    lgpio.gpio_write(h, BLUE_LED, 0)


def buzzer_on():
    lgpio.gpio_write(h, BUZZER, 1)


def buzzer_off():
    lgpio.gpio_write(h, BUZZER, 0)


def cleanup():
    blue_led_off()
    buzzer_off()
    lgpio.gpiochip_close(h)