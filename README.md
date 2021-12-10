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

## Components Used
| Component                                        | Function                       | Link                                  |
|--------------------------------------------------|--------------------------------|---------------------------------------|
| Adafruit Feather M4 Express - Featuring ATSAMD51 | Microcontroller/The Brain      | https://www.adafruit.com/product/3857 |
| Adafruit AMG8833 IR Thermal Camera Breakout      | Temperature Sensor             | https://www.adafruit.com/product/3538 |
| Adafruit LTR390 UV Light Sensor                  | UV Light Sensor                | https://www.adafruit.com/product/4831 |
| Micro Servo - MG90D High Torque Metal Gear       | Actuation of Mask              | https://www.adafruit.com/product/1143 |
| Adafruit Wii Nunchuck Breakout Adapter           | Interface Nunchuck with Device | https://www.adafruit.com/product/4836 |
| Wii Nunchuck                                     | Manual Control                 | Many sources exist                    |
| Many 3D Printed Parts (Translucent Blue PLA)     | Structure                      | See CAD Folder for STEP files         |
## Implementation
There are 2 main parts of the device: the mask actuator and the sensor housing. The mask actuator consists of a non-moving back piece, which attaches to the moving front piece via 2 hinges. Each side has a different hinge, since 1 of them accommodates the servo.
The front piece can be attached to the joints via tape or glue, and the motor can be attached to the join similarly. The joint
with the motor fits into the back piece as more of an interference fit to ease removal of the whole device from the head. The sensor housing consists of a main box with a cover. The box has space to hold a breadboard with all the components and sensors, shown below.
There are also cutouts to accomodate a Micro USB cable for the Feather M4 and the Nunchuck plug. At one end of the box there are
holes for string, a chain, or some other necklace-type item to wear the box.
## Pictures

## Post Mortem


Project for CompE 395 @ Northwestern w/ Josiah Hester

Code is written in CircuitPython for an Adafruit Feather M4 Express
Specific Feather M4 Express and libraries included are for CircuitPython 7.0.0
Most up to date [libraries](https://circuitpython.org/libraries) and firmware can be found at the [CircuitPython website](https://circuitpython.org/board/feather_m4_express/)
