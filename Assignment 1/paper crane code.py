import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import random

# Initialize the M5 board
M5.begin()

# Set pin 8 as output, connected to the light bulb
output_pin = Pin(8, mode=Pin.OUT)

# Set pin 7 as input, connected to the button, using a pull-up resistor
input_pin = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

# State and time tracking
state = 1
button_pressed_time = 0
button_released_time = 0
long_press_detected = False

while True:  # Infinite loop
    M5.update()  # Update M5 board status
    
    current_time = time.ticks_ms()

    # Detect button press
    if input_pin.value() == 0 and button_pressed_time == 0:
        button_pressed_time = current_time  # Record press time

    # Detect button release
    if input_pin.value() == 1 and button_pressed_time != 0:
        button_released_time = current_time
        press_duration = button_released_time - button_pressed_time

        # Short press, toggle the state
        if press_duration < 3000 and not long_press_detected:
            state = 2 if state == 1 else 1
        button_pressed_time = 0
        long_press_detected = False  # Reset long press flag

    # Long press detection
    if input_pin.value() == 0 and button_pressed_time != 0:
        if (current_time - button_pressed_time) > 3000:
            state = 3
            long_press_detected = True

    # State behaviors
    if state == 1:  # Irregular flashing
        output_pin.on()   # Turn on the light
        time.sleep_ms(random.randint(50, 200))
        output_pin.off()  # Turn off the light
        time.sleep_ms(random.randint(500, 2000))
    elif state == 2:  # Regular flashing
        output_pin.on()   # Turn on the light
        time.sleep_ms(1000)
        output_pin.off()  # Turn off the light
        time.sleep_ms(1000)
    elif state == 3:  # Constant on when long press
        output_pin.on()

    # Detect release after long press and return to irregular flashing
    if state == 3 and input_pin.value() == 1:
        state = 1

    time.sleep_ms(100) 
