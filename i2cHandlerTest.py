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

# Main
try:
    handler = I2cHandler()
    handler.start()
    handler.setRomanNumber(3)
    sleep(3)


except KeyboardInterrupt:
    print("\033c")
    print("Goodbye!")
except:
    print("\033c")
    print("Aaaaaargh!")
    raise