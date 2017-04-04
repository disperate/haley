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
# Sensors:      - Read:     On measuring (continuous reading)
#                 Write:    On initialisation
# Sense-Hat:    - Read:     Gyro-States (continuous reading)
#                 Write:    Display
#
# ToDo:         - PyCharm highlights rows with "ToDo" which is nice
# ToDo:         - Testing the whole sheit
#------------------------------------------------------------------------------

# Imports
import threading
from time import sleep
from modul.i2cModules import senseHatAdapter
from modul.i2cModules import distanceSensorAdapter

# Variables
SENSOR_DATA_BUFFER_SIZE = 5
DISPLAY_MAX_STATES      = 8
THREAD_SLEEP_MS         = 100


# Class
class I2cHandler(threading.Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        # Threading stuff
        threading.Thread.__init__(self)
        self.lock = threading.RLock()

        # Protected field by locks
        self.currYaw = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.currPitch = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.currRoll = [0.0] * SENSOR_DATA_BUFFER_SIZE
        self.dispStatesList = [0] * DISPLAY_MAX_STATES
        self.dispRomanNumber = 0
        self.threadMeasureOrientation = True
        self.threadMeasureDistance = True
        self.threadRefreshDisplay = False

        # Unprotected field
        self.threadIsRunning = True

        # Used modules
        self.senseHat = senseHatAdapter.SenseHatAdapter()
        self.distanceSensors = distanceSensorAdapter.DistanceSensorAdapter()


    # Funktions
    # --------------------------------------------------------------------------
    def getCurrYaw(self):
        """
        Description: Gets the yaw-value from the last measurement
        Returns:     Float
        """
        currYaw = 0.0
        self.lock.acquire()
        try:
            currYaw = self.currYaw[0]
        except:
            pass
        finally:
            self.lock.release()

        return currYaw


    def getCurrPitch(self):
        """
        Description: Gets the pitch-value from the last measurement
        Returns:     Float
        """
        currPitch = 0.0
        self.lock.acquire()
        try:
            currPitch = self.currPitch[0]
        except:
            pass
        finally:
            self.lock.release()

        return currPitch


    def getCurrRoll(self):
        """
        Description: Gets the roll-value from the last measurement
        Returns:     Float
        """
        currRoll = 0.0
        self.lock.acquire()
        try:
            currRoll = self.currRoll[0]
        except:
            pass
        finally:
            self.lock.release()

        return currRoll


    def setStatus(self, newNumber, newState):
        """
        Description: Sets the status LED on the sense-hat for a visual feedback
                     of a given module.
                     Possible values (0-2): "IDLE", "RUNNING", "STOPPED"
        Args:        1. Position as number or a string
                     2. State value (0-2)
        """
        if ((0 <= newNumber) and (newNumber < DISPLAY_MAX_STATES)):
            self.lock.acquire()
            try:
                self.dispStatesList[newNumber] = newState
            except:
                pass
            finally:
                self.threadRefreshDisplay = True
                self.lock.release()

        return


    def setRomanNumber(self, newNumber):
        """
        Description: Sets the roman number
        Args:        1. Number as integer or string
        """
        self.lock.acquire()
        try:
            self.dispRomanNumber = int(newNumber)
        except:
            pass
        finally:
            self.threadRefreshDisplay = True
            self.lock.release()

        return


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        while (self.threadIsRunning):
            self.lock.acquire()
            try:
                # Write stuff to display
                if(self.threadRefreshDisplay):
                    self.senseHat.setStatusLeds(self.dispStatesList)
                    self.senseHat.setRomanNumber(self.dispRomanNumber)
                    self.senseHat.refreshDisplay()

                    self.threadRefreshDisplay = False

                if (self.threadMeasureDistance):
                    # Do measurements and save the results locally
                    pass

                if (self.threadMeasureOrientation):
                    if(self.senseHat.refreshOrientation()):
                        # get orientation
                        self.currYaw.append(self.senseHat.getYaw())
                        self.currPitch.append(self.senseHat.getPitch())
                        self.currRoll.append(self.senseHat.getRoll())
                        self.currYaw.pop(0)
                        self.currPitch.pop(0)
                        self.currRoll.pop(0)
            except:
                pass
            finally:
                self.lock.release()

            sleep((1 / 1000) * THREAD_SLEEP_MS)

        return