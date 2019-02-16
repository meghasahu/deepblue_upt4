#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import spidev
from time import sleep

# uses the "spidev" package ('sudo pip3 install spidAev')
# check dtparam=spi=on --> in /boot/config.txt or (set via 'sudo raspi-config')


def readADC_MSB():
    """
    Reads 2 bytes (byte_0 and byte_1) and converts the output code from the MSB-mode:
    byte_0 holds two ?? bits, the null bit, and the 5 MSB bits (B11-B07),
    byte_1 holds the remaning 7 MBS bits (B06-B00) and B01 from the LSB-mode, which has to be removed.
    """
    bytes_received = spi.xfer2([0x00, 0x00])

    MSB_1 = bytes_received[1]
    MSB_1 = MSB_1 >> 1  # shift right 1 bit to remove B01 from the LSB mode

    MSB_0 = bytes_received[0] & 0b00011111  # mask the 2 unknown bits and the null bit
    MSB_0 = MSB_0 << 7  # shift left 7 bits (i.e. the first MSB 5 bits of 12 bits)

    return MSB_0 + MSB_1


def readADC_LSB():
    """
    Reads 4 bytes (byte_0 - byte_3) and converts the output code from LSB format mode:
    byte 1 holds B00 (shared by MSB- and LSB-modes) and B01,
    byte_2 holds the next 8 LSB bits (B03-B09), and
    byte 3, holds the remaining 2 LSB bits (B10-B11).
    """
    bytes_received = spi.xfer2([0x00, 0x00, 0x00, 0x00])

    LSB_0 = bytes_received[1] & 0b00000011  # mask the first 6 bits from the MSB mode
    LSB_0 = bin(LSB_0)[2:].zfill(2)  # converts to binary, cuts the "0b", include leading 0s

    LSB_1 = bytes_received[2]
    LSB_1 = bin(LSB_1)[2:].zfill(8)  # see above, include leading 0s (8 digits!)

    LSB_2 = bytes_received[3]
    LSB_2 = bin(LSB_2)[2:].zfill(8)
    LSB_2 = LSB_2[0:2]  # keep the first two digits

    LSB = LSB_0 + LSB_1 + LSB_2  # concatenate the three parts to the 12-digits string
    LSB = LSB[::-1]  # invert the resulting string
    return int(LSB, base=2)

    
def convert_to_voltage(self, adc_output, VREF=3.3):
    """
    Calculates analogue voltage from the digital output code (ranging from 0-4095)
    VREF could be adjusted here (standard uses the 3V3 rail from the Rpi)
    """
    return adc_output * (VREF / (2 ** 12 - 1))
    




SPI_bus = 0
CE = 0

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 976000

def turbidity():
    ADC_output_code = readADC_MSB()
    #ADC_voltage = convert_to_voltage(ADC_output_code)
    #print("MCP3201 output code (MSB-mode): %d" % ADC_output_code)
    #print("MCP3201 voltage: %0.2f V" % ADC_voltage)
    
    sleep(0.1)  # wait minimum of 100 ms between ADC measurements
    
    ADC_output_code = readADC_LSB()
    #ADC_voltage = convert_to_voltage(ADC_output_code)
    #print("MCP3201 output code (LSB-mode): %d" % ADC_output_code)
    #print("MCP3201 voltage: %0.2f V" % ADC_voltage)
    #print(ADC_output_code)
    
    sleep(1)
    return ADC_output_code

'''except (KeyboardInterrupt):
    print('\n', "Exit on Ctrl-C: Good bye!")

except:
    print("Other error or exception occurred!")
    raise

finally:
    print()
'''
while 1:
    print(turbidity())
