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


class motor(Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        # Threading stuff
        Thread.__init__(self)
        self.lock = RLock()

        # Protected field by lock
        self.motorIsEnabled = False
        self.motorLeftDirection = DrivingDirection.FORWARD.value
        self.motorLeftCurrVelocity = 0
        self.motorRightDirection = DrivingDirection.FORWARD.value
        self.motorRightCurrVelocity = 0

        self.threadIsRunning = False
        self.threadRequestStop = False
        self.threadRefreshDrive = False

        self.pi = None
        self.initMotor()


    # Funktions
    # --------------------------------------------------------------------------
    def initMotor(self):
        """
        Description: Initializes motor controller
        Returns:     Boolean
        """
        try:
            self._printDebug("Init...")

            if(self.pi is None):
                self.pi = pigpio.pi()

            self.pi.write(BCM_PIN_NR_ENABLE, 1)

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

                self.lock.acquire()
                try:
                    self._setVelocityLeft(int(round(((MAX_FREQUENCY / 100.0) * newValue), 0)))
                except Exception as err:
                    self._printDebug("setVelocityLeft(): Exception --> " + str(err))
                finally:
                    self.lock.release()

        return


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
                self.lock.acquire()
                try:
                    self._setVelocityRight(int(round(((MAX_FREQUENCY / 100.0) * newValue), 0)))
                except Exception as err:
                    self._printDebug("setVelocityRight(): Exception --> " + str(err))
                finally:
                    self.lock.release()

        return


    def stopDriver(self):
        """
        Description: Stops the stepping motors.
        """
        self.lock.acquire()
        try:
            self._stopDriver()
        except:
            pass
        finally:
            self.lock.release()

        return


    def _stopDriver(self):
        """
        Description: This function is only for the class itself!
        """
        self._setVelocityLeft(0)
        self._setVelocityRight(0)
        self.pi.write(BCM_PIN_NR_ENABLE, 1)
        self.motorIsEnabled = False

        return


    def _setVelocityLeft(self, currVelocity):
        """
        Description: This function is only for the class itself!
        Args:        1. currVelocity as Integer
        """
        self.motorLeftCurrVelocity = abs(currVelocity)

        if (currVelocity < 0):
            self.motorLeftDirection = DrivingDirection.BACKWARD.value
        else:
            self.motorLeftDirection = DrivingDirection.FORWARD.value

        if(self.motorIsEnabled is not True):
            self.pi.write(BCM_PIN_NR_ENABLE, 0)
            self.motorIsEnabled = True

        self.threadRefreshDrive = True

        return


    def _setVelocityRight(self, currVelocity):
        """
        Description: This function is only for the class itself!
        Args:        1. currVelocity as Integer
        """
        self.motorRightCurrVelocity = abs(currVelocity)

        if (currVelocity < 0):
            self.motorRightDirection = DrivingDirection.BACKWARD.value
        else:
            self.motorRightDirection = DrivingDirection.FORWARD.value

        if(self.motorIsEnabled is not True):
            self.pi.write(BCM_PIN_NR_ENABLE, 0)
            self.motorIsEnabled = True

        self.threadRefreshDrive = True

        return


    def terminate(self):
        """
        Description: Stops running thread. Threads stops after
                     a complete while loop.
        """
        self.lock.acquire()
        try:
            self._stopDriver()
            self.threadRequestStop = True
        except:
            pass
        finally:
            self.lock.release()

        return


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        self.threadIsRunning = True
        self.threadRequestStop = False

        while (self.threadIsRunning):
            self.lock.acquire()
            try:
                #
                if(self.threadRequestStop):
                    self.threadIsRunning = False

                # Refresh driver
                if(self.threadRefreshDrive):
                    self.pi.hardware_PWM(BCM_PIN_NR_PWM_LEFT, self.motorLeftCurrVelocity, PWM_DEFAULT_DUTYCYCLE)
                    self.pi.hardware_PWM(BCM_PIN_NR_PWM_RIGHT, self.motorRightCurrVelocity, PWM_DEFAULT_DUTYCYCLE)
                    self.pi.write(BCM_PIN_NR_DIRECTION_LEFT, self.motorLeftDirection)
                    self.pi.write(BCM_PIN_NR_DIRECTION_RIGHT, self.motorRightDirection)

                    self.threadRefreshDrive = False
            except Exception as err:
                self._printDebug("Thread: Exception --> " + str(err))
            finally:
                self.lock.release()

            sleep((1 / 1000) * THREAD_SLEEP_MS)

        return


    def _printDebug(self, message):
        if (__debug__):
            print("{}: {}".format(self.__class__.__name__, message))