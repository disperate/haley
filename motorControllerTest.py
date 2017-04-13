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
from modul.motorController import MotorController
from time import sleep

controller = None

# Main
try:
    controller = MotorController()
    controller.start()

    controller.setVelocityLeft(10.0)
    controller.setVelocityRight(10.0)

    sleep(2)

    controller.setVelocityLeft(-5.0)
    controller.setVelocityRight(-5.0)

    sleep(2)

    controller.setVelocityLeft(1.0)
    controller.setVelocityRight(1.0)

    sleep(5)

    controller.setVelocityLeft(2.8246466)
    controller.setVelocityRight(-13.46978456)

    sleep(2)

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