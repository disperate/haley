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

    while(True):
        sleep(0.1)
        print("\033c")
        print("Left Back: {:4d}, Left Front: {:4d}, Front: {:4d}".format(handler.getDistanceLeftBack(), handler.getDistanceLeftFront(), handler.getDistanceFront()))
        #print("Pitch: {0:3.3f}, Yaw: {0:3.3f}, Roll: {0:3.3f}".format(handler.getCurrPitch(), handler.getCurrYaw(), handler.getCurrRoll()))

    handler.terminate()


except KeyboardInterrupt:
    handler.terminate()
    print("Goodbye!")
except:
    handler.terminate()
    print("Aaaaaargh!")
    raise