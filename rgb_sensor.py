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


def rgb_to_hsv(r, g, b):
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    
    if mx == 0:
        return 0, 0, 0
    
    v = mx
    s = (df / mx) * 100 if mx > 0 else 0
    
    if df == 0:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
        
    return h, s, v

def is_black(r, g, b, c):
    if c < 110:
        return True
    return False


def is_blue(r, g, b, c):
    if c < 110:
        return False
        
    h, s, v = rgb_to_hsv(r, g, b)
    
    # Blue/Cyan/Magenta hues fall between 150 and 330 degrees.
    # Floor/Normal tiles fall between 0 and 60 degrees (Orange/Yellow).
    # This is practically bulletproof against lighting changes.
    if 150 < h < 330:
        return True

    return False


def is_green(r, g, b, c):
    if c < 110:
        return False
        
    h, s, v = rgb_to_hsv(r, g, b)
    
    # Green hues fall perfectly between 70 and 140 degrees.
    if 70 < h < 140:
        return True

    return False