#!/usr/bin/python3

# TODO
# Author:
#  - Hoanh An (hoanhan@bennington.edu)
#  - Luka Pandza (lukapandza@bennington.edu)
# Date: 04/02/2019
#

import RPi.GPIO as GPIO
import smbus
import time

# TOF configs
TOF_DEVICE_ADDRESS = 0x29

# LED 7-segment configs
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

def configure_tof(my_bus):
    """Configure the TOF settings when it starts up"""
    # my_bus.write_i2c_block_data(TOF_DEVICE_ADDRESS, 0xFF, [0xFF])
    my_bus.write_i2c_block_data(TOF_DEVICE_ADDRESS, 0xC0, [0xFF])

def write_tof(my_bus):
    return my_bus.read_i2c_block_data(TOF_DEVICE_ADDRESS, 0xFF)

def configure_led(my_bus):
    """Configure the 7-segment settings when it starts up"""
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x2F, [0xFF]) # system setup
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x89, [0xFF]) # display on

def display_led(my_bus, temp):
    """Based on the given temperature, display the value on the 7-segment"""
    # if the temperature is 0, display all 0
    if temp == 0:
        write_led(my_bus, num_map['0'], num_map['0.'], num_map['0'], num_map['0'])
        return

    # if temp < 10, meaning it follows the format x.yz, display 0x.yz
    if temp < 10:
        # get the first 4 digits in string
        str_temp = str(temp)[:4]
        d0 = str_temp[0]
        d1 = str_temp[1]
        d2 = str_temp[2]
        d3 = str_temp[3]

        write_led(my_bus, num_map['0'], num_map[d0 + d1], num_map[d2], num_map[d3])
    else:
        # get the first 5 digits in string
        str_temp = str(temp)[:5]
        d0 = str_temp[0]
        d1 = str_temp[1]
        d2 = str_temp[2]
        d3 = str_temp[3]
        d4 = str_temp[4]

        write_led(my_bus, num_map[d0], num_map[d1 + d2], num_map[d3], num_map[d4])

def write_led(my_bus, d0, d1, d2, d3):
    """Write the 4 digit value to the 7-segment display"""
    data = [d0, 0x00, d1, 0x00, 0x00, 0x00, d2, 0x00, d3, 0x00]
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x00, data)

if __name__== "__main__":
    # create bus objects
    led_bus = smbus.SMBus(1)
    tof_bus = smbus.SMBus(1)

    # configure bus
    configure_led(led_bus)
    configure_tof(tof_bus)

    while True:
        read = write_tof(tof_bus)
        print(read)

        time.sleep(1)
