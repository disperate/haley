#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        I2cHandlerTest
# Description:  For testing the I2C-Handler
#
#------------------------------------------------------------------------------

# Imports
from modul import i2cHandler
from time import sleep

handler = None

# Main
try:
    handler = i2cHandler.I2cHandler()
    handler.start()
    handler.setRomanNumber("3")

    while(True):
        sleep(0.1)
        print("\033c")
        print("LB: {:4d}, LF: {:4d}, F: {:4d}, RF: {:4d}, RB: {:4d}".format(
            handler.getDistanceLeftBack(),
            handler.getDistanceLeftFront(),
            handler.getDistanceFront(),
            handler.getDistanceRightFront(),
            handler.getDistanceRightBack()))
        print("Pitch: {0:07.3f}°, Yaw: {1:07.3f}°, Roll: {2:07.3f}°".format(
            handler.getCurrPitch(),
            handler.getCurrYaw(),
            handler.getCurrRoll()))
        print("Current relative yaw: {}".format(handler.currRelativeYaw))

    handler.terminate()

except KeyboardInterrupt:
    handler.terminate()
    print("Goodbye!")
except:
    handler.terminate()
    print("Aaaaaargh!")
    raise