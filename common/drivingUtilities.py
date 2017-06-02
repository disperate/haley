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
from haleyenum import direction
import math

# Constants
TURN_VELOCITY_START                 = 0.5
TURN_VELOCITY_MAX                   = 50.0
LOOP_FREQUENCY                      = 10
DRIVE_UP_TICK_VALUE                 = 0.025
DRIVE_UP_RANGE_IN_DEGREES           = 15.0 # Marks drive-up range
SLOW_DOWN_RANGE_IN_DEGREES          = 15.0 # Marks slow-down range
SLOW_DOWN_STOP_OFFSET_IN_DEGREES    = 1.0
CORRECTION_VALUE_LEFT_TURN          = 1.0
CORRECTION_VALUE_RIGHT_TURN         = 1.0

PI                                  = 3.14 # More precision is not necessary for given size of ticks
PI_HALF                             = 1.57 # More precision is not necessary for given size of ticks
SINUS_PI_OFFSET                     = 0.4
SINUS_TICK_SIZE_DEFAULT             = 0.025
SINUS_TICK_SLEEP_MS                 = 10

FRONT_SENSOR_OFFSET                 = 59 # Measurement in mm (Distance between sensor and front-bumper) (Wood)

APPROACH_PATTERN_VERY_SLOW          = [50, 25, 10, 5] # for velocities between 0% & 25%
APPROACH_PATTERN_SLOW               = [75, 40, 20, 5] # for velocities between 25% & 50%
APPROACH_PATTERN_FAST               = [100, 80, 40, 15, 5] # for velocities between 50% & 75%
APPROACH_PATTERN_VERY_FAST          = [200, 80, 40, 15, 5] # for velocities between 75% & 100%

class DrivingUtilities():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self, i2cHandler, motorDriver):
        self._printDebug("Init...")
        self.i2cHandler = i2cHandler
        self.motorDriver = motorDriver
        self._printDebug("...done!")

        return


    # Used functions
    # --------------------------------------------------------------------------
    def accelerate(self, requestedVelocity):
        sinusTickSize = self._getOptimalTickSize(self.motorDriver.getCurrVelocityLeft(), requestedVelocity)
        self._accelerate(requestedVelocity, sinusTickSize)

        return


    def stop(self):
        sinusTickSize = self._getOptimalTickSize(self.motorDriver.getCurrVelocityLeft(), 0)
        self._stop(sinusTickSize)

        return


    def driveByTime(self, timeInMilliseconds, requestedVelocity):
        # Set optimal ticksize
        sinusTickSize = self._getOptimalTickSize(self.motorDriver.getCurrVelocityLeft(), requestedVelocity)

        # Calculate the time, which haley drives with the requested velocity
        timeInRequestedVelocity = timeInMilliseconds - (((PI_HALF - SINUS_PI_OFFSET) / sinusTickSize) * SINUS_TICK_SLEEP_MS * 2)

        if(timeInRequestedVelocity < 0.0):
            sinusTickSize = self._getOptimalTickSize(self.motorDriver.getCurrVelocityLeft(), requestedVelocity / 2)
            timeInRequestedVelocity = timeInMilliseconds - (((PI_HALF - SINUS_PI_OFFSET) / sinusTickSize) * SINUS_TICK_SLEEP_MS * 2)

        self._printDebug("driveByTime(): sinusTickSize = {}, timeInRequestedVelocity = {}".format(sinusTickSize, timeInRequestedVelocity))

        self._accelerate(requestedVelocity, sinusTickSize)
        sleep((1/1000) * timeInRequestedVelocity)
        self._stop(sinusTickSize)

        return


    def _getOptimalTickSize(self, currentVelocity, targetVelocity):
        deltaVelocity = abs(targetVelocity - currentVelocity)

        if (deltaVelocity > 100):
            return SINUS_TICK_SIZE_DEFAULT
        elif (deltaVelocity > 50):
            return SINUS_TICK_SIZE_DEFAULT * 2
        elif (deltaVelocity > 25):
            return SINUS_TICK_SIZE_DEFAULT * 4
        else:
            return SINUS_TICK_SIZE_DEFAULT * 8


    def _accelerate(self, targetVelocity, sinusTickSize = SINUS_TICK_SIZE_DEFAULT):
        self._printDebug("_accelerate(): sinusTickSize = {}".format(sinusTickSize))
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        if((int(initialVelocityLeft) + int(initialVelocityRight)) == 0 ):
            # Starting from velocity 0
            currPiValue = SINUS_PI_OFFSET

            while (currPiValue < PI_HALF):
                self.motorDriver.setVelocityLeft(targetVelocity * math.sin(currPiValue))
                self.motorDriver.setVelocityRight(targetVelocity * math.sin(currPiValue))
                currPiValue = currPiValue + sinusTickSize
                sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)
        else:
            # Starting from velocity != 0
            deltaVelocityLeft = targetVelocity - initialVelocityLeft
            deltaVelocityRight = targetVelocity - initialVelocityRight

            currPiValue = 0

            while (currPiValue < PI):
                self.motorDriver.setVelocityLeft(initialVelocityLeft + deltaVelocityLeft * ((- math.cos(currPiValue) / 2) + 0.5))
                self.motorDriver.setVelocityRight(initialVelocityRight + deltaVelocityRight * ((- math.cos(currPiValue) / 2) + 0.5))
                currPiValue = currPiValue + 2 * sinusTickSize
                sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)

        return


    def _stop(self, sinusTickSize = SINUS_TICK_SIZE_DEFAULT):
        self._printDebug("_stop(): sinusTickSize = {}".format(sinusTickSize))
        currPiValue = PI_HALF
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        while (currPiValue < (PI - SINUS_PI_OFFSET)):
            self.motorDriver.setVelocityLeft(initialVelocityLeft * math.sin(currPiValue))
            self.motorDriver.setVelocityRight(initialVelocityRight * math.sin(currPiValue))
            currPiValue = currPiValue + sinusTickSize
            sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)

        self.motorDriver.stop()

        return


    def approachWallAndStop(self, relativeDistanceInMillimeter):
        divisor = 1
        approachPattern = None
        realDistance = relativeDistanceInMillimeter + FRONT_SENSOR_OFFSET
        self._printDebug("approachWallAndStop(): Required distance --> {}mm".format(relativeDistanceInMillimeter + FRONT_SENSOR_OFFSET))
        currDiff = self.i2cHandler.getDistanceFront() - realDistance
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        # Set approaching pattern for different velocities
        if(75.0 < abs(initialVelocityLeft)):
            approachPattern = APPROACH_PATTERN_VERY_FAST
            self._printDebug("approachWallAndStop(): Set approaching pattern VERY_FAST")
        elif (50.0 < abs(initialVelocityLeft)):
            approachPattern = APPROACH_PATTERN_FAST
            self._printDebug("approachWallAndStop(): Set approaching pattern FAST")
        elif (25.0 < abs(initialVelocityLeft)):
            approachPattern = APPROACH_PATTERN_SLOW
            self._printDebug("approachWallAndStop(): Set approaching pattern SLOW")
        else:
            approachPattern = APPROACH_PATTERN_VERY_SLOW
            self._printDebug("approachWallAndStop(): Set approaching pattern VERY_SLOW")

        # Use pattern for approaching wall
        for triggerDistance in approachPattern:
            while (True):
                currDiff = self.i2cHandler.getDistanceFront() - realDistance
                if (currDiff < triggerDistance):
                    break
                sleep(0.1)

            divisor = divisor * 2
            self.motorDriver.setVelocityLeft(initialVelocityLeft / divisor)
            self.motorDriver.setVelocityRight(initialVelocityRight / divisor)

        while(True):
            currDiff = self.i2cHandler.getDistanceFront() - realDistance
            if (currDiff <= 0):
                break

            sleep(0.1)

        self.motorDriver.stop()
        self._printDebug("approachWallAndStop(): Reached distance --> {}mm".format(self.i2cHandler.getDistanceFront()))

        return


    def turn(self, angle):
        if(angle is not None):
            currVelocity = TURN_VELOCITY_START

            # Left turn
            if (angle < 0.0):
                self._printDebug("Turn {}° to the left...".format(abs(angle)))
                self.i2cHandler.resetRelativeYaw()

                adjustedAngle = angle * CORRECTION_VALUE_LEFT_TURN

                while (True):
                    currDelta = abs(adjustedAngle) - abs(self.i2cHandler.currRelativeYaw)

                    # Drive-Up
                    if (currDelta > (abs(adjustedAngle) - DRIVE_UP_RANGE_IN_DEGREES)):
                        if (currVelocity < TURN_VELOCITY_MAX):
                            currVelocity = currVelocity + DRIVE_UP_TICK_VALUE
                            self.motorDriver.setVelocityLeft(-currVelocity)
                            self.motorDriver.setVelocityRight(currVelocity)
                            continue

                    # Stop
                    if (currDelta < SLOW_DOWN_STOP_OFFSET_IN_DEGREES):
                        self.motorDriver.stop()
                        break

                    # Slow-Down
                    if (currDelta <= SLOW_DOWN_RANGE_IN_DEGREES):
                        currVelocity = (TURN_VELOCITY_MAX / SLOW_DOWN_RANGE_IN_DEGREES) * currDelta
                        self.motorDriver.setVelocityLeft(-currVelocity)
                        self.motorDriver.setVelocityRight(currVelocity)
                        continue

                    sleep(1 / LOOP_FREQUENCY)

                self._printDebug("...done!")

            if(angle > 0.0):
                self._printDebug("Turn {}° to the right...".format(abs(angle)))
                self.i2cHandler.resetRelativeYaw()

                adjustedAngle = angle * CORRECTION_VALUE_RIGHT_TURN

                while (True):
                    currDelta = abs(adjustedAngle) - abs(self.i2cHandler.currRelativeYaw)

                    # Drive-Up
                    if (currDelta > (abs(adjustedAngle) - DRIVE_UP_RANGE_IN_DEGREES)):
                        if (currVelocity < TURN_VELOCITY_MAX):
                            currVelocity = currVelocity + DRIVE_UP_TICK_VALUE
                            self.motorDriver.setVelocityLeft(currVelocity)
                            self.motorDriver.setVelocityRight(-currVelocity)
                            continue

                    # Stop
                    if (currDelta < SLOW_DOWN_STOP_OFFSET_IN_DEGREES):
                        self.motorDriver.stop()
                        break

                    # Slow-Down
                    if (currDelta <= SLOW_DOWN_RANGE_IN_DEGREES):
                        currVelocity = (TURN_VELOCITY_MAX / SLOW_DOWN_RANGE_IN_DEGREES) * currDelta
                        self.motorDriver.setVelocityLeft(currVelocity)
                        self.motorDriver.setVelocityRight(-currVelocity)
                        continue

                    sleep(1 / LOOP_FREQUENCY)

                self._printDebug("...done!")
        return


    def adjustToWall(self, _direction):

        while (True):
            if _direction is direction.direction.RIGHT:
                frontDistance = self.i2cHandler.getDistanceLeftFront()
                backDistance = self.i2cHandler.getDistanceLeftBack()
                diff = frontDistance - backDistance

            if _direction is direction.direction.LEFT:
                frontDistance = self.i2cHandler.getDistanceRightFront()
                backDistance = self.i2cHandler.getDistanceRightBack()
                diff = backDistance - frontDistance

            if abs(diff) > 10:
                if diff > 0:
                    print("Correcting angle, distance diff was: " + str(
                        diff))
                    self.turn(0.3)
                else:
                    print("Correcting angle, distance diff was: " + str(
                        diff))
                    self.turn(-0.3)

                sleep(0.3)
            else:
                print("accepted diff: " + str(diff))
                break

        return


    def _printDebug(self, message):
        if (__debug__):
            print("    {}: {}".format(self.__class__.__name__, message))

        return