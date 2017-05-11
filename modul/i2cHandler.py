#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------
#
# I2C-Map:      - "sudo i2cdetect -y 1"
#
#                    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
#               00:          -- -- -- -- -- -- -- -- -- -- -- -- --
#               10: -- -- -- -- -- -- -- -- -- -- -- -- 1c -- -- --
#               20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#               30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#               40: -- -- -- -- -- -- UU -- -- -- -- -- -- -- -- --
#               50: -- -- -- -- -- -- -- -- -- -- -- -- 5c -- -- 5f
#               60: -- -- -- -- -- -- -- -- -- -- 6a -- -- -- -- --
#               70: -- -- -- -- -- -- -- --
#
#               - 0x1C --> Sense-Hat:   LSM9DS1     (Accelerometer / Gyro)
#               - 0x46 --> Sense-Hat:   ATTINY88    (RGB-Display / Joystick)
#               - 0x5C --> Sense-Hat:   LPS25H      (Pressure / Temperature)
#               - 0x5F --> Sense-Hat:   HTS221      (Humidity / Temperature)
#               - 0x6A --> Sense-Hat:   LSM9DS1     (Magnetometer)
#
#               Reserved for sensors:
#               - 0x30 --> VL53L0X-TOF-Sensor Left-Back
#               - 0x31 --> VL53L0X-TOF-Sensor Left-Front
#               - 0x32 --> VL53L0X-TOF-Sensor Front
#               - 0x33 --> VL53L0X-TOF-Sensor Right-Front
#               - 0x34 --> VL53L0X-TOF-Sensor Right-Back
#
#-------------------------------------------------------------------------------
#
# Tests passed: - Write numbers to display (2017.04.07)
#               - Write states to display (2017.04.07)
#               - Read gyro-states (2017.04.07)
#
#------------------------------------------------------------------------------

# Imports
from threading import Thread
from threading import RLock
from time import sleep
from modul.i2cModules import senseHatAdapter
from modul.i2cModules import distanceSensorAdapter

# Constants
INVALID_VALUE               = -1
DISPLAY_MAX_STATES          = 8
THREAD_SLEEP_MS             = 100

class I2cHandler(Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        print(self.__class__.__name__ + ": Init...")

        # Threading stuff
        Thread.__init__(self)
        self.lock = RLock()

        # Protected field by lock
        self.currDistanceLeftBack   = 0
        self.currDistanceLeftFront  = 0
        self.currDistanceFront      = 0
        self.currDistanceRightFront = 0
        self.currDistanceRightBack  = 0
        self.currYaw                = 0.0
        self.prevYaw                = 0.0
        self.currPitch              = 0.0
        self.currRoll               = 0.0
        self.currRelativeYaw = 0

        self.dispStatesList = [0] * DISPLAY_MAX_STATES
        self.dispRomanNumber = 0

        self.threadIsRunning = False
        self.threadMeasureOrientation = True
        self.threadMeasureDistance = True
        self.threadRefreshDisplay = False

        # Used modules
        self.senseHat = senseHatAdapter.SenseHatAdapter()
        self.distanceSensors = distanceSensorAdapter.DistanceSensorAdapter()

        print(self.__class__.__name__ + ": ...done!")


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
            currYaw = self.currYaw
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
            currPitch = self.currPitch
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
            currRoll = self.currRoll
        except:
            pass
        finally:
            self.lock.release()

        return currRoll


    def _setRelativeYaw(self):
        currentValue = self.currYaw
        previousValue = self.prevYaw

        if((currentValue is not None) and (previousValue is not None)):
            # Check if the value jumps between 360° and 0°
            if(abs(currentValue - previousValue) < 90.0):
                self.currRelativeYaw = self.currRelativeYaw + (currentValue - previousValue)
            else:
                # Now it's getting dirty!
                if(previousValue < currentValue):
                    self.currRelativeYaw = self.currRelativeYaw - (360.0 - currentValue + previousValue)
                else:
                    self.currRelativeYaw = self.currRelativeYaw + (360.0 - previousValue + currentValue)


    def resetRelativeYaw(self):
        self.currRelativeYaw = 0.0


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
        self._printDebug("setRomanNumber() ...enter")
        self.lock.acquire()
        try:
            self._printDebug("setRomanNumber() ...try")
            self.dispRomanNumber = int(newNumber)
        except:
            self._printDebug("setRomanNumber() ...except")
        finally:
            self._printDebug("setRomanNumber() ...finally")
            self.threadRefreshDisplay = True
            self.lock.release()

        return


    def getDistanceLeftBack(self):
        """
        Description: Gets the distance value from the last measurement of the
                     back left sensor.
        Returns:     Int
        """
        currDistance = INVALID_VALUE
        self.lock.acquire()
        try:
            currDistance = self.currDistanceLeftBack
        except:
            pass
        finally:
            self.lock.release()

        return currDistance


    def getDistanceLeftFront(self):
        """
        Description: Gets the distance value from the last measurement of the
                     front left sensor.
        Returns:     Int
        """
        currDistance = INVALID_VALUE
        self.lock.acquire()
        try:
            currDistance = self.currDistanceLeftFront
        except:
            pass
        finally:
            self.lock.release()

        return currDistance


    def getDistanceFront(self):
        """
        Description: Gets the distance value from the last measurement of the
                     front sensor.
        Returns:     Int
        """
        currDistance = INVALID_VALUE
        self.lock.acquire()
        try:
            currDistance = self.currDistanceFront
        except:
            pass
        finally:
            self.lock.release()

        return currDistance


    def getDistanceRightFront(self):
        """
        Description: Gets the distance value from the last measurement of the
                     front right sensor.
        Returns:     Int
        """
        currDistance = INVALID_VALUE
        self.lock.acquire()
        try:
            currDistance = self.currDistanceRightFront
        except:
            pass
        finally:
            self.lock.release()

        return currDistance


    def getDistanceRightBack(self):
        """
        Description: Gets the distance value from the last measurement of the
                     back right sensor.
        Returns:     Int
        """
        currDistance = INVALID_VALUE
        self.lock.acquire()
        try:
            currDistance = self.currDistanceRightBack
        except:
            pass
        finally:
            self.lock.release()

        return currDistance

    def getDistance(self, direction, drivingDirection):
        if(direction.LEFT):
            if(drivingDirection.FORWARD):
                return self.currDistanceLeftFront
            else:
                return self.currDistanceLeftBack
        else:
            if (drivingDirection.FORWARD):
                return self.currDistanceRightFront
            else:
                return self.currDistanceRightBack



    def terminate(self):
        """
        Description: Stops running thread. Threads stops after
                     a complete while loop.
        """
        self.lock.acquire()
        try:
            self.senseHat.clearDisplay()
            self.threadIsRunning = False
        except:
            pass
        finally:
            self.lock.release()

        return


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        print(self.__class__.__name__ + ": Start thread...")
        self.threadIsRunning = True

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
                    self.currDistanceLeftBack = self.distanceSensors.getDistanceLeftBack()
                    self.currDistanceLeftFront = self.distanceSensors.getDistanceLeftFront()
                    self.currDistanceFront = self.distanceSensors.getDistanceFront()
                    self.currDistanceRightFront = self.distanceSensors.getDistanceRightFront()
                    self.currDistanceRightBack = self.distanceSensors.getDistanceRightBack()

                if (self.threadMeasureOrientation):
                    if(self.senseHat.refreshOrientation()):
                        # Get orientation
                        self.prevYaw = self.currYaw
                        self.currYaw = self.senseHat.getYaw()
                        self.currPitch = self.senseHat.getPitch()
                        self.currRoll = self.senseHat.getRoll()
                        self._setRelativeYaw()

            except Exception as err:
                self._printDebug("...Exception --> " + str(err))
            finally:
                self.lock.release()

            sleep((1 / 1000) * THREAD_SLEEP_MS)

        return


    def _printDebug(self, message):
        if (__debug__):
            print("  {}: {}".format(self.__class__.__name__, message))