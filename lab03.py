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

bus = smbus.SMBus(1)
config_bytes = [0x84,0x83]

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(pin, GPIO.LOW)

def blink_in_sequence(pin, seq):
    for i in seq:
        if i == '1':
            blink(pin)
        else:
            time.sleep(0.1)
        time.sleep(0.5)

if __name__== "__main__":
    # set board mode
    GPIO.setmode(GPIO.BOARD)
    print(GPIO.getmode())

    # setup output pin
    output_pin = 11
    GPIO.setup(output_pin, GPIO.OUT)

    # configure adc
    bus.write_i2c_block_data(DEVICE_ADDRESS, CONFIG_REGISTER, config_bytes)

    # read
    read = bus.read_i2c_block_data(DEVICE_ADDRESS, CONVERSION_REGISTER)
    print(read[0],read[1])

    # combie these using bitwise operation
    MSB = read[0] << 8
    RAW = MSB + read[1]
    print(RAW, hex(RAW))

    # calculate the voltage
    vol = (RAW * 3.3 * 10 ** 3) / (2 ** 16)
    print(vol)

    # temp
    temp = (vol - 500) / 10

    # why is it negative?
    print(abs(temp))

    # seq = '10111'
    seq = bin(int(abs(temp)))[2:]
    print(seq)
    blink_in_sequence(output_pin, seq)

    GPIO.cleanup()
