import os, sys, io
import M5
from M5 import *
from hardware import *
import time
import random

# 初始化M5板
M5.begin()

# 配置pin 8作为输出，连接到灯泡
output_pin = Pin(8, mode=Pin.OUT)

# 配置pin 7作为输入，连接到开关，并使用上拉电阻
input_pin = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)

# 状态和时间跟踪
state = 1
button_pressed_time = 0
button_released_time = 0
long_press_detected = False


while True:  # 无限循环
    M5.update()  # 更新M5板状态
    
    current_time = time.ticks_ms()

    # 检测按钮按下
    if input_pin.value() == 0 and button_pressed_time == 0:
        button_pressed_time = current_time  # 记录按下时间

    # 检测按钮释放
    if input_pin.value() == 1 and button_pressed_time != 0:
        button_released_time = current_time
        press_duration = button_released_time - button_pressed_time

        # 短按，切换状态
        if press_duration < 3000 and not long_press_detected:
            state = 2 if state == 1 else 1
        button_pressed_time = 0
        long_press_detected = False  # 重置长按标志

    # 长按检测
    if input_pin.value() == 0 and button_pressed_time != 0:
        if (current_time - button_pressed_time) > 3000:
            state = 3
            long_press_detected = True

    # 状态行为
    if state == 1:  # 不规律闪烁
        output_pin.on()   # 灯泡打开
        time.sleep_ms(random.randint(50, 200))
        output_pin.off()  # 灯泡关闭
        time.sleep_ms(random.randint(500, 2000))
    elif state == 2:  # 规律闪烁
        output_pin.on()   # 灯泡打开
        time.sleep_ms(1000)
        output_pin.off()  # 灯泡关闭
        time.sleep_ms(1000)
    elif state == 3:  # 长按保持常亮
        output_pin.on()

    # 检测长按释放后恢复到不规律闪烁
    if state == 3 and input_pin.value() == 1:
        state = 1

    time.sleep_ms(100)  # 主循环延时，防止CPU占用过高
