"""CircuitPython Essentials: PWM with Fixed Frequency example."""
import time
import math
import board
import pwmio
import simpleio
import analogio
import adafruit_nunchuk
import adafruit_amg88xx
import adafruit_ltr390
import neopixel

UPPER = 0.095      # lowers the mask
LOWER = 0.05       # raises the mask (yes I know it's confusing)
UV_THRES = 0.1     # accounts for "noise" inside
DIST_THRES = 7600  # approx 6 ft


amg = adafruit_amg88xx.AMG88XX(board.I2C())
ltr = adafruit_ltr390.LTR390(board.I2C())


mtr = pwmio.PWMOut(board.D10, frequency=50, duty_cycle=3276)
npix = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.5)
# nc = adafruit_nunchuk.Nunchuk(board.I2C())

ultra = analogio.AnalogIn(board.A0)

def map_duty(frac):
    return int(simpleio.map_range(frac, 0, 1, 0, 65535))
# 2000 to 7700 -> 0.03 to 0.11

def top_5_avg(temps):
    temps = [item for sublist in temps for item in sublist]
    sorted_temps = sorted(temps, reverse=True)
    return sum(sorted_temps[0:5])/5

def convert_temp(temp):
    char = ""
    if temp <= 23:
        char = "."
    elif temp <= 24:
        char = "o"
    elif temp <= 26:
        char = "O"
    elif temp >= 27:
        char = "#"
    
    return char

def ranger(dist):
    out = "["
    for i in range(int(30*dist/14000)):
        out += "#"

    out += "]"

    return out

# motor
inside = False
duty_cycle = UPPER

# UV light
cycles = 0

# temp
running_average = [0,0,0,0,0]
warm = False

# distance
state_buffer = 0
detect = False


while True:
    ### NUNCHUCK
    # x, y = nc.joystick

    # incr = simpleio.map_range(y, 255, 1, -0.002, 0.002)
    # duty_cycle += incr

    # if duty_cycle < LOWER:
    #     duty_cycle = LOWER
    # elif duty_cycle > UPPER:
    #     duty_cycle = UPPER

    # if nc.buttons.C:
    #     duty_cycle = UPPER
    # elif nc.buttons.Z:
    #     duty_cycle = LOWER

    ### DISTANCE SENSOR
    if detect:
        # we think theres a person
        if ultra.value > DIST_THRES:
            state_buffer += 1
            if state_buffer >= 8:
                detect = False
                state_buffer = 0
                # kit.servo[0].angle = 90
        else:
            state_buffer = max(0,state_buffer-1)
    else:
        # currently no one nearby
        if ultra.value < DIST_THRES:
            state_buffer += 1
            if state_buffer >= 8:
                detect = True
                state_buffer = 0
                # kit.servo[0].angle = 0
        else:
            state_buffer = max(0,state_buffer-1)

    ### UV SENSOR

    uv = ltr.uvs
    if not inside:
        if uv <= UV_THRES:
            cycles += 1
            if cycles > 8:
                inside = True
                cycles = 0
        else:
            cycles = 0
    else:
        if uv >= UV_THRES:
            cycles += 1
            if cycles > 8:
                inside = False
                cycles = 0
        else:
            cycles = 0

    print(uv)

    ### IR TEMP SENSOR
    running_average = running_average[1:5]
    running_average.append(top_5_avg(amg.pixels))
    print(running_average)

    if sum(running_average)/5 < 21.5:
        # nothing warm there
        warm = False
    else:
        warm = True

    if inside:
        # Raise mask on inside
        duty_cycle = LOWER
    elif warm and detect:
        # theres something nearby that's warm, raise the mask
        duty_cycle = LOWER
    else:
        # we're outside, there's nothing warm AND near, lower the mask
        # TODO: gate this so normal operation doesn't lower mask
        duty_cycle = UPPER

    # some nice lighing stuff that shines green when mask should be down, red when up
    if duty_cycle == LOWER:
        npix.fill(0xFF0000)
    else:
        npix.fill(0x00FF00)

    ### MOTOR

    mtr.duty_cycle = map_duty(duty_cycle)
    print(mtr.duty_cycle, " --- dc: ", duty_cycle)



    print("**" if detect else "  ", ultra.value, ranger(ultra.value))
    time.sleep(0.05) # 20 Hz is the max rate of the distance sensor




