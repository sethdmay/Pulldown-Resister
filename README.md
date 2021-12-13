# Pulldown Resister: An Automatic Face Mask Raiser
_developed by Seth May_

## Executive Summary
Due to the COVID-19 Pandemic, it is in the interest of public health that people wear face masks or coverings inside to
reduce the spread of the virus. 
Sometimes people forget to pull their mask off their chin when they go inside. They might also be physically unable to do
so, either due to a disability or because their hands are filled.
I propose the Pulldown Resister, a device that automatically detects when a person goes inside and pulls up their mask.
This device improves mask adherence in public, while also offering an aid to those whom it may be difficult to manually
raise their mask

## Visual Story

The general visual story can be found [in the images folder](images/visualstory.pdf).

## Components Used

| Component                                        | Function                       | Link                                  |
|--------------------------------------------------|--------------------------------|---------------------------------------|
| Adafruit Feather M4 Express - Featuring ATSAMD51 | Microcontroller/The Brain      | https://www.adafruit.com/product/3857 |
| Adafruit AMG8833 IR Thermal Camera Breakout      | Temperature Sensor             | https://www.adafruit.com/product/3538 |
| Adafruit LTR390 UV Light Sensor                  | UV Light Sensor                | https://www.adafruit.com/product/4831 |
| Maxbotix Ultrasonic Rangefinder - LV-EZ0         | Distance Sensor                | https://www.adafruit.com/product/979  |
| Micro Servo - MG90D High Torque Metal Gear       | Actuation of Mask              | https://www.adafruit.com/product/1143 |
| Adafruit Wii Nunchuck Breakout Adapter           | Interface Nunchuck with Device | https://www.adafruit.com/product/4836 |
| Wii Nunchuck                                     | Manual Control                 | Many sources exist                    |
| Many 3D Printed Parts (Translucent Blue PLA)     | Structure                      | [See CAD Folder for STEP files](CAD)  |

## Implementation

### Overview

There are 2 main parts of the device: the mask actuator and the sensor housing. 

The mask actuator consists of a non-moving back piece, which attaches to the moving front piece via 2 hinges. Each side has a different hinge, since 1 of them accommodates the servo.
The front piece can be attached to the joints via tape or glue, and the motor can be attached to the join similarly. The joint
with the motor fits into the back piece as more of an interference fit to ease removal of the whole device from the head. 

The sensor housing consists of a main box with a cover. The box has space to hold a breadboard with all the components and sensors, shown below.
There are also cutouts to accomodate a Micro USB cable for the Feather M4 and the Nunchuck plug. At one end of the box there are
holes for string, a chain, or some other necklace-type item to wear the box.

### Hardware

For indoor/outdoor detection I used the LTR390. Based on some experiments, I found that the sensor gave a non-zero reading of UV light in full
sunlight, in shade, and in cloudy weather. Inside, even by windows, there was no UV light detected, with the exception of when the sensor was
near older incandescent light bulbs. Since many lightbulbs are now LED, this is not a pressing issue.

For person detection I used the AMG8833 combined with the LV-EZ0 to detect if there was (a) a warm mass - likely a person - in the field of
view and (b) if there was an object within ~6 feet. If both (a) and (b) were true, the device decides there is a person within 6 feet and
the mask should be raised. One shortcoming of this methodology is that heaters like radiators or heat lamps also fulfill this criteria,
although radiators are unlikely to be outside.

I used a Wii Nunchuck and the Adafruit breakout board for testing of the mechanism, and for some demonstration purposes. This method of device
actuation could have uses for people who can't raise their arms or have other limited mobility.

For actuation of the mask, I used the Micro Servo, which was attached to the main moving piece of the mechanism. It rotated on the joint between
the moving and stationary piece, which rotated the whole mechnaism, and had sufficient torque to do so.

### Software

The code is written in CircuitPython, specifically version 7.0.0 for the Adafruit Feather M4 Express, but the code could likely work on any
dev board that supports CircuitPython, has sufficient flash memory for the libraries, supports I2C, and has 1 pin of PWM. The most up to date
[libraries](https://circuitpython.org/libraries) and firmware can be found at
the [CircuitPython website](https://circuitpython.org/board/feather_m4_express/).

The code is all in [code.py](code.py).

### CAD

The STEP files in the [CAD](CAD/) folder are enough to 3D print all of the mechanisms. 1 of each STEP file should be printed for a full assembly.
Additionally, the .f3d and.f3z files can be used in Autodesk Fusion 360 and probably imported into other CAD software if you want to edit
anything.

## Pictures

![CAD of the Breadboard Box](/images/Breadboard_Box_Render.png)
_CAD of the Breadboard and Sensor Housing_

![actual breadboard box](/images/breadboard_box.jpeg)
_Actual Breadboard and Sensor Housing_

![person wearing device](/images/device_in_use.jpeg)
_Device being put on by user_

![CAD of the mask mechanism](/images/Full_Joint.png)
_CAD of the mask actuator, the moving piece is on the left while the stationary piece is on the right_

![alt text](/images/mask_mechanism.jpeg)
_The real mask actuator, showing the motor at the bottom, and where the mask would go on the right._
_Here, the stationary piece is on the left and the moving piece is on the right_
## Post Mortem

1. The most complicated subsystem to get working was the actual mechanism that raised and lowered the mask. I limited myself to primarily
   raising the mask, since you wouldn't want a scenario where a sensor malfunctions and the mask lowers itself when it shouldn't. The mechanism
   can do up and down, but it's better tuned to raising the mask. Even so, the mask is very loose across the face, and I had to use a modified 
   mask of 2 masks put together so it doesn't get stuck. An optimal system would likely need to move the nose brace in a non-circular path, in order to clear both the nose and chin.
2. Ultrasonic sensors can a bit finicky, especially when working with people and a sensor mounted on a mobile platform (another person). In
   hindsight, a camera with computer vision may work better to identify people (although some CV algorithms have bias issues).
3. 3D Printing is really great and useful for being able to quickly make good prototype and even production-level parts, but it can be slow. For
   some of my prototyping, making a mockup out of cardboard or foamboard may have helped figure out some of the actuation issues. 3D printing is
   still really useful since you can mockup the design in CAD and perfectly reproduce that with a 3D printer rather than by hand.

## Further Notes

Project for CompE 395 @ Northwestern w/ Josiah Hester

Code is written in CircuitPython for an Adafruit Feather M4 Express  
Specific Feather M4 Express and libraries included are for CircuitPython 7.0.0  
Most up to date [libraries](https://circuitpython.org/libraries) and firmware can be found at the [CircuitPython website](https://circuitpython.org/board/feather_m4_express/)
