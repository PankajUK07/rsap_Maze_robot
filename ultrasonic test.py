from gpiozero import DistanceSensor
from time import sleep

# Create sensors
front_sensor = DistanceSensor(
    echo=6,
    trigger=5,
    max_distance=2
)

left_sensor = DistanceSensor(
    echo=20,
    trigger=16,
    max_distance=2
)

right_sensor = DistanceSensor(
    echo=26,
    trigger=21,
    max_distance=2
)

print("3-Sensor Ultrasonic Test Started")

while True:

    try:
        front = front_sensor.distance * 100
    except:
        front = -1

    try:
        left = left_sensor.distance * 100
    except:
        left = -1

    try:
        right = right_sensor.distance * 100
    except:
        right = -1

    print(
        f"Front: {front:6.1f} cm | "
        f"Left: {left:6.1f} cm | "
        f"Right: {right:6.1f} cm"
    )

    sleep(0.2)