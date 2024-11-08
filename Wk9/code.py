import os, sys, io
import M5
from M5 import *
import time
from hardware import *
import m5utils

# Initialize M5 device
M5.begin()

# Configure parameters
acceleration_threshold = 1.1  # Acceleration threshold; below this value, the device is considered stationary
stationary_time_limit = 5000  # Stationary time limit in milliseconds (e.g., 5 seconds)
start_stationary_time = None  # Time when stationary state begins
stationary = False  # Flag indicating whether the device is in a stationary state

# LED trigger timer
last_b_trigger_time = time.ticks_ms()  # Time since last "b" trigger

# Configure RGB LED strip
rgb_strip = RGB(io=38, n=30, type="SK6812")  # Set up LED strip with 30 LEDs on pin 38
rgb_strip.fill_color(0x000000)  # Initialize with all LEDs off

while True:
    M5.update()
    
    # Get acceleration data
    imu_data = Imu.getAccel()
    acc_x, acc_y, acc_z = imu_data
    
    # Calculate the magnitude of the acceleration vector
    total_acceleration = (acc_x ** 2 + acc_y ** 2 + acc_z ** 2) ** 0.5
    
    # Check if the device is in a stationary state
    if total_acceleration < acceleration_threshold:
        if not stationary:  # First detection of stationary state
            start_stationary_time = time.ticks_ms()
            stationary = True
        else:
            # Calculate stationary duration
            elapsed_time = time.ticks_ms() - start_stationary_time
            if elapsed_time > stationary_time_limit:
                # Stationary duration exceeds limit; trigger drowning alert
                print("Drowning!")
                rgb_strip.fill_color(0xFF0000)  # Set all LEDs to red
                print('b')  # Send "b" for ProtoPie to trigger interaction
                last_b_trigger_time = time.ticks_ms()  # Reset timer for "b"
    else:
        # Movement detected; reset state
        stationary = False
        rgb_strip.fill_color(0x000000)  # Turn off all LEDs

    # Check if screen button was pressed
    if BtnA.wasPressed():
        rgb_strip.fill_color(0xFF0000)  # Set all LEDs to red
        print('b')  # Send "b" for ProtoPie to trigger interaction
        last_b_trigger_time = time.ticks_ms()  # Reset timer for "b"

    # Check if 5 seconds have passed without triggering "b"
    if time.ticks_ms() - last_b_trigger_time > 5000:
        print('a')  # Trigger "a" if no "b" has been triggered for 5 seconds
        last_b_trigger_time = time.ticks_ms()  # Reset timer after "a" trigger

    # Small delay to avoid excessive processing load
    time.sleep_ms(100)
