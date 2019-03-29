#!/usr/bin/python3

# lab03.py
# Author: Hoanh An (hoanhan@bennington.edu)
# Date: 03/17/2019
#

import RPi.GPIO as GPIO
import smbus
import time

# ADC configs
DEVICE_ADDRESS = 0x48
CONFIG_REGISTER = 0x01
CONVERSION_REGISTER = 0x00
CONFIG_BYTES = [0xC2, 0x83]

# LED 7-segment configs
LED_DEVICE_ADDRESS = 0x70

# blinking time
short_rest = 0.1
long_rest = 0.5

def configure_adc(my_bus):
    my_bus.write_i2c_block_data(DEVICE_ADDRESS, CONFIG_REGISTER, CONFIG_BYTES)

def configure_led(my_bus):
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x2F, [0xFF]) # system setup
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x89, [0xFF]) # display on

def write(my_bus, data):
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x00, data)


def display(my_bus, d0, d1, d2, d3):
    data = [d0, 0x00, d1, 0x00, 0x00, 0x00, d2, 0x00, d3, 0x00]
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x00, data)

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
    # GPIO.setmode(GPIO.BOARD)

    # setup output pin
    # output_pin = 11
    # GPIO.setup(output_pin, GPIO.OUT)

    # create a bus object
    bus = smbus.SMBus(1)

    # configure adc
    configure_adc(bus)

    # get raw adc reading
    read = get_raw_adc_reading(bus)

    # convert adc raw reading to voltage
    vol = convert_adc_read_to_voltage(read)

    # convert voltage to temperature
    temp = convert_voltage_to_temp(vol)

    # create a led bus object
    led_bus = smbus.SMBus(1)

    # configure led bus
    configure_led(led_bus)

    # display the temperature on the led screen
    str_temp = str(temp)[:4]
    print("temp:", str_temp)

    d0 = str_temp[0]
    d1 = str_temp[1]
    d2 = str_temp[2]
    d3 = str_temp[3]

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

    # either in x.yz or xy.z format
    if d1 == ".":
        display(led_bus, num_map['0'], num_map[d0 + '.'], num_map[d2], num_map[d3])
    elif d2 == ".":
        display(led_bus, num_map[d0], num_map[d1 + '.'], num_map[d2], num_map['0'])
