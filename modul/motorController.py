#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        MotorController
# Description:  This class provides:
#               - For movement
#                   - Access to the left and right stepmotor
#                   - Range from 0% to 100%
#               - For the fork on the front
#                   - Movement left or right
#
# Used Pins:
#               - BCM 12 (Pin 32) - Stepmotor Left PWM (PWM 0)
#               - BCM 13 (Pin 33) - Stepmotor Right PWM (PWM 1)
#               - BCM 16 (Pin 36) - Stepmotor Left Direction
#               - BCM 17 (Pin 11) - Stepmotor Right Direction
#
# ToDo:         - Module is currently under construction!
# ToDo:         - Testing!
#------------------------------------------------------------------------------

# Imports
import pigpio
from threading import Thread
from threading import RLock
from haleyenum.drivingDirection import DrivingDirection
from time import sleep

BCM_PIN_NR_PWM_LEFT = 12
BCM_PIN_NR_PWM_RIGHT = 13
BCM_PIN_NR_DIRECTION_LEFT = 16
BCM_PIN_NR_DIRECTION_RIGHT = 17
BCM_PIN_NR_FORK_ENABLE = 22

MIN_FREQUENCY = 0
MAX_FREQUENCY = 600
THREAD_SLEEP_MS = 10


class MotorController(Thread):
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        # Threading stuff
        Thread.__init__(self)
        self.lock = RLock()

        # Protected field by lock
        self.motorLeftDirection = DrivingDirection.FORWARD
        self.motorLeftCurrVelocity = 0
        self.motorRightDirection = DrivingDirection.FORWARD
        self.motorRightCurrVelocity = 0

        self.threadIsRunning = False
        self.threadRefreshDrive = False
        self.threadRefreshForkMotor = False

        # self.enableFork = BCM_PIN_NR_FORK_ENABLE ???
        self.pi = None
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
            self.pi.write(BCM_PIN_NR_FORK_ENABLE, 1)

            print(self.__class__.__name__ + ": ...done!")
            return True
        except:
            print(self.__class__.__name__ + ": ...failed!")
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
                    self.motorLeftCurrVelocity = abs(int((MAX_FREQUENCY / 100.0) * newValue))

                    if(newValue < 0):
                        self.motorLeftDirection = DrivingDirection.BACKWARD
                    else:
                        self.motorLeftDirection = DrivingDirection.FORWARD
                except:
                    pass
                finally:
                    self.threadRefreshDrive = True
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
                    self.motorRightCurrVelocity =  abs(int((MAX_FREQUENCY / 100.0) * newValue))

                    if(newValue < 0):
                        self.motorRightDirection = DrivingDirection.BACKWARD
                    else:
                        self.motorRightDirection = DrivingDirection.FORWARD

                except:
                    pass
                finally:
                    self.threadRefreshDrive = True
                    self.lock.release()

        return


    def stopDriver(self):
        """
        Description: Stops the stepmotors.
        """
        self.lock.acquire()
        try:
            self.motorRightCurrVelocity = 0
            self.motorLeftCurrVelocity = 0
            self.motorLeftDirection = DrivingDirection.FORWARD
            self.motorRightDirection = DrivingDirection.FORWARD
        except:
            pass
        finally:
            self.threadRefreshDrive = True
            self.lock.release()

        return


    def run(self):
        """
        Running thread, which will do all the work for this module.
        """
        self.threadIsRunning = True

        while (self.threadIsRunning):
            self.lock.acquire()
            try:
                # Refresh driver
                if(self.threadRefreshDrive):
                    self.pi.hardware_PWM(BCM_PIN_NR_PWM_LEFT, self.motorLeftCurrVelocity)
                    self.pi.hardware_PWM(BCM_PIN_NR_PWM_RIGHT, self.motorRightCurrVelocity)
                    self.pi.write(BCM_PIN_NR_DIRECTION_LEFT, self.motorLeftDirection)
                    self.pi.write(BCM_PIN_NR_DIRECTION_RIGHT, self.motorRightDirection)

                    self.threadRefreshDrive = False

                # Refresh forkmotor
                if(self.threadRefreshForkMotor):
                    # Do something

                    self.threadRefreshForkMotor = False
            except:
                pass
            finally:
                self.lock.release()

            sleep((1 / 1000) * THREAD_SLEEP_MS)

        return