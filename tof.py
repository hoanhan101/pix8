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
        print("\t*err: got", hex(read), "instead of", hex(data),
                "when write to", hex(reg))

def read_tof(bus, reg):
    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
    print("\tget", hex(read), "from", hex(reg))

    return read

def make_uint16(lsb, msb):
    return (msb << 8) + lsb

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

    print("perform single ranging measurement")

    # perform single measurement
    print("start measurement")
    write_tof(bus, 0x80, 0x01)
    write_tof(bus, 0xFF, 0x01)
    write_tof(bus, 0x00, 0x00)

    read_tof(bus, 0x91)

    write_tof(bus, 0x00, 0x01)
    write_tof(bus, 0xFF, 0x00)
    write_tof(bus, 0x80, 0x00)

    # device mode single ranging
    write_tof(bus, VL53L0X_REG_SYSRANGE_START, 0x01)

    # wait until start bit has been cleared
    start_stop_byte = VL53L0X_REG_SYSRANGE_MODE_START_STOP
    tmp_byte = start_stop_byte
    max_loop = 2000
    loop_nb = 0

    while ((tmp_byte & start_stop_byte) == start_stop_byte) and (loop_nb <
            max_loop):
        if loop_nb > 0:
            tmp_byte = read_tof(bus, VL53L0X_REG_SYSRANGE_START)

        loop_nb += 1

    print("measurement poll for completion")

    print("get measurement data")
    sysrange_status_reg = read_tof(bus, VL53L0X_REG_RESULT_RANGE_STATUS)
    if sysrange_status_reg & 0x01:
        print("measurement data ready")

    print("get ranging measurement data")

    raw_data = bus.read_i2c_block_data(VL53L0X_DEFAULT_ADDRESS, 0x14)

    range_millimeter = make_uint16(raw_data[11], raw_data[10])
    signal_rate = make_uint16(raw_data[7], raw_data[6])
    ambient_rate = make_uint16(raw_data[9], raw_data[8])
    effective_spad_rtn_count = make_uint16(raw_data[3], raw_data[2])
    device_range_status = raw_data[0]

    print(
            "range_millimeter:", range_millimeter,
            "signal rate:", hex(signal_rate),
            "ambient rate:", hex(ambient_rate),
            "effective spad rtn count:", hex(effective_spad_rtn_count),
            "device range status:", hex(device_range_status))
