#!/usr/bin/python

from pad4pi import rpi_gpio
import time
import sys
#import threading
#import gevent.monkey; gevent.monkey.patch_thread()

global length,check
check = False
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [27, 22, 23, 24] # BCM numbering
COL_PINS = [4,17,18] # BCM numbering

# makes assumptions about keypad layout and GPIO pin numbers


entered_passcode = ""
correct_passcode = "1234"

def cleanup():
    global keypad
    keypad.cleanup()
    return

def correct_passcode_entered():
    print("correct")
    cleanup()
    return

def incorrect_passcode_entered():
    print("ghhd")
    cleanup()
    return

def digit_entered(key):
    global entered_passcode, correct_passcode,length,check
    entered_passcode += str(key)
    print(entered_passcode)
    #print("length")
    #print(length)
    
    if len(entered_passcode) == length:
        check = True
        print("done")
        correct_passcode_entered()

def non_digit_entered(key):
    global entered_passcode

    if key == "*" and len(entered_passcode) > 0:
        entered_passcode = entered_passcode[:-1]
        print(entered_passcode)
    return

def key_pressed(key):
    try:
        
        int_key = int(key)
        print(key)
        if int_key >= 0 and int_key <= 9:
            digit_entered(key)
        return
    except ValueError:
        non_digit_entered(key)

def keypadCall(l):
    try:
        global length,check,entered_passcode,keypad
        length = l
        check=False
        #print("hey")
        factory = rpi_gpio.KeypadFactory()
        keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and GPIO pin numbers
        keypad.registerKeyPressHandler(key_pressed)

        #print("Enter your passcode (hint: {0}).".format(correct_passcode))
        #print("Press * to clear previous digit.")

        while True:
            if check:
                value = entered_passcode
                entered_passcode=""
                break
            time.sleep(1)
        return value
    except KeyboardInterrupt:
        print("Goodbye")
    finally:
        pass