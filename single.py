#!/usr/bin/python3

# single.py - single long range test
# Date: 04/18/2019

import smbus
import time

from registers_map import *

def write_byte(bus, reg, data):
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

def read_byte(bus, reg):
    read = bus.read_byte_data(VL53L0X_DEFAULT_ADDRESS, reg)
    print("\tget", hex(read), "from", hex(reg))

    return read

def make_uint16(lsb, msb):
    return (msb << 8) + lsb

def data_init(bus):
    print("data init")

    # set I2C standard mode
    write_byte(bus, 0x88, 0x00)

    # read who am i
    read_byte(bus, 0xC0)

    # TODO - set parameters 

    # use internal default setting
    write_byte(bus, 0x80, 0x01)
    write_byte(bus, 0xFF, 0x01)
    write_byte(bus, 0x00, 0x00)

    read_byte(bus, 0x91)

    write_byte(bus, 0x00, 0x01)
    write_byte(bus, 0xFF, 0x00)
    write_byte(bus, 0x80, 0x00)

    # TODO: enable/disable checks
    # TODO: limit default values

    write_byte(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0xFF)

def static_init(bus):
    print("static init")

    write_byte(bus, 0xFF, 0x01)
    read_byte(bus, 0x84)
    write_byte(bus, 0xFF, 0x00)

def perform_ref_calibration(bus):
    print("perfrom ref calibration")

    print("perfrom vhv calibration")

    # run vhv
    write_byte(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0x01)

    print(">> perform single ref calibration")
    print(">> perform ref calibration io")
    print(">> restore previous sequnce config")

    # >> perform single ref calibration
    write_byte(
        bus,
        VL53L0X_REG_SYSRANGE_START,
        VL53L0X_REG_SYSRANGE_MODE_START_STOP)

    # >>> measurement poll for completion
    # >>> get measurement data ready
    read_byte(bus, VL53L0X_REG_RESULT_RANGE_STATUS)

    # >>>
    write_byte(bus, VL53L0X_REG_SYSRANGE_START, 0x00)

    # >> read vhv from device
    write_byte(bus, 0xFF, 0x01)
    write_byte(bus, 0x00, 0x00)
    write_byte(bus, 0xFF, 0x00)

    read_byte(bus, 0xCB)

    # TODO perform phase calibartion

    print("> perfrom phase calibration")
    print("> restore previous sequence config")

    # >> restore prev sequence config
    write_byte(bus, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, 0x00)

def perform_ref_spad_management(bus):
    print("perform ref spad management")

    write_byte(bus, 0xFF, 0x01)
    write_byte(bus, VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00)
    write_byte(bus, VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C)
    write_byte(bus, 0xFF, 0x00)
    write_byte(bus, VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT, 0xB4)
    write_byte(bus, VL53L0X_REG_POWER_MANAGEMENT_GO1_POWER_FORCE, 0)

    # FIXME perform ref calibartion again
    # FIXME perform ref signal measurement

def perform_single_ranging_measurement(bus):
    print("perform single ranging measurement")

    # perform single measurement
    print("start measurement")
    write_byte(bus, 0x80, 0x01)
    write_byte(bus, 0xFF, 0x01)
    write_byte(bus, 0x00, 0x00)

    read_byte(bus, 0x91)

    write_byte(bus, 0x00, 0x01)
    write_byte(bus, 0xFF, 0x00)
    write_byte(bus, 0x80, 0x00)

    # device mode single ranging
    write_byte(bus, VL53L0X_REG_SYSRANGE_START, 0x01)

    # wait until start bit has been cleared
    start_stop_byte = VL53L0X_REG_SYSRANGE_MODE_START_STOP
    tmp_byte = start_stop_byte
    max_loop = 2000
    loop_nb = 0

    while ((tmp_byte & start_stop_byte) == start_stop_byte) and (loop_nb <
            max_loop):
        if loop_nb > 0:
            tmp_byte = read_byte(bus, VL53L0X_REG_SYSRANGE_START)

        loop_nb += 1

    print("measurement poll for completion")

    print("get measurement data")
    sysrange_status_reg = read_byte(bus, VL53L0X_REG_RESULT_RANGE_STATUS)
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
            "\trange_millimeter:", range_millimeter,
            "signal rate:", hex(signal_rate),
            "ambient rate:", hex(ambient_rate),
            "effective spad rtn count:", hex(effective_spad_rtn_count),
            "device range status:", hex(device_range_status))

if __name__== "__main__":
    # create a bus object
    bus = smbus.SMBus(1)

    data_init(bus)

    static_init(bus)

    perform_ref_calibration(bus)

    perform_ref_spad_management(bus)

    # set_device_mode(bus)

    # set_limit_check_enabled(bus)

    # set_limit_check_value(bus)

    # set_measurement_timing_buget_microseconds(bus)

    # set_vcse_ilse_period(bus)

    perform_single_ranging_measurement(bus)



