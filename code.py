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

UPPER = 0.095
LOWER = 0.05
UV_THRES = 0.1
DIST_THRES = 7600


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
duty_cycle = UPPER

# temp
cycles = 0
running_average = [0,0,0,0,0]

state_buffer = 0
detect = False

while True:
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

    # if detect:
    #     # we think theres a person
    #     if ultra.value > DIST_THRES:
    #         state_buffer += 1
    #         if state_buffer >= 8:
    #             detect = False
    #             state_buffer = 0
    #             # kit.servo[0].angle = 90
    #     else:
    #         state_buffer = max(0,state_buffer-1)
    # else:
    #     # currently no one nearby
    #     if ultra.value < DIST_THRES:
    #         state_buffer += 1
    #         if state_buffer >= 8:
    #             detect = True
    #             state_buffer = 0
    #             # kit.servo[0].angle = 0
    #     else:
    #         state_buffer = max(0,state_buffer-1)

    uv = ltr.uvs
    if duty_cycle == UPPER:
        if uv <= UV_THRES:
            cycles += 1
            if cycles > 8:
                duty_cycle = LOWER
                cycles = 0
        else:
            cycles = 0
    else:
        if uv >= UV_THRES:
            cycles += 1
            if cycles > 8:
                duty_cycle = UPPER
                cycles = 0
        else:
            cycles = 0

    print(uv)

    # if cycles > 8:
    #     duty_cycle = LOWER


    mtr.duty_cycle = map_duty(duty_cycle)
    print(mtr.duty_cycle, " --- dc: ", duty_cycle)



    # running_average = running_average[1:5]
    # running_average.append(top_5_avg(amg.pixels))
    # print(running_average)

    # if sum(running_average)/5 < 21.5:
    #     npix.fill(0x00FF00)
    # else:
    #     npix.fill(0xFF0000)

    if duty_cycle == LOWER:
        npix.fill(0xFF0000)
    else:
        npix.fill(0x00FF00)

    print

    # npix.brightness = min(1.0, max(0.01,1.0 - (ultra.value/8800)))


    print("**" if detect else "  ", ultra.value, ranger(ultra.value))
    time.sleep(0.05)




