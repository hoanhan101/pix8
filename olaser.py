#!/usr/bin/python3

# olaser.py - experiment with vl53l0x tof sensor
# Author:
#  - Hoanh An (hoanhan@bennington.edu)
#  - Luka Pandza (lukapandza@bennington.edu)
# Date: 04/13/2019
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

if __name__== "__main__":
    # create and config led bus object
    # led_bus = smbus.SMBus(1)
    # configure_led(led_bus)
    # display_led(led_bus, 1997)

    # create a tof bus object
    tof_bus = smbus.SMBus(1)


    """data init"""
    # Set I2C standard mode
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x88, 0x00)

    # Use internal default setting
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x80, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x00, 0x00)

    print("internal default setting:", tof_bus.read_byte_data(TOF_DEVICE_ADDRESS, 0x91))

    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x00, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x00)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x80, 0x00)

    """static init"""
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x01)
    print("static init:", tof_bus.read_byte_data(TOF_DEVICE_ADDRESS, 0x84))
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x00)


    """perform ref calibration"""
    # perform vhv calibration
    reg_system_seq_config = 0x0001
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_system_seq_config, 0x01)

    # perfom phase calibration
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_system_seq_config, 0x02)

    """perform ref spad mgmt"""
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x01)

    reg_dynamic_spad_ref_end_start_offset = 0x4F
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_dynamic_spad_ref_end_start_offset, 0x01)

    reg_dynamic_spad_num_requested_ref_spad = 0x4E
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_dynamic_spad_num_requested_ref_spad, 0x2C)

    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x00)

    reg_dynamic_spad_num_requested_ref_spad = 0xB6
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_dynamic_spad_num_requested_ref_spad, 0xB4)

    reg_power_mgmt_g01_power_force = 0x80
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_power_mgmt_g01_power_force, 0)

    # perform ref calibration again?

    # perform ref signal measurement
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_system_seq_config, 0xC0)

    # perform single ranging measurement
    # start measurement
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x80, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x00, 0x00)

    print("internal default setting:", tof_bus.read_byte_data(TOF_DEVICE_ADDRESS, 0x91))

    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x00, 0x01)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x00)
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0x80, 0x00)

    # single ranging mode
    reg_sysrange_start = 0x000
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_sysrange_start, 0x01)

    reg_sysrange_mode_start_stop = 0x01
    print("single ranging mode:", tof_bus.read_byte_data(TOF_DEVICE_ADDRESS, reg_sysrange_mode_start_stop))

    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x01)

    """setup continuous ranging mode"""
    tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, reg_sysrange_start, 0x02)

    # print("continuous ranging mode:", tof_bus.read_byte_data(TOF_DEVICE_ADDRESS, 0x14))
    print("continuous ranging mode:", tof_bus.read_block_data(TOF_DEVICE_ADDRESS, 0x14))

    print("read from write", tof_bus.write_byte_data(TOF_DEVICE_ADDRESS, 0xFF, 0x00))

    """try best accuracy mode"""
