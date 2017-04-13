#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        motorControllerTest
# Description:  For testing the motor controller -_-
#
#------------------------------------------------------------------------------

# Imports
from modul.motor import motor
from time import sleep

controller = None

# Main
try:
    controller = motor()
    controller.start()



    controller.setVelocityLeft(-100.0)
    controller.setVelocityRight(-100.0)

    sleep(30)


    controller.terminate()


except KeyboardInterrupt:
    controller.terminate()
    print("\033c")
    print("Goodbye!")
except:
    controller.terminate()
    print("\033c")
    print("Aaaaaargh!")
    raise