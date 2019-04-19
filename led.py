#!/usr/bin/python3

# led.py - experiment with vl53l0x tof sensor
# Date: 04/18/2019

import time

LED_DEVICE_ADDRESS = 0x70

# map number to led corresponding hex value
num_map = {
        "0" : 0x3F,
        "0.": 0xBF,
        "1" : 0x06,
        "1.": 0x86,
        "2" : 0x5B,
        "2.": 0xDB,
        "3" : 0x4F,
        "3.": 0xCF,
        "4" : 0x66,
        "4.": 0xE6,
        "5" : 0x6D,
        "5.": 0xED,
        "6" : 0x7D,
        "6.": 0xFD,
        "7" : 0x07,
        "7.": 0xA7,
        "8" : 0x7F,
        "8.": 0xFF,
        "9" : 0x6F,
        "9.": 0xEF
}

def configure_led(my_bus):
    """Configure the 7-segment settings when it starts up"""
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x2F, [0xFF]) # system setup
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x89, [0xFF]) # display on

def display_led(my_bus, num):
    """Based on the given int number, display the value on the 7-segment"""
    if num < 0:
        write_led(my_bus, num_map['0'], num_map['0'], num_map['0'], num_map['0'])
    elif 0 <= num <= 9:
        write_led(my_bus, num_map['0'], num_map['0'], num_map['0'], num_map[str(num)])
    elif 10 <= num <= 99:
        str_num = str(num)[:2]
        write_led(my_bus, num_map['0'], num_map['0'], num_map[str_num[0]], num_map[str_num[1]])
    elif 100 <= num <= 999:
        str_num = str(num)[:3]
        write_led(my_bus, num_map['0'], num_map[str_num[0]], num_map[str_num[1]], num_map[str_num[2]])
    else:
        str_num = str(num)[:4]
        write_led(my_bus, num_map[str_num[0]], num_map[str_num[1]], num_map[str_num[2]], num_map[str_num[3]])

def write_led(my_bus, d0, d1, d2, d3):
    """Write the 4 digit value to the 7-segment display"""
    data = [d0, 0x00, d1, 0x00, 0x00, 0x00, d2, 0x00, d3, 0x00]

    try:
        my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x00, data)
    except IOError:
        t = 0.1
        print("got IOError. try again in", t, "second")
        time.sleep(t)
