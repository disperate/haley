#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        MotorController
# Description:  This class provides:
#               - Access to the left and right motor
#               - Range from 0% to 100%
#
# Used Pins:
#               - PWM 0 = BCM 12 (GPIO 26 - Pin 32)
#               - PWM 1 = BCM 13 (GPIO 23 - Pin 33)
#
# ToDo:         - Module is currently under construction!
#------------------------------------------------------------------------------

# Imports
import pigpio

BCM_PWM0 = 12
BCM_PWM1 = 13
MotorEnable = 22

MIN_FREQUENCY = 0
MAX_FREQUENCY = 600

class MotorController():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self.pi = None
        self.pwmChannel0 = BCM_PWM0
        self.pwmChannel1 = BCM_PWM1
        self.enableChannel = MotorEnable

        self.initMotorController()


    # Funktions
    # --------------------------------------------------------------------------
    def initMotorController(self):
        """
        Description: Initializes motor controller
        Returns:     Boolean
        """
        try:
            print(self.__class__.__name__ + ": Init...")
            self.pi = pigpio.pi()

            ##Stopping motors
            self.pi.write(22, 1)


            print(self.__class__.__name__ + ": ...done!")
            return True
        except:
            print(self.__class__.__name__ + ": ...failed!")
            return False


    def setVelocityLeft(self, newValue):
        """
        Description: Reads the current distance from the front sensor
        Args:        1. NewValue as float
        Returns:     Boolean
        """

        # Value from 0% to 100%
        # new motor value would be: (MAX_FREQUENCY / 100) * newValue
        # Max Velocity is settable with MAX_FREQUENCY

        return True


    def setVelocityRight(self, newValue):
        """
        Description: Reads the current distance from the front sensor
        Returns:     Boolean
        """
        return True


    def getCurrentVelocityRight(self):
        """
        Description: Reads the current distance from the front sensor
        Returns:     Boolean
        """
        return True


    def getCurrentVelocityLeft(self):
        """
        Description: Reads the current distance from the front sensor
        Returns:     Boolean
        """
        return True
