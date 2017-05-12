#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.05.12
#------------------------------------------------------------------------------
# Class:        ForkHandler
# Description:  Provides access to the Fork
#------------------------------------------------------------------------------
#
#               - BCM 18 (Pin xx) - Forkmotor direction right
#               - BCM 19 (Pin xx) - Forkmotor direction left
#
# ToDo:         - Test "setPositionForNumber()" for right parcour!
#------------------------------------------------------------------------------

# Imports
import pigpio
from threading import Thread
from haleyenum.direction import direction
from time import sleep

# Constants
BCM_PIN_NR_FORK_MOT_RIGHT   = 18
BCM_PIN_NR_FORK_MOT_LEFT    = 19
THREAD_SLEEP_MS = 10

class Fork():
    def __init__(self, i2cHandler):
        self.pi = None
        self.i2cHandler = i2cHandler
        self.buttonDistanceList = [100, 54, 118, 33, 89, 148, 100] # Don't Touch!
        self.initFork()

    # Funktions
    # --------------------------------------------------------------------------
    def initFork(self):
        """
        Description: Initializes fork
        Returns:     Boolean
        """
        try:
            self._printDebug("Init fork...")

            if(self.pi is None):
                self.pi = pigpio.pi()

            self.stopMovement()

            self._printDebug("...done!")
            return True
        except Exception as err:
            self._printDebug("...failed --> " + str(err))
            return False


    def setForkPositionByManual(self):
        self._printDebug("Now you can set the position of the fork with the joystick...")
        while(True):
            self.i2cHandler.readSenseHatEvents()
            if(self.i2cHandler.isJoystickPressed("pressed","left")):
                self.moveLeft()
                continue

            if(self.i2cHandler.isJoystickPressed("pressed","right")):
                self.moveRight()
                continue

            if(self.i2cHandler.isJoystickPressed("released","left") or self.i2cHandler.isJoystickPressed("released","right")):
                self.stopMovement()
                continue

            if(self.i2cHandler.isJoystickPressed("pressed","middle")):
                break

            sleep(0.01)

        self.stopMovement()
        self._printDebug("Exit Forkdingens...")


    def stopMovement(self):
        self.pi.write(BCM_PIN_NR_FORK_MOT_LEFT, 0)
        self.pi.write(BCM_PIN_NR_FORK_MOT_RIGHT, 0)


    def moveLeft(self):
        self.pi.write(BCM_PIN_NR_FORK_MOT_LEFT, 1)
        self.pi.write(BCM_PIN_NR_FORK_MOT_RIGHT, 0)


    def moveRight(self):
        self.pi.write(BCM_PIN_NR_FORK_MOT_LEFT, 0)
        self.pi.write(BCM_PIN_NR_FORK_MOT_RIGHT, 1)


    def setPositionForNumber(self, number, drivingDirection):
        if(-1 < number and number < 6):
            if(drivingDirection is direction.LEFT): # Left parcour
                desiredDistance = self.buttonDistanceList[number]
                currDistance = self.i2cHandler.getDistanceLeftFront()

                if(desiredDistance < currDistance):
                    self.moveLeft()
                    print("Move left...")

                    while (desiredDistance < currDistance):
                        sleep(0.1)
                        currDistance = self.i2cHandler.getDistanceLeftFront()

                    self.stopMovement()
                else:
                    self.moveRight()
                    print("Move right...")
                    while (desiredDistance > currDistance):
                        sleep(0.1)
                        currDistance = self.i2cHandler.getDistanceLeftFront()

                    self.stopMovement()

                return True

            # Not tested!
            if (drivingDirection is direction.RIGHT): # Right parcour
                desiredDistance = self.buttonDistanceList[6 - number]
                currDistance = self.i2cHandler.getDistanceRightFront()

                if(desiredDistance < currDistance):
                    self.moveRight()
                    print("Move left...")

                    while (desiredDistance < currDistance):
                        sleep(0.1)
                        currDistance = self.i2cHandler.getDistanceRightFront()

                    self.stopMovement()
                else:
                    self.moveLeft()
                    print("Move right...")
                    while (desiredDistance > currDistance):
                        sleep(0.1)
                        currDistance = self.i2cHandler.getDistanceRightFront()

                    self.stopMovement()

                return True

        return False


    def startAutoCalibration(self):
        pass


    def _printDebug(self, message):
        if (__debug__):
            print("  {}: {}".format(self.__class__.__name__, message))