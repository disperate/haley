#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.06
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        DistanceSensorAdapter
# Description:  This class provides:
#               - Initialization and access to the Distance-Sensors via I2C
#               - Distance-Sensors: VL53L0X Time-of-Flight (ToF) ranging sensor
#------------------------------------------------------------------------------

# Imports
import pigpio

# Class
class DistanceSensorAdapter():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self.pi = pigpio.pi()

        self.initDistanceSensors()


    # Funktions
    # --------------------------------------------------------------------------
    def initDistanceSensors(self):
        """
        Description: Initializes the distance sensors
        Returns:     Boolean
        """
        try:
            return True
        except:
            return False


    def getDistanceFront(self):
        """
        Description: Reads the current distance from the front sensor
        Returns:     Float
        """
        return 0.0


    def getDistanceFrontLeft(self):
        """
        Description: Reads the current distance from the front left sensor
        Returns:     Float
        """
        return 0.0


    def getDistanceFrontRight(self):
        """
        Description: Reads the current distance from the front right sensor
        Returns:     Float
        """
        return 0.0


    def getDistanceBackLeft(self):
        """
        Description: Reads the current distance from the back left sensor
        Returns:     Float
        """
        return 0.0


    def getDistanceBackRight(self):
        """
        Description: Reads the current distance from the back right sensor
        Returns:     Float
        """
        return 0.0