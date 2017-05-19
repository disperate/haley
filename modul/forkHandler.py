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
        counter = 0
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

            if(counter % 20 == 0):
                self._printDebug("Current distance-values: LF -> {}mm, RF -> {}mm".format(self.i2cHandler.getDistanceLeftFront(), self.i2cHandler.getDistanceRightFront()))
                counter = 0

            counter = counter + 1
            sleep(0.05)

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
        self._printDebug("Enter setPositionForNumber()...")
        if(-1 < number and number < 6):
            self._printDebug("Number is {}".format(number))
            if(drivingDirection is direction.RIGHT): # Left parcour
                self._printDebug("Direction is RIGHT (Left parcour)")
                desiredDistance = self.buttonDistanceList[number]
                currDistance = self.i2cHandler.getDistanceLeftFront()

                self._printDebug("Desired distance is: {}mm".format(desiredDistance))
                self._printDebug("Current distance LF before: {}mm".format(self.i2cHandler.getDistanceLeftFront()))
                if(desiredDistance < currDistance):
                    self.moveLeft()
                    self._printDebug("Move fork to the left...")

                    while (desiredDistance < currDistance):
                        sleep(0.05)
                        currDistance = self.i2cHandler.getDistanceLeftFront()

                    self.stopMovement()
                else:
                    self.moveRight()
                    self._printDebug("Move fork to the right...")
                    while (desiredDistance > currDistance):
                        sleep(0.05)
                        currDistance = self.i2cHandler.getDistanceLeftFront()

                    self.stopMovement()

                self._printDebug("Current distance LF after: {}mm".format(self.i2cHandler.getDistanceLeftFront()))
                return True

            # Not tested!
            if (drivingDirection is direction.LEFT): # Right parcour
                self._printDebug("Direction is LEFT (Right parcour)")
                desiredDistance = self.buttonDistanceList[6 - number]
                currDistance = self.i2cHandler.getDistanceRightFront()
                self._printDebug("Desired distance is: {}mm".format(desiredDistance))
                self._printDebug("Current distance RF before: {}mm".format(self.i2cHandler.getDistanceRightFront()))
                if(desiredDistance < currDistance):
                    self.moveRight()
                    self._printDebug("Move fork to the left...")

                    while (desiredDistance < currDistance):
                        sleep(0.05)
                        currDistance = self.i2cHandler.getDistanceRightFront()

                    self.stopMovement()
                else:
                    self.moveLeft()
                    self._printDebug("Move for to the right...")
                    while (desiredDistance > currDistance):
                        sleep(0.05)
                        currDistance = self.i2cHandler.getDistanceRightFront()

                    self.stopMovement()

                self._printDebug("Current distance LF after: {}mm".format(self.i2cHandler.getDistanceRightFront()))
                return True

        return False


    def startAutoCalibration(self):
        pass


    def _printDebug(self, message):
        if (__debug__):
            print("  {}: {}".format(self.__class__.__name__, message))