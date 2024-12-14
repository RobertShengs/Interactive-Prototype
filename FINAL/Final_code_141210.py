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
stationary_time_limit = 10000  # Stationary time limit in milliseconds (e.g., 10 seconds)
heart_rate_threshold = 50  # Heart rate threshold (e.g., beats per minute)
start_stationary_time = None  # Time when stationary state begins
stationary = False  # Flag indicating whether the device is in a stationary state
last_b_trigger_time = time.ticks_ms()  # Time since last "b" trigger
led_on = False  # Flag to track LED state

# Configure RGB LED strip
rgb_strip = RGB(io=38, n=30, type="SK6812")  # Set up LED strip with 30 LEDs on pin 38
rgb_strip.fill_color(0x000000)  # Initialize with all LEDs off

# Configure pulse sensor (example: using ADC on pin 1)
pulse_sensor = ADC(Pin(1), atten=ADC.ATTN_11DB)

title0 = Widgets.Title("HeartRate", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
label0 = Widgets.Label("BPM:", 0, 20, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
label1 = Widgets.Label("LED:", 0, 40, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
label2 = Widgets.Label("---", 0, 60, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

protopie_enable = True  # Enable ProtoPie communication

def get_heart_rate():
    """Map pulse sensor raw values to heart rate (BPM)"""
    raw_value = pulse_sensor.read()  # Read raw value
    heart_rate = int(m5utils.remap(raw_value, 0, 4095, 0, 120))
    return heart_rate

while True:
    M5.update()
    
    # Get acceleration data
    imu_data = Imu.getAccel()
    acc_x, acc_y, acc_z = imu_data
    total_acceleration = (acc_x ** 2 + acc_y ** 2 + acc_z ** 2) ** 0.5

    # Get heart rate data
    heart_rate = get_heart_rate()
    print(heart_rate)
    label0.setText('BPM: ' + str(heart_rate))

    # Check heart rate threshold and send "b" if below threshold
    if heart_rate < heart_rate_threshold:
        label1.setText('LED: red')
        label2.setText('Drowning!')
        rgb_strip.fill_color(0xFF0000)  # Set all LEDs to red
        led_on = True
        if protopie_enable:
            print('b')  # Send "b" for ProtoPie
        last_b_trigger_time = time.ticks_ms()  # Reset timer after "b"
    elif heart_rate >= heart_rate_threshold and led_on:
        # Heart rate recovered, turn off LED
        label1.setText('LED: OFF')
        label2.setText('---')
        rgb_strip.fill_color(0x000000)  # Turn off all LEDs
        led_on = False

    # Check if the device is in a stationary state
    elif total_acceleration < acceleration_threshold:
        if not stationary:  # First detection of stationary state
            start_stationary_time = time.ticks_ms()
            stationary = True
        else:
            elapsed_time = time.ticks_ms() - start_stationary_time
            if elapsed_time > stationary_time_limit and not led_on:
                label2.setText('Drowning!')
                label1.setText('LED: red')
                rgb_strip.fill_color(0xFF0000)  # Set all LEDs to red
                led_on = True
                if protopie_enable:
                    print('b')  # Send "b" for ProtoPie
                last_b_trigger_time = time.ticks_ms()
    else:
        # Movement detected, turn off LED
        if stationary and led_on:
            label1.setText('LED: OFF')
            rgb_strip.fill_color(0x000000)  # Turn off all LEDs
            led_on = False
        stationary = False

    # Check if screen button was pressed
    if BtnA.wasPressed():
        rgb_strip.fill_color(0xFF0000)  # Set all LEDs to red
        led_on = True
        label1.setText('LED: red')
        if protopie_enable:
            print('b')  # Send "b" for ProtoPie
        last_b_trigger_time = time.ticks_ms()

    # Check if 5 seconds have passed without triggering "b"
    if time.ticks_ms() - last_b_trigger_time > 5000:
        if protopie_enable:
            print('a')  # Trigger "a" if no "b" has been triggered for 5 seconds
        last_b_trigger_time = time.ticks_ms()  # Reset timer after "a"

    time.sleep_ms(100)
