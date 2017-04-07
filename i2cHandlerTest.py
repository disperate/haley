#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.06
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        I2cHandlerTest
# Description:  For testing the I2C-Handler
#
#------------------------------------------------------------------------------

# Imports
from modul.i2cHandler import I2cHandler
from time import sleep

handler = None

# Main
try:
    handler = I2cHandler()
    handler.start()

    while(True):
        print("\033c")
        print("Pitch: " + str(handler.getCurrPitch()))
        print("Yaw: " + str(handler.getCurrYaw()))
        print("Roll: " + str(handler.getCurrRoll()))
        sleep(0.05)

    handler.terminate()


except KeyboardInterrupt:
    handler.terminate()
    print("\033c")
    print("Goodbye!")
except:
    handler.terminate()
    print("\033c")
    print("Aaaaaargh!")
    raise