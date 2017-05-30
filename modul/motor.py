#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        MotorController
# Description:  This class provides:
#               - For movement
#                   - Access to the left and right stepping motor
#                   - Range from -100% to 100%
#
# Used Pins:
#               - BCM 12 (Pin 32) - Stepping motor Left PWM (PWM 0)
#               - BCM 13 (Pin 33) - Stepping motor Right PWM (PWM 1)
#               - BCM 16 (Pin 36) - Stepping motor Left Direction
#               - BCM 17 (Pin 11) - Stepping motor Right Direction
#
#------------------------------------------------------------------------------
#
# Tests passed: - setVelocityLeft() (2017.04.13)
#               - setVelocityRight() (2017.04.13)
#               - stopDriver() (2017.04.13)
#               - terminate() (2017.04.13)
#
#------------------------------------------------------------------------------
# ToDo:         - Testing!
#------------------------------------------------------------------------------

# Imports
import pigpio
from threading import Thread
from threading import RLock
from haleyenum.drivingDirection import DrivingDirection
from time import sleep
from datetime import datetime

# Constants
BCM_PIN_NR_PWM_LEFT = 12
BCM_PIN_NR_PWM_RIGHT = 13
BCM_PIN_NR_DIRECTION_LEFT = 16
BCM_PIN_NR_DIRECTION_RIGHT = 17
BCM_PIN_NR_ENABLE = 22

PWM_DEFAULT_DUTYCYCLE = 250000 # 25%
MIN_FREQUENCY = 0
MAX_FREQUENCY = 700
THREAD_SLEEP_MS = 10

LOG_FILENAME = "_Log_Motor.csv"


class motor(Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        # Threading stuff
        Thread.__init__(self)
        self._lock = RLock()

        # Protected field by lock
        self._motorIsEnabled = False
        self._motorLeftDirection = DrivingDirection.FORWARD.value
        self._motorLeftCurrVelocity = 0
        self._motorRightDirection = DrivingDirection.FORWARD.value
        self._motorRightCurrVelocity = 0

        self._threadIsRunning = False
        self._threadRequestStop = False
        self._threadRefreshDrive = False
        self._threadWriteLog = False

        self._pi = None
        self._initMotor()

        self._listVelocityMeasurement = list()


    # Funktions
    # --------------------------------------------------------------------------
    def _initMotor(self):
        """
        Description: Initializes motor controller
        Returns:     Boolean
        """
        try:
            self._printDebug("Init...")

            if(self._pi is None):
                self._pi = pigpio.pi()

            self._pi.write(BCM_PIN_NR_ENABLE, 1)

            self._printDebug("...done!")
            return True
        except Exception as err:
            self._printDebug("...failed --> " + str(err))
            return False


    def setVelocityLeft(self, newValue = 0.0):
        """
        Description: Sets the current velocity for the left wheels
                     between -100 and +100.
                     Range from 0.0 (Stop) to 100.0 (Full throttle).
                     If value is positive: Moving forward.
                     If value is negative: Moving backward.
                     For safety: If newValue is set as None, then a value of
                     0.0 will used to stop the wheels.
        Args:        1. NewValue as float
        """
        if(newValue is not None):
            if((-100.0 <= newValue) and (newValue <= 100.0)):
                self._setVelocityLeft(int(round(((MAX_FREQUENCY / 100.0) * newValue), 0)))

        return


    def getCurrVelocityLeft(self):
        if(self._motorLeftDirection is DrivingDirection.FORWARD.value):
            return (100.0 / MAX_FREQUENCY) * self._motorLeftCurrVelocity
        else:
            return (100.0 / MAX_FREQUENCY) * self._motorLeftCurrVelocity * - 1


    def setVelocityRight(self, newValue = 0.0):
        """
        Description: Sets the current velocity for the right wheels
                     between -100 and +100.
                     Range from 0.0 (Stop) to 100.0 (Full throttle).
                     If value is positive: Moving forward.
                     If value is negative: Moving backward.
                     For safety: If newValue is set as None, then a value of
                     0.0 will used to stop the wheels.
        Args:        1. NewValue as float
        """
        if (newValue is not None):
            if ((-100.0 <= newValue) and (newValue <= 100.0)):
                self._setVelocityRight(int(round(((MAX_FREQUENCY / 100.0) * newValue), 0)))

        return


    def getCurrVelocityRight(self):
        if(self._motorRightDirection is DrivingDirection.FORWARD.value):
            return (100.0 / MAX_FREQUENCY) * self._motorRightCurrVelocity
        else:
            return (100.0 / MAX_FREQUENCY) * self._motorRightCurrVelocity * - 1


    def stop(self):
        """
        Description: Stops the stepping motors.
        """
        self._stopMotor()

        return


    def _stopMotor(self):
        """
        Description: This function is only for the class itself!
        """
        self._setVelocityLeft(0)
        self._setVelocityRight(0)
        self._pi.write(BCM_PIN_NR_ENABLE, 1)
        self._motorIsEnabled = False

        return


    def _setVelocityLeft(self, currVelocity):
        """
        Description: This function is only for the class itself!
        Args:        1. currVelocity as Integer
        """
        self._motorLeftCurrVelocity = abs(currVelocity)

        if (currVelocity < 0):
            self._motorLeftDirection = DrivingDirection.BACKWARD.value
        else:
            self._motorLeftDirection = DrivingDirection.FORWARD.value

        if(self._motorIsEnabled is not True):
            self._pi.write(BCM_PIN_NR_ENABLE, 0)
            self._motorIsEnabled = True

        self._threadRefreshDrive = True

        return


    def _setVelocityRight(self, currVelocity):
        """
        Description: This function is only for the class itself!
        Args:        1. currVelocity as Integer
        """
        self._motorRightCurrVelocity = abs(currVelocity)

        if (currVelocity < 0):
            self._motorRightDirection = DrivingDirection.BACKWARD.value
        else:
            self._motorRightDirection = DrivingDirection.FORWARD.value

        if(self._motorIsEnabled is not True):
            self._pi.write(BCM_PIN_NR_ENABLE, 0)
            self._motorIsEnabled = True

        self._threadRefreshDrive = True

        return


    def terminate(self):
        """
        Description: Stops running thread. Threads stops after
                     a complete while loop.
        """
        self._stopMotor()
        self._threadRequestStop = True

        return


    def startLogging(self):
        self._listVelocityMeasurement.clear()
        self._listVelocityMeasurement.append("Motor-Driver Logging")
        self._listVelocityMeasurement.append("\n;;")
        self._listVelocityMeasurement.append("\nDate;Velocity-Left;Velocity-Right")
        self._threadWriteLog = True


    def _getLogEntryForCurrentVelocity(self):
        logEntry = datetime.now().strftime("(%Y.%m.%d - %H:%M:%S.%f)")

        if(self._motorLeftDirection is DrivingDirection.FORWARD.value):
            logEntry += ";{}".format(self._motorLeftCurrVelocity)
        else:
            logEntry += ";{}".format(self._motorLeftCurrVelocity * -1)

        if(self._motorRightDirection is DrivingDirection.FORWARD.value):
            logEntry += ";{}".format(self._motorRightCurrVelocity)
        else:
            logEntry += ";{}".format(self._motorRightCurrVelocity * -1)

        return logEntry

    def stopLogging(self):
        self._threadWriteLog = False
        logFile = open(datetime.now().strftime("(%Y-%m-%dT%H%M%S)") + LOG_FILENAME, 'a')
        logFile.writelines(self._listVelocityMeasurement)
        logFile.close()
        self._listVelocityMeasurement.clear()


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        self._threadIsRunning = True
        self._threadRequestStop = False

        while (self._threadIsRunning):
            try:
                # Stop thread
                if(self._threadRequestStop):
                    self._threadIsRunning = False

                # Refresh driver
                if(self._threadRefreshDrive):
                    self._pi.hardware_PWM(BCM_PIN_NR_PWM_LEFT, self._motorLeftCurrVelocity, PWM_DEFAULT_DUTYCYCLE)
                    self._pi.hardware_PWM(BCM_PIN_NR_PWM_RIGHT, self._motorRightCurrVelocity, PWM_DEFAULT_DUTYCYCLE)
                    self._pi.write(BCM_PIN_NR_DIRECTION_LEFT, self._motorLeftDirection)
                    self._pi.write(BCM_PIN_NR_DIRECTION_RIGHT, self._motorRightDirection)

                    self._threadRefreshDrive = False

                # Log current velocity
                if(self._threadWriteLog):
                    self._listVelocityMeasurement.append("\n" + self._getLogEntryForCurrentVelocity())


            except Exception as err:
                self._stopMotor()
                self._threadIsRunning = False
                self._printDebug("Thread: Exception --> " + str(err))
            finally:
                pass

            sleep((1 / 1000) * THREAD_SLEEP_MS)

        return


    def _printDebug(self, message):
        if (__debug__):
            print("{}: {}".format(self.__class__.__name__, message))