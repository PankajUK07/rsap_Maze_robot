from motors import Motors

from ultrasonic import (
    get_front_distance,
    get_left_distance,
    get_right_distance
)

from imu import (
    turn_left_90,
    turn_right_90,
    turn_180
)

from rgb_sensor import (
    is_black,
    is_blue,
    is_green,
    get_values
)

from indicators import (
    blue_led_on,
    blue_led_off,
    buzzer_on,
    buzzer_off,
    cleanup as indicator_cleanup
)

from time import sleep, time
import lgpio


# =========================
# Robot Initialization
# =========================

robot = Motors()

# Distance thresholds (cm)
FRONT_LIMIT = 14
SIDE_LIMIT = 18

# Speeds (%)
FORWARD_SPEED = 30
REVERSE_SPEED = 30

# Tile timings
BLUE_WAIT_TIME = 5
BLACK_BUZZ_TIME = 2

# Turn timings
TURN_ALIGN_TIME = 1.00
TURN_CLEAR_TIME = 0.80

# Anti-repeat timers
last_blue_time = 0
last_black_time = 0

# Path Memory for Return to Start
path = []
returning = False

def simplify_path(p):
    if len(p) < 3 or p[-2] != 'U':
        return
    
    m = p[-3:]
    
    if m == ['L', 'U', 'L']:
        p[-3:] = ['S']
    elif m == ['L', 'U', 'S']:
        p[-3:] = ['R']
    elif m == ['R', 'U', 'L']:
        p[-3:] = ['U']
    elif m == ['S', 'U', 'L']:
        p[-3:] = ['R']
    elif m == ['S', 'U', 'S']:
        p[-3:] = ['U']
    elif m == ['L', 'U', 'R']:
        p[-3:] = ['U']

try:
    # Setup Buttons
    START_BTN = 18
    STOP_BTN = 19
    btn_h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_input(btn_h, START_BTN, lgpio.SET_PULL_UP)
    lgpio.gpio_claim_input(btn_h, STOP_BTN, lgpio.SET_PULL_UP)

    print("\n===============================")
    print(" ROBOT READY")
    print(" PRESS START BUTTON TO BEGIN")
    print("===============================\n")
    
    # Wait for START button
    while lgpio.gpio_read(btn_h, START_BTN) == 1:
        sleep(0.01)

    print("\nStarting in 1 second...")
    sleep(1)

    while True:

        # Check for STOP button
        if lgpio.gpio_read(btn_h, STOP_BTN) == 0:
            print("\n🛑 STOP BUTTON PRESSED!")
            raise KeyboardInterrupt

        current_time = time()
        r, g, b, c = get_values()

        # =========================
        # BLUE TILE
        # =========================

        if is_blue(r, g, b, c) and current_time - last_blue_time > 8:

            print("\n🔵 BLUE TILE DETECTED")

            last_blue_time = current_time

            robot.stop()

            blue_led_on()

            print("Waiting 5 seconds...")
            sleep(BLUE_WAIT_TIME)

            blue_led_off()

            # Move off the tile
            robot.forward(25)
            sleep(0.5)
            robot.stop()

            continue


        # =========================
        # BLACK TILE (RETURN TO START)
        # =========================

        if is_black(r, g, b, c) and current_time - last_black_time > 5:

            print("\n⚫ BLACK TILE DETECTED")

            last_black_time = current_time

            if not returning:
                print("MAZE COMPLETED! Returning to start...")
                robot.stop()
                buzzer_on()
                sleep(3)
                buzzer_off()
                
                turn_180(robot)
                returning = True
                continue



        # =========================
        # ULTRASONIC READINGS
        # =========================

        front = get_front_distance()
        left = get_left_distance()
        right = get_right_distance()


        if front == 999:
            front = 300

        if left == 999:
            left = 300

        if right == 999:
            right = 300


        print(
            f"F:{front:5.1f}  "
            f"L:{left:5.1f}  "
            f"R:{right:5.1f}  "
            f"RGB=({r},{g},{b},{c})"
        )


        can_go_straight = front > FRONT_LIMIT
        can_go_left = left > SIDE_LIMIT
        can_go_right = right > SIDE_LIMIT

        # Determine if we are at an intersection / corner
        if can_go_straight and not can_go_left and not can_go_right:
            # Normal corridor, just drive forward with path correction
            left_speed = FORWARD_SPEED
            right_speed = FORWARD_SPEED
            Kp = 0.8

            if left < 15 and right < 15:
                error = right - left 
                left_speed = FORWARD_SPEED + (error * Kp)
                right_speed = FORWARD_SPEED - (error * Kp)
            elif left < 15:
                error = 6.5 - left
                left_speed = FORWARD_SPEED + (error * Kp * 1.5)
                right_speed = FORWARD_SPEED - (error * Kp * 1.5)
            elif right < 15:
                error = right - 6.5
                left_speed = FORWARD_SPEED + (error * Kp * 1.5)
                right_speed = FORWARD_SPEED - (error * Kp * 1.5)

            left_speed = max(0, min(100, int(left_speed)))
            right_speed = max(0, min(100, int(right_speed)))
            robot.set_speeds(left_speed, right_speed)

        else:
            # We are at a junction, corner, or dead end!
            robot.stop()
            
            # If front is blocked, back up slightly to ensure we have room to turn
            if not can_go_straight:
                robot.backward(REVERSE_SPEED)
                sleep(0.20)
                robot.stop()
                sleep(0.05)
                # Re-check side sensors after backing up
                left = get_left_distance()
                right = get_right_distance()
                if left == 999: left = 300
                if right == 999: right = 300
                can_go_left = left > SIDE_LIMIT
                can_go_right = right > SIDE_LIMIT

            move = None
            
            if not returning:
                # Left priority mapping (L > S > R > U)
                if can_go_left:
                    move = 'L'
                elif can_go_straight:
                    if can_go_right:
                        move = 'S' # Junction where we choose straight
                    else:
                        move = None # Shouldn't happen, but safe fallback
                elif can_go_right:
                    move = 'R'
                else:
                    move = 'U'
            else:
                # Returning to start!
                if len(path) > 0:
                    orig_move = path.pop()
                    if orig_move == 'L': move = 'R'
                    elif orig_move == 'R': move = 'L'
                    elif orig_move == 'S': move = 'S'
                    elif orig_move == 'U': move = 'U' 
                    print(f"\nRETURNING: executing {move} (opposite of {orig_move})")
                else:
                    print("\nARRIVED AT START!")
                    robot.stop()
                    while True:
                        buzzer_on()
                        sleep(0.5)
                        buzzer_off()
                        sleep(0.5)

            if move is not None:
                # 1. Alignment Phase
                # Drive forward slightly to center the wheels in the intersection before turning
                if can_go_straight and move != 'U':
                    robot.set_speeds(FORWARD_SPEED, FORWARD_SPEED)
                    sleep(TURN_ALIGN_TIME)
                    robot.stop()
                
                # 2. Memory Phase
                if not returning:
                    path.append(move)
                    simplify_path(path)
                    print(f"\nPath Memory: {path}")

                # 3. Execution Phase
                if move == 'L':
                    print("TURN LEFT")
                    turn_left_90(robot)
                elif move == 'R':
                    print("TURN RIGHT")
                    turn_right_90(robot)
                elif move == 'U':
                    print("TURN AROUND")
                    turn_180(robot)
                elif move == 'S':
                    print("GO STRAIGHT")
                
                # 4. Clearing Phase
                # Drive forward a bit to clear the intersection so side sensors don't re-trigger
                if move != 'U':
                    robot.set_speeds(FORWARD_SPEED, FORWARD_SPEED)
                    sleep(TURN_CLEAR_TIME)
                    robot.stop()

        sleep(0.01)

except KeyboardInterrupt:

    print("\nStopping Robot...")

    robot.stop()
    robot.cleanup()

    indicator_cleanup()
    
    try:
        lgpio.gpiochip_close(btn_h)
    except NameError:
        pass # In case it failed before initialization

    print("Robot Stopped Successfully")