from rgb_sensor import *
import time

print("RGB TEST STARTED...\n")

try:

    while True:

        r, g, b, c = get_values()

        print(f"R:{r} G:{g} B:{b} C:{c}")

        if is_black(r, g, b, c):

            print("⚫ BLACK TILE")

        elif is_blue(r, g, b, c):

            print("🔵 BLUE TILE")

        elif is_green(r, g, b, c):

            print("🟩 GREEN TILE")

        else:

            print("⬜ NORMAL TILE")

        print("------------------------")

        time.sleep(1)

except KeyboardInterrupt:

    print("\nTest Stopped")