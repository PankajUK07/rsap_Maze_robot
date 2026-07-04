import board
import busio
import adafruit_tcs34725

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)

sensor.integration_time = 100
sensor.gain = 4


def get_values():
    r, g, b, c = sensor.color_raw
    return r, g, b, c


def is_black():

    r, g, b, c = get_values()

    # Black tile
    if c < 60:
        return True

    return False


def is_blue():

    r, g, b, c = get_values()

    total = r + g + b

    if total == 0:
        return False

    b_percent = (b / total) * 100

    # Current blue sample ≈ 28%
    if c > 80 and 26 <= b_percent <= 35:
        return True

    return False


def is_silver():

    r, g, b, c = get_values()

    # Silver is brightest
    if c > 165:
        return True

    return False