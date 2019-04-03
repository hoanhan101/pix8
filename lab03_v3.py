#!/usr/bin/python3

# lab03_v3.py - blink 1 LED on the binary reading value
# Author:
# - Hoanh An (hoanhan@bennington.edu)
# - Luka Pandza (lukapandza@bennington.edu)
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
    if read > 32767:
        return ((65512 - read) / (65512 - 32767)) * -5
    else:
        return read / 32767 * 5

def convert_voltage_to_temp(voltage):
    # return temp is in C
    temp = 0
    if 2.71644162 < voltage < 3.697916667:
        temp = 53.2 + (-9.07*voltage) + (-1.43*(voltage**2))
    elif 1.67168326 < voltage < 2.65974766:
        temp = 78.8 + (-27.8*voltage) + (2*(voltage**2))

    return temp

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
    output_pin = 11
    GPIO.setup(output_pin, GPIO.OUT)

    # create a bus object
    bus = smbus.SMBus(1)

    # configure adc
    configure_adc(bus)

    while True:
        # get raw adc reading
        read = get_raw_adc_reading(bus)
        print("adc reading is:", hex(read), "in hex,", read, "in decimal")

        vol = convert_adc_read_to_voltage(read)
        print("voltage is:", vol)

        # the more precise the better
        c_degree = convert_voltage_to_temp(vol)
        print("temp is:", c_degree)

        seq = get_blink_sequence(c_degree)
        print("sequence is: ", seq)

        blink_in_sequence(output_pin, get_blink_sequence(c_degree))
