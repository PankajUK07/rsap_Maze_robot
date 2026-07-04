import sys

sys.path.append("/usr/lib/python3/dist-packages")

import lgpio

# Motor Pins
IN1 = 17
IN2 = 27
IN3 = 22
IN4 = 23

ENA = 12
ENB = 13


class Motors:

    def __init__(self):

        self.h = lgpio.gpiochip_open(0)

        # Claim all pins
        for pin in [IN1, IN2, IN3, IN4, ENA, ENB]:
            lgpio.gpio_claim_output(self.h, pin)

        # Make sure everything is OFF initially
        self.stop()

    def forward(self, speed=50):

        lgpio.gpio_write(self.h, IN1, 1)
        lgpio.gpio_write(self.h, IN2, 0)

        lgpio.gpio_write(self.h, IN3, 1)
        lgpio.gpio_write(self.h, IN4, 0)

        lgpio.tx_pwm(self.h, ENA, 1000, speed)
        lgpio.tx_pwm(self.h, ENB, 1000, speed)

    def backward(self, speed=50):

        lgpio.gpio_write(self.h, IN1, 0)
        lgpio.gpio_write(self.h, IN2, 1)

        lgpio.gpio_write(self.h, IN3, 0)
        lgpio.gpio_write(self.h, IN4, 1)

        lgpio.tx_pwm(self.h, ENA, 1000, speed)
        lgpio.tx_pwm(self.h, ENB, 1000, speed)

    def left(self, speed=75):

        lgpio.gpio_write(self.h, IN1, 0)
        lgpio.gpio_write(self.h, IN2, 1)

        lgpio.gpio_write(self.h, IN3, 1)
        lgpio.gpio_write(self.h, IN4, 0)

        lgpio.tx_pwm(self.h, ENA, 1000, speed)
        lgpio.tx_pwm(self.h, ENB, 1000, speed)

    def right(self, speed=75):

        lgpio.gpio_write(self.h, IN1, 1)
        lgpio.gpio_write(self.h, IN2, 0)

        lgpio.gpio_write(self.h, IN3, 0)
        lgpio.gpio_write(self.h, IN4, 1)

        lgpio.tx_pwm(self.h, ENA, 1000, speed)
        lgpio.tx_pwm(self.h, ENB, 1000, speed)

    def stop(self):

        # Stop PWM safely
        lgpio.tx_pwm(self.h, ENA, 1000, 0)
        lgpio.tx_pwm(self.h, ENB, 1000, 0)

        # Force enable pins LOW
        lgpio.gpio_write(self.h, ENA, 0)
        lgpio.gpio_write(self.h, ENB, 0)

        # Direction pins LOW
        lgpio.gpio_write(self.h, IN1, 0)
        lgpio.gpio_write(self.h, IN2, 0)
        lgpio.gpio_write(self.h, IN3, 0)
        lgpio.gpio_write(self.h, IN4, 0)

    def cleanup(self):

        self.stop()

        lgpio.gpiochip_close(self.h)