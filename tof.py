#!/usr/bin/python3

# tof.py - experiment with vl53l0x tof sensor
# Date: 04/18/2019

import smbus
import time

# VL54L0X default address
VL53L0X_DEFAULT_ADDRESS = 0x29

# device register map
VL53L0X_REG_SYSRANGE_START = 0x000
VL53L0X_REG_SYSRANGE_MODE_MASK = 0x0F
VL53L0X_REG_SYSRANGE_MODE_START_STOP = 0x01
VL53L0X_REG_SYSRANGE_MODE_START_SINGLESHOT = 0x00

VL53L0X_REG_SYSTEM_THRESH_HIGH = 0x000C
VL53L0X_REG_SYSTEM_THRESH_LOW = 0x000E

VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG = 0x0001
VL53L0X_REG_SYSTEM_RANGE_CONFIG = 0x0009
VL53L0X_REG_SYSTEM_SYSTEM_INTERMEASUREMENT_PERIOD  = 0x0004

# result register
VL53L0X_REG_RESULT_RANGE_STATUS = 0x0014

VL53L0X_REG_RESULT_CORE_PAGE = 1
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_RTN = 0x00C0
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_REF = 0x00D4

# algo register
VL53L0X_REG_ALGO_PART_TO_PART_RANGE_OFFSET_MM = 0x0028

# check limit registers
VL53L0X_REG_MSRC_CONFIG_CONTROL = 0x0060

# pre range registers
VL53L0X_REG_GLOBAL_CONFIG_VCSEL_WIDTH = 0x032

VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT = 0xB6

VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD = 0x4E
VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET = 0x4F
VL53L0X_REG_POWER_MANAGEMENT_G01_POWER_FORCE = 0x80

def write_tof(bus, reg, data):
    # print("write ", hex(data), "to  ", hex(reg))
    bus.write_byte_data(VL53L0X_DEFAULT_ADDRESS, reg, data)

    time.sleep(0.1)

    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
    if read != data:
        print("err", hex(read), "is not the same as", hex(data))

def read_tof(bus, reg):
    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
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

    read_tof(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    print("=== static init ===")
    write_tof(bus, 0xFF, 0x01)
    read_tof(bus, 0x84)
    write_tof(bus, 0xFF, 0x00)

    print("=== perfrom ref calibration ===")
    # > perform vhv calibartion
    write_tof(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0x01)

    # >> perform single ref calibration
    write_tof(
        bus,
        VL53L0X_REG_SYSRANGE_START,
        VL53L0X_REG_SYSRANGE_MODE_START_STOP | 0x40)

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

    print("=== perfrom ref spad mgmt ===")
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00)
    write_tof(bus, VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4)
    write_tof(bus, VL53L0X_REG_POWER_MANAGEMENT_G01_POWER_FORCE, 0)

    # FIXME perform ref calibartion again
    # FIXME perform ref signal measurement

    print("=== start single measurement ===")

    write_tof(bus, 0x80, 0x01)
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)

    read_tof(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    write_tof(bus, VL53L0X_REG_SYSRANGE_START, 0x01)
    read_tof(bus, VL53L0X_REG_SYSRANGE_START)
