#!/usr/bin/python3

# tof.py - experiment with vl53l0x tof sensor
# Date: 04/18/2019

import smbus
import time

# TOF configs
TOF_DEVICE_ADDRESS = 0x29

def write_tof(bus, reg, data):
    print("write ", hex(data), "to  ", hex(reg))
    bus.write_byte_data(TOF_DEVICE_ADDRESS, reg, data)

    time.sleep(0.1)

    read_back(bus, reg)

def read_back(bus, reg):
    read = bus.read_byte_data(TOF_DEVICE_ADDRESS, reg)
    print("return", hex(read), "from", hex(reg))

if __name__== "__main__":
    # create a bus object
    bus = smbus.SMBus(1)

    # configure_led(led_bus)
    # display_led(led_bus, 1997)

    print("=== data init ===")
    # Set I2C standard mode
    write_tof(bus, 0x88, 0x00)

    # Use internal default setting
    write_tof(bus, 0x80, 0x01)
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)

    read_back(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    print("=== static init ===")
    write_tof(bus, 0xFF, 0x01)
    read_back(bus, 0x84)
    write_tof(bus, 0xFF, 0x00)

    print("=== perfrom ref calibration ===")
