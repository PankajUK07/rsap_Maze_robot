import board
import busio
import adafruit_tcs34725

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tcs34725.TCS34725(i2c)

sensor.integration_time = 24
sensor.gain = 4


def get_values():
    r, g, b, c = sensor.color_raw
    # Scale values to match the old 100ms integration thresholds
    scale = 100 / 24
    return int(r * scale), int(g * scale), int(b * scale), int(c * scale)


def is_black(r, g, b, c):
    # Black tile
    if c < 60:
        return True

    return False


def is_blue(r, g, b, c):
    total = r + g + b

    if total == 0:
        return False

    b_percent = (b / total) * 100

    # Current blue sample ≈ 28%
    if c > 80 and 26 <= b_percent <= 35:
        return True

    return False


def is_silver(r, g, b, c):
    # Silver is brightest
    if c > 165:
        return True

    return False