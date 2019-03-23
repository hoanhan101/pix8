#!/usr/bin/python3

# lab03.py
# Author: Hoanh An (hoanhan@bennington.edu)
# Date: 03/17/2019
#

import RPi.GPIO as GPIO
import smbus
import time

DEVICE_ADDRESS = 0x48
CONFIG_REGISTER = 0x01
CONVERSION_REGISTER = 0x00
CONFIG_BYTES = [0xC2, 0x83]

# blinking time
short_rest = 0.1
long_rest = 0.5

def configure_adc(my_bus):
    my_bus.write_i2c_block_data(DEVICE_ADDRESS, CONFIG_REGISTER, CONFIG_BYTES)

def get_raw_adc_reading(my_bus):
    read = my_bus.read_i2c_block_data(DEVICE_ADDRESS, CONVERSION_REGISTER)

    # combine MSB and LSB to a single meaningful value and return it
    return (read[0] << 8 ) + read[1]

def convert_adc_read_to_voltage(read):
    # return (read * 3.3 * 10 ** 3) / (2 ** 16)
    # return ((65512 - read) / (65512 - 32767)) * 5
    if read > 32767:
        return ((65512 - read) / (65512 - 32767)) * -5
    else:
        return read / 32767 * 5

def convert_voltage_to_temp(voltage):
    # return absolute value of the coversion
    return abs((voltage - 500) / 10)

def two_complement(read):
    return (10 ** 16) - bin(read)

def get_blink_sequence(temp):
    return bin(int(temp))[2:]

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(short_rest)
    GPIO.output(pin, GPIO.LOW)

def blink_in_sequence(pin, seq):
    for i in seq:
        if i == '1':
            blink(pin)
        else:
            time.sleep(short_rest)
        time.sleep(long_rest)

if __name__== "__main__":
    # set board mode
    GPIO.setmode(GPIO.BOARD)

    # setup output pin
    # output_pin = 11
    # GPIO.setup(output_pin, GPIO.OUT)

    # create a bus object
    bus = smbus.SMBus(1)

    # configure adc
    configure_adc(bus)

    # get raw adc reading
    read = get_raw_adc_reading(bus)
    print("adc reading is:", hex(read), "in hex,", read, "in decimal")

    vol = convert_adc_read_to_voltage(read)
    print("voltage is:", vol)

    # c_degree = (0.0003 * vol * vol) - (0.0675 * vol) + 3.7257
    # c_degree = -3 * 10 ** -8 * vol ** 4 + 6 * 10 ** -6
    # c_degree = (0.0003 * vol * vol) - (0.0675 * vol) + 2
    # c_degree = (5 * (10 ** -10) * (vol ** 5)) - (2 * (10 ** -7) * (vol ** 4)) + (2 * (10 ** -5) * (vol ** 3)) - (0.0007 * (vol ** 2)) - (0.0484 * vol + 3.6453)
    c_degree = 53.2 + (-9.07*x) + (-1.43*(x**2))
    print("temp is:", c_degree)
