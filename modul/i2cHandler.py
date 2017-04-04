#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.04
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        I2cHandler
# Description:  This class provides:
#               - Guarantees "synchronised" access to the I2C-bus.
#               - Act as a container for gyro- and distance-data
#               - Reads via thread continuous the current gyro- and
#                 distance-values and stores it
#               - Access to the sense-hat
#
# Sensors:      - Read:     On measuring
#                 Write:    On initialisation
# Sense-Hat:    - Read:     Gyro-States
#                 Write:    Display
#------------------------------------------------------------------------------

# Imports
from modul.i2cModules import senseHatAdapter
from modul.i2cModules import distanceSensorAdapter

# Variables
SENSOR_DATA_BUFFER_SIZE = 5


# Class
class I2cHandler(threading.Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        # Threading stuff
        threading.Thread.__init__(self)
        self.condition = threading.Condition()

        # Protected field by condition
        self.currYaw = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.currPitch = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.currRoll = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.measureOrientation = False
        self.measureDistance = False

        # Unprotected field
        self.threadIsRunning = True


    # Funktions
    # --------------------------------------------------------------------------
    def getCurrYaw(self):
        """
        Description: Gets the yaw-value from the last forced measurement
        Returns:     Float
        """
        with self.condition:
            self.condition.wait()
            return self.currYaw[0]


    def getCurrPitch(self):
        """
        Description: Gets the pitch-value from the last forced measurement
        Returns:     Float
        """
        with self.condition:
            self.condition.wait()
            return self.currPitch[0]


    def getCurrRoll(self):
        """
        Description: Gets the roll-value from the last forced measurement
        Returns:     Float
        """
        with self.condition:
            self.condition.wait()
            return self.currRoll[0]


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        while (self.threadIsRunning):
            with self.condition:
                # Write stuff to display

                if(self.measureDistance):
                    # Do measurements and save the results locally
                    pass

                if(self.measureOrientation):
                    newYaw = 0.0
                    newRoll = 0.0
                    newPitch = 0.0

                    # get orientation()

                    self.currYaw.append(newYaw)
                    self.currPitch.append(newPitch)
                    self.currRoll.append(newRoll)
                    self.currYaw.pop(0)
                    self.currPitch.pop(0)
                    self.currRoll.pop(0)

                # After all, release lock
                self.condition.notifyAll()

        return