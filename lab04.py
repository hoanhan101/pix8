#!/usr/bin/python3

# lab04.py - 7-segment display
# Author:
#  - Hoanh An (hoanhan@bennington.edu)
#  - Luka Pandza (lukapandza@bennington.edu)
# Date: 03/29/2019
#

import RPi.GPIO as GPIO
import smbus
import time

# adc configs
DEVICE_ADDRESS = 0x48
CONFIG_REGISTER = 0x01
CONVERSION_REGISTER = 0x00
CONFIG_BYTES = [0xC2, 0x83]

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

def configure_adc(my_bus):
    """Configure the adc settings when it starts up"""
    my_bus.write_i2c_block_data(DEVICE_ADDRESS, CONFIG_REGISTER, CONFIG_BYTES)

def configure_led(my_bus):
    """Configure the 7-segment settings when it starts up"""
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x2F, [0xFF]) # system setup
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x89, [0xFF]) # display on

def display_led(my_bus, temp):
    """Based on the given temperature, display the value on the 7-segment"""
    # if the temperature is 0, display all 0
    if temp == 0:
        write_led(my_bus, num_map['0'], num_map['0.'], num_map['0'], num_map['0'])
        return

    # if temp < 10, meaning it follows the format x.yz, display 0x.yz
    if temp < 10:
        # get the first 4 digits in string
        str_temp = str(temp)[:4]
        d0 = str_temp[0]
        d1 = str_temp[1]
        d2 = str_temp[2]
        d3 = str_temp[3]

        write_led(my_bus, num_map['0'], num_map[d0 + d1], num_map[d2], num_map[d3])
    else:
        # get the first 5 digits in string
        str_temp = str(temp)[:5]
        d0 = str_temp[0]
        d1 = str_temp[1]
        d2 = str_temp[2]
        d3 = str_temp[3]
        d4 = str_temp[4]

        write_led(my_bus, num_map[d0], num_map[d1 + d2], num_map[d3], num_map[d4])

def write_led(my_bus, d0, d1, d2, d3):
    """Write the 4 digit value to the 7-segment display"""
    data = [d0, 0x00, d1, 0x00, 0x00, 0x00, d2, 0x00, d3, 0x00]
    my_bus.write_i2c_block_data(LED_DEVICE_ADDRESS, 0x00, data)

def get_raw_adc_reading(my_bus):
    """Get the raw adc reading"""
    read = my_bus.read_i2c_block_data(DEVICE_ADDRESS, CONVERSION_REGISTER)

    # combine MSB and LSB to a single meaningful value and return it
    return (read[0] << 8 ) + read[1]

def convert_adc_read_to_voltage(read):
    """Convert the adc reading to voltage"""
    if read > 32767:
        return ((65512 - read) / (65512 - 32767)) * -5
    else:
        return read / 32767 * 5

def convert_voltage_to_temp(voltage):
    """Convert the voltage to temperature in C degree.

    Based on the calibration plot, we only make two piecewise functions
    in this case, ranging from 0 to 38 degree in C. The rest are not
    that neccessary since we won't be able to test it anyway.
    """
    temp = 0
    if 2.71644162 < voltage < 3.697916667:
        temp = 53.2 + (-9.07*voltage) + (-1.43*(voltage**2))
    elif 1.67168326 < voltage < 2.65974766:
        temp = 78.8 + (-27.8*voltage) + (2*(voltage**2))

    return temp

if __name__== "__main__":
    # create bus objects
    adc_bus = smbus.SMBus(1)
    led_bus = smbus.SMBus(1)

    # configure bus
    configure_adc(adc_bus)
    configure_led(led_bus)

    while True:
        # get raw adc reading
        read = get_raw_adc_reading(adc_bus)

        # convert adc raw reading to voltage
        vol = convert_adc_read_to_voltage(read)
        print("vol:", vol)

        # convert voltage to temperature
        temp = convert_voltage_to_temp(vol)
        print("temp:", str(temp)[:5])

        # display temperature on the led screen
        display_led(led_bus, temp)

        # update every 5s
        time.sleep(5)
