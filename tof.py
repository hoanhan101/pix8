#!/usr/bin/python3

# tof.py - experiment with vl53l0x tof sensor
# Date: 04/18/2019

import smbus
import time

from registers_map import *

def write_tof(bus, reg, data):
    """
    write to the registere address
    read back its data
    check if it's the same
    """
    bus.write_byte_data(VL53L0X_DEFAULT_ADDRESS, reg, data)

    time.sleep(0.1)

    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
    if read != data:
        print("\t*err: got", hex(read), "instead of", hex(data), "when write to", hex(reg))

def read_tof(bus, reg):
    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
    print("\tget", hex(read), "from", hex(reg))

if __name__== "__main__":
    # create a bus object
    bus = smbus.SMBus(1)

    print("data init")
    # Set I2C standard mode
    write_tof(bus, 0x88, 0x00)

    # Use internal default setting
    write_tof(bus, 0x80, 0x01)
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)

    read_tof(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    print("static init")
    write_tof(bus, 0xFF, 0x01)
    read_tof(bus, 0x84)
    write_tof(bus, 0xFF, 0x00)

    print("perfrom ref calibration")
    # > perform vhv calibartion
    write_tof(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0x01)

    # >> perform single ref calibration
    write_tof(
        bus,
        VL53L0X_REG_SYSRANGE_START,
        VL53L0X_REG_SYSRANGE_MODE_START_STOP)

    # >>> measurement poll for completion
    # >>> get measurement data ready
    read_tof(bus, VL53L0X_REG_RESULT_RANGE_STATUS)

    # >>>
    write_tof(bus, VL53L0X_REG_SYSRANGE_START, 0x00)

    # >> read vhv from device
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)
    write_tof(bus, 0xFF, 0x00)

    read_tof(bus, 0xCB)

    # TODO perform phase calibartion

    # >> restore prev sequence config
    write_tof(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0x00)

    print("perfrom ref spad mgmt")
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00)
    write_tof(bus, VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4)
    write_tof(bus, VL53L0X_REG_POWER_MANAGEMENT_GO1_POWER_FORCE, 0)

    # FIXME perform ref calibartion again
    # FIXME perform ref signal measurement

    print("start single measurement")

    write_tof(bus, 0x80, 0x01)
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)

    read_tof(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    write_tof(bus, VL53L0X_REG_SYSRANGE_START, 0x01)
    read_tof(bus, VL53L0X_REG_SYSRANGE_START)
