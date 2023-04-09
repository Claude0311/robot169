#!/usr/bin/env python3
#
#   Drive the Robot
#
import sys
import time
import qwiic_scmd

from itertools import chain


# Define the constants.
MTR_NUM_LEFT  = 1               # Motor numbers 0, 1.
MTR_NUM_RIGHT = 0
MTR_DIR_LEFT  = 0               # Motor forward direction (0 or 1).
MTR_DIR_RIGHT = 1


def rampup(driver):
    # straight line
    driver.set_drive(MTR_NUM_LEFT , MTR_DIR_LEFT , 0)
    driver.set_drive(MTR_NUM_RIGHT, not MTR_DIR_RIGHT, 0)
    driver.enable()

    # Wait, just in case.
    time.sleep(0.25)

    # Ramp up/down
    for speed in chain(range(20,116), range(116,20,-1)):
        print("Speed = %3d" % speed)
        driver.set_drive(MTR_NUM_LEFT,  MTR_DIR_LEFT,  speed)
        driver.set_drive(MTR_NUM_RIGHT, not MTR_DIR_RIGHT, speed)
        time.sleep(.05)

    driver.set_drive(MTR_NUM_LEFT , MTR_DIR_LEFT , 0)
    driver.set_drive(MTR_NUM_RIGHT, not MTR_DIR_RIGHT, 0)
    driver.enable()

def turn(driver):
    # straight line
    driver.set_drive(MTR_NUM_LEFT , MTR_DIR_LEFT , 0)
    driver.set_drive(MTR_NUM_RIGHT, MTR_DIR_RIGHT, 0)
    driver.enable()

    # Wait, just in case.
    time.sleep(0.25)

    # Ramp up/down
    for speed in chain(range(20,88,2), range(88,20,-2)):
        print("Speed = %3d" % speed)
        driver.set_drive(MTR_NUM_LEFT,  MTR_DIR_LEFT,  speed)
        driver.set_drive(MTR_NUM_RIGHT, MTR_DIR_RIGHT, speed)
        time.sleep(.05)

    driver.set_drive(MTR_NUM_LEFT , MTR_DIR_LEFT , 0)
    driver.set_drive(MTR_NUM_RIGHT, MTR_DIR_RIGHT, 0)
    driver.enable()


#
#   Drive Function
#
def driveBot(driver):
    # Set speed to zero to enable.
    print('Enabling')


    while True:
        rampup(driver)
        turn(driver)

    # Set speed to zero.
    print('Stopping')
    driver.set_drive(MTR_NUM_LEFT , MTR_DIR_LEFT , 0)
    driver.set_drive(MTR_NUM_RIGHT, MTR_DIR_RIGHT, 0)

    # Wait, just in case.
    time.sleep(0.25)

    # Set speed to zero.
    print('Disabling')
    driver.disable()


#
#   Main
#
if __name__ == "__main__": 
    # Establish a connection to the motor drivers.
    driver = qwiic_scmd.QwiicScmd()

    # Check.
    if driver.connected == False:
        print("Motor Driver not connected!")
        sys.exit(0)

    # Initialize.
    driver.begin()
    print("Motor driver initialized.")

    # Run while watching exceptions.
    try:
        driveBot(driver)
    except BaseException as ex:
        print("Ending due to exception: %s" % repr(ex))
        driver.disable()
        sys.exit(0)
