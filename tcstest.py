import board
import busio
import adafruit_tcs34725
import time

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensor
sensor = adafruit_tcs34725.TCS34725(i2c)

# Better stability
sensor.integration_time = 100
sensor.gain = 4

print("TCS34725 Test Started...\n")
print("Place different tiles under the sensor.\n")

try:

    while True:

        # Raw values
        r, g, b, c = sensor.color_raw

        print("----------------------------")
        print(f"R: {r}")
        print(f"G: {g}")
        print(f"B: {b}")
        print(f"Clear: {c}")

        # Color percentages
        total = r + g + b

        if total > 0:

            r_percent = (r / total) * 100
            g_percent = (g / total) * 100
            b_percent = (b / total) * 100

            print(f"R%: {r_percent:.1f}%")
            print(f"G%: {g_percent:.1f}%")
            print(f"B%: {b_percent:.1f}%")

        time.sleep(1)

except KeyboardInterrupt:

    print("\nTest Stopped")