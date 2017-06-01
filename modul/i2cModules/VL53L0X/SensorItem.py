#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.19
#------------------------------------------------------------------------------
# Class:        SensorItem
# Description:  This class provides:
#               - xxx
#------------------------------------------------------------------------------
#
# ToDo:         - TESTING!
#
#------------------------------------------------------------------------------

# Imports
from modul.i2cModules.VL53L0X import VL53L0X
import pigpio
from time import sleep


# Constants
INVALID_VALUE = -1
RESET_TIME_MS = 250 # Time in milliseconds


class SensorItem():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self, shutDownPin, address, offset):
        self._pigpio  = None
        self._shutDownPin = shutDownPin
        self._address = address
        self._offset = offset
        self._sensor = None
        self._initCounter = 0
        self._sensorIsRunning = False
        self._timingBudget = 100
        self._preInitSensor()
        self._printDebug("New instance")

    # Funktions
    # --------------------------------------------------------------------------
    def _preInitSensor(self):
        self._printDebug("Enter _preInitSensor()")
        if(self._pigpio is None):
            self._pigpio = pigpio.pi()

        self._sensor = VL53L0X.VL53L0X(self._address)
        self._printDebug("Leave _preInitSensor()")


    def startRanging(self):
        self._printDebug("-------------------------------")
        self._printDebug("Start Ranging...")
        self._initCounter = self._initCounter + 1
        self.resetSensor()
        self._pigpio.write(self._shutDownPin, 1)
        self._printDebug("{}. try to activate sensor".format(self._initCounter))
        self._sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self._timingBudget = self._sensor.get_timing()

        if(self._sensor.status == 0):
            self._printDebug("Sensor is activated...")
            self._printDebug("Timing-Budget is: {}ms".format(int(self._timingBudget / 1000)))
            self._sensorIsRunning = True
        else:
            self._printDebug("Sensor activation error")


    def stopRanging(self):
        if(self._sensor is not None):
            self._sensor.stop_ranging()

        self._sensorIsRunning = False


    def resetSensor(self):
        self._pigpio.write(self._shutDownPin, 0)
        sleep((1 / 1000) * RESET_TIME_MS)


    def getDistance(self):
        if ((self._sensor is None) or (self._sensorIsRunning is False)):
            return INVALID_VALUE
        else:
            return self._sensor.get_distance() + self._offset


    def getInitCounter(self):
        return self._initCounter


    def isRunning(self):
        return self._sensorIsRunning


    def _printDebug(self, message):
        if (__debug__):
            print("      {} (0x{:x}): {}".format(self.__class__.__name__, self._address, message))