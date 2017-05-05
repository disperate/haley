#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        DrivingUtilities
# Description:  Utilities to drive like turn etc.
#
#------------------------------------------------------------------------------
#
#
# Vmax   .................................
#       /|                               |\
#      / |                               | \
#     /  |                               |  \
# 0 ------------------------------------------------>
#
#    |---|                               |---|
#  Start-Range                         Stop-Range
#
#

# Imports
from time import sleep
import math

# Constants
VELOCITY_START                      = 0.5
VELOCITY_MAX                        = 50.0
LOOP_FREQUENCY                      = 10
DRIVE_UP_TICK_VALUE                 = 0.025
DRIVE_UP_RANGE_IN_DEGREES           = 15.0 # Marks drive-up range
SLOW_DOWN_RANGE_IN_DEGREES          = 15.0 # Marks slow-down range
SLOW_DOWN_STOP_OFFSET_IN_DEGREES    = 1.0
CORRECTION_VALUE_LEFT_TURN          = 1.0
CORRECTION_VALUE_RIGHT_TURN         = 1.0

class DrivingUtilities():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self, i2cHandler, motorDriver):
        self._printDebug("Init...")
        self.i2cHandler = i2cHandler
        self.motorDriver = motorDriver
        self._printDebug("...done!")


    def driveDistanceByTime(self, timeInMilliseconds, velocity):
        if((abs(velocity) <= 100.0) and (timeInMilliseconds > 0)):
            counter = 0.5
            counter_ticks = 0.05

            # Start up
            while(counter < (math.pi/2)):
                self.motorDriver.setVelocityLeft(velocity * math.sin(counter))
                self.motorDriver.setVelocityRight(velocity * math.sin(counter))
                counter = counter + counter_ticks
                sleep(0.01)

            # Drive
            self.motorDriver.setVelocityLeft(velocity)
            self.motorDriver.setVelocityRight(velocity)
            sleep((1 / 1000) * timeInMilliseconds)

            # Slow down
            while(counter > 0.25):
                self.motorDriver.setVelocityLeft(velocity * math.sin(counter))
                self.motorDriver.setVelocityRight(velocity * math.sin(counter))
                counter = counter - counter_ticks
                sleep(0.01)

            self.motorDriver.stopDriver()


    def turn(self, angle):
        if(angle is not None):
            currVelocity = VELOCITY_START

            # Left turn
            if (angle < 0.0):
                self._printDebug("Turn {}° to the left...".format(abs(angle)))
                self.i2cHandler.resetRelativeYaw()

                adjustedAngle = angle * CORRECTION_VALUE_LEFT_TURN

                while (True):
                    currDelta = abs(adjustedAngle) - abs(self.i2cHandler.currRelativeYaw)

                    # Drive-Up
                    if (currDelta > (abs(adjustedAngle) - DRIVE_UP_RANGE_IN_DEGREES)):
                        if (currVelocity < VELOCITY_MAX):
                            currVelocity = currVelocity + DRIVE_UP_TICK_VALUE
                            self.motorDriver.setVelocityLeft(-currVelocity)
                            self.motorDriver.setVelocityRight(currVelocity)
                            continue

                    # Stop
                    if (currDelta < SLOW_DOWN_STOP_OFFSET_IN_DEGREES):
                        self.motorDriver.stopDriver()
                        break

                    # Slow-Down
                    if (currDelta <= SLOW_DOWN_RANGE_IN_DEGREES):
                        currVelocity = (VELOCITY_MAX / SLOW_DOWN_RANGE_IN_DEGREES) * currDelta
                        self.motorDriver.setVelocityLeft(-currVelocity)
                        self.motorDriver.setVelocityRight(currVelocity)
                        continue

                    sleep(1 / LOOP_FREQUENCY)

            if(angle > 0.0):
                self._printDebug("Turn {}° to the right...".format(abs(angle)))
                self.i2cHandler.resetRelativeYaw()

                adjustedAngle = angle * CORRECTION_VALUE_RIGHT_TURN

                while (True):
                    currDelta = abs(adjustedAngle) - abs(self.i2cHandler.currRelativeYaw)

                    # Drive-Up
                    if (currDelta > (abs(adjustedAngle) - DRIVE_UP_RANGE_IN_DEGREES)):
                        if (currVelocity < VELOCITY_MAX):
                            currVelocity = currVelocity + DRIVE_UP_TICK_VALUE
                            self.motorDriver.setVelocityLeft(currVelocity)
                            self.motorDriver.setVelocityRight(-currVelocity)
                            continue

                    # Stop
                    if (currDelta < SLOW_DOWN_STOP_OFFSET_IN_DEGREES):
                        self.motorDriver.stopDriver()
                        break

                    # Slow-Down
                    if (currDelta <= SLOW_DOWN_RANGE_IN_DEGREES):
                        currVelocity = (VELOCITY_MAX / SLOW_DOWN_RANGE_IN_DEGREES) * currDelta
                        self.motorDriver.setVelocityLeft(currVelocity)
                        self.motorDriver.setVelocityRight(-currVelocity)
                        continue

                    sleep(1 / LOOP_FREQUENCY)


    def _printDebug(self, message):
        if (__debug__):
            print("    {}: {}".format(self.__class__.__name__, message))