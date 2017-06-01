#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.19
#------------------------------------------------------------------------------
# Class:        DistanceSensorAdapter
# Description:  This class provides:
#               - Initialization and access to the Distance-Sensors via I2C
#               - Distance-Sensors: VL53L0X Time-of-Flight (ToF) ranging sensor
#
#               - BCM XX (Pin 01) - 3.3V DC Power
#               - BCM 02 (Pin 03) - SDA1, I2C
#               - BCM 03 (Pin 05) - SCL1, 12C
#               - BCM XX (Pin 06) - GND
#------------------------------------------------------------------------------
#
# Tests passed: - Channel tests (14, 15, 21, 26, 27) (2017.05.02)
#               - Init tests: Max. 5 retries if init fails (2017.05.02)
#
# ToDo:         - TESTING!
#
#------------------------------------------------------------------------------

# Imports
from modul.i2cModules.VL53L0X import SensorItem


# Sensor Constants
SENSOR_LEFT_BACK                        = 0
SENSOR_LEFT_BACK_SHUTDOWN_BCM_PIN_NR    = 14 # Test OK
SENSOR_LEFT_BACK_I2C_ADDRESS            = 0x30
SENSOR_LEFT_BACK_OFFSET                 = 0

SENSOR_LEFT_FRONT                       = 1
SENSOR_LEFT_FRONT_SHUTDOWN_BCM_PIN_NR   = 15 # Test OK
SENSOR_LEFT_FRONT_I2C_ADDRESS           = 0x31
SENSOR_LEFT_FRONT_OFFSET                = 0

SENSOR_FRONT                            = 2
SENSOR_FRONT_SHUTDOWN_BCM_PIN_NR        = 21 # Test OK
SENSOR_FRONT_I2C_ADDRESS                = 0x32
SENSOR_FRONT_OFFSET                     = 0

SENSOR_RIGHT_FRONT                      = 3
SENSOR_RIGHT_FRONT_SHUTDOWN_BCM_PIN_NR  = 26 # Test OK
SENSOR_RIGHT_FRONT_I2C_ADDRESS          = 0x33
SENSOR_RIGHT_FRONT_OFFSET               = 0

SENSOR_RIGHT_BACK                       = 4
SENSOR_RIGHT_BACK_SHUTDOWN_BCM_PIN_NR   = 27 # Test OK
SENSOR_RIGHT_BACK_I2C_ADDRESS           = 0x34
SENSOR_RIGHT_BACK_OFFSET                = 0

# Other Constants
INVALID_VALUE                           = -1


class DistanceSensorAdapter():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self._sensors = [None] * 5
        self._initDistanceSensors()


    # Funktions
    # --------------------------------------------------------------------------
    def _initDistanceSensors(self):
        """
        Description: Initializes the distance sensors
        Returns:     Boolean
        """
        try:
            self._printDebug("Init...")
            # Init sensors
            if(SENSOR_LEFT_BACK_SHUTDOWN_BCM_PIN_NR != 0):
                self._sensors[SENSOR_LEFT_BACK] = SensorItem.SensorItem(SENSOR_LEFT_BACK_SHUTDOWN_BCM_PIN_NR, SENSOR_LEFT_BACK_I2C_ADDRESS, SENSOR_LEFT_BACK_OFFSET)

            if (SENSOR_LEFT_FRONT_SHUTDOWN_BCM_PIN_NR != 0):
                self._sensors[SENSOR_LEFT_FRONT] = SensorItem.SensorItem(SENSOR_LEFT_FRONT_SHUTDOWN_BCM_PIN_NR, SENSOR_LEFT_FRONT_I2C_ADDRESS, SENSOR_LEFT_FRONT_OFFSET)

            if (SENSOR_FRONT_SHUTDOWN_BCM_PIN_NR != 0):
                self._sensors[SENSOR_FRONT] = SensorItem.SensorItem(SENSOR_FRONT_SHUTDOWN_BCM_PIN_NR, SENSOR_FRONT_I2C_ADDRESS, SENSOR_FRONT_OFFSET)

            if (SENSOR_RIGHT_FRONT_SHUTDOWN_BCM_PIN_NR != 0):
                self._sensors[SENSOR_RIGHT_FRONT] = SensorItem.SensorItem(SENSOR_RIGHT_FRONT_SHUTDOWN_BCM_PIN_NR, SENSOR_RIGHT_FRONT_I2C_ADDRESS, SENSOR_RIGHT_FRONT_OFFSET)

            if (SENSOR_RIGHT_BACK_SHUTDOWN_BCM_PIN_NR != 0):
                self._sensors[SENSOR_RIGHT_BACK] = SensorItem.SensorItem(SENSOR_RIGHT_BACK_SHUTDOWN_BCM_PIN_NR, SENSOR_RIGHT_BACK_I2C_ADDRESS, SENSOR_RIGHT_BACK_OFFSET)

            for x in range(0,5):
                if(self._sensors[x] is not None):
                    while ((self._sensors[x].isRunning() is False) and (self._sensors[x].getInitCounter() < 5)):
                        self._sensors[x].startRanging()

            self._printDebug("...done!")
            return True
        except Exception as err:
            self._printDebug("...Exception --> " + str(err))
            return False


    def getDistanceLeftBack(self):
        """
        Description: Reads the current distance from the back left sensor
        Returns:     Int
        """
        return self._getDistance(SENSOR_LEFT_BACK)


    def getDistanceLeftFront(self):
        """
        Description: Reads the current distance from the front left sensor
        Returns:     Int
        """
        return self._getDistance(SENSOR_LEFT_FRONT)


    def getDistanceFront(self):
        """
        Description: Reads the current distance from the front sensor
        Returns:     Int
        """
        return self._getDistance(SENSOR_FRONT)


    def getDistanceRightFront(self):
        """
        Description: Reads the current distance from the front right sensor
        Returns:     Int
        """
        return self._getDistance(SENSOR_RIGHT_FRONT)


    def getDistanceRightBack(self):
        """
        Description: Reads the current distance from the back right sensor
        Returns:     Int
        """
        return self._getDistance(SENSOR_RIGHT_BACK)


    def _getDistance(self, sensorNr):
        if (self._sensors[sensorNr] is not None):
            if(self._sensors[sensorNr].isRunning()):
                return self._sensors[sensorNr].getDistance()

        return INVALID_VALUE


    def _printDebug(self, message):
        if (__debug__):
            print("    {}: {}".format(self.__class__.__name__, message))