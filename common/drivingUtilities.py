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
SINUS_TICK_SIZE                     = 0.025
SINUS_TICK_SLEEP_MS                 = 10

FRONT_SENSOR_OFFSET                 = 45 # Measurement in mm (Distance between sensor and front-bumper) (Wood)


class DrivingUtilities():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self, i2cHandler, motorDriver):
        self._printDebug("Init...")
        self.i2cHandler = i2cHandler
        self.motorDriver = motorDriver
        self._printDebug("...done!")


    # Used functions
    # --------------------------------------------------------------------------
    def driveByTime(self, timeInMilliseconds, velocity):
        timeInRequestedVelocity = timeInMilliseconds - (((PI_HALF - SINUS_PI_OFFSET) / SINUS_TICK_SIZE) * SINUS_TICK_SLEEP_MS * 2)

        self.accelerate(velocity)
        sleep((1/1000) * timeInRequestedVelocity)
        self.stop()

        return


    def accelerate(self, targetVelocity):
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        if((int(initialVelocityLeft) + int(initialVelocityRight)) == 0 ):
            # Starting from velocity 0
            currPiValue = SINUS_PI_OFFSET

            while (currPiValue < PI_HALF):
                self.motorDriver.setVelocityLeft(targetVelocity * math.sin(currPiValue))
                self.motorDriver.setVelocityRight(targetVelocity * math.sin(currPiValue))
                currPiValue = currPiValue + SINUS_TICK_SIZE
                sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)
        else:
            # Starting from velocity != 0
            deltaVelocityLeft = targetVelocity - initialVelocityLeft
            deltaVelocityRight = targetVelocity - initialVelocityRight

            currPiValue = 0

            while (currPiValue < PI):
                self.motorDriver.setVelocityLeft(initialVelocityLeft + deltaVelocityLeft * ((- math.cos(currPiValue) / 2) + 0.5))
                self.motorDriver.setVelocityRight(initialVelocityRight + deltaVelocityRight * ((- math.cos(currPiValue) / 2) + 0.5))
                currPiValue = currPiValue + 2 * SINUS_TICK_SIZE
                sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)

        return


    def stop(self):
        currPiValue = PI_HALF
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        while (currPiValue < (PI - SINUS_PI_OFFSET)):
            self.motorDriver.setVelocityLeft(initialVelocityLeft * math.sin(currPiValue))
            self.motorDriver.setVelocityRight(initialVelocityRight * math.sin(currPiValue))
            currPiValue = currPiValue + SINUS_TICK_SIZE
            sleep((1 / 1000) * SINUS_TICK_SLEEP_MS)

        self.motorDriver.stop()
        return


    def approachWallAndStop(self, relativeDistanceInMillimeter):
        realDistance = relativeDistanceInMillimeter + FRONT_SENSOR_OFFSET
        currDiff = self.i2cHandler.getDistanceFront() - realDistance
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        while(True):
            currDiff = self.i2cHandler.getDistanceFront() - realDistance
            if (currDiff < 100):
                break
            sleep(0.1)

        self.motorDriver.setVelocityLeft(initialVelocityLeft / 2)
        self.motorDriver.setVelocityRight(initialVelocityRight / 2)

        while(True):
            currDiff = self.i2cHandler.getDistanceFront() - realDistance
            if (currDiff < 50):
                break
            sleep(0.1)

        self.motorDriver.setVelocityLeft(initialVelocityLeft / 4)
        self.motorDriver.setVelocityRight(initialVelocityRight / 4)

        while(True):
            currDiff = self.i2cHandler.getDistanceFront() - realDistance
            if (currDiff < 25):
                break
            sleep(0.1)

        self.motorDriver.setVelocityLeft(initialVelocityLeft / 8)
        self.motorDriver.setVelocityRight(initialVelocityRight / 8)

        while(True):
            currDiff = self.i2cHandler.getDistanceFront() - realDistance
            if (currDiff <= 0):
                break

            sleep(0.1)

        self.motorDriver.stop()
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

    # Experimental
    # --------------------------------------------------------------------------
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

            self.motorDriver.stop()


    def approachWallAndStopNew(self, relativeDistanceInMillimeter):
        realDistance = relativeDistanceInMillimeter + FRONT_SENSOR_OFFSET
        currDiff = self.i2cHandler.getDistanceFront() - realDistance
        initialVelocityLeft = self.motorDriver.getCurrVelocityLeft()
        initialVelocityRight = self.motorDriver.getCurrVelocityRight()

        for x in range(1, 8):
            self._printDebug("Current velocity: {}".format(self.motorDriver.getCurrVelocityLeft()))
            while (True):
                currDiff = self.i2cHandler.getDistanceFront() - realDistance
                if (currDiff < int(100 / x)):
                    break
                sleep(0.05)

            self.motorDriver.setVelocityLeft(initialVelocityLeft / (2 * x))
            self.motorDriver.setVelocityRight(initialVelocityRight / (2 * x))

        self.motorDriver.stop()