#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.03.31
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        SenseHatAdapter
# Description:  Provides access to the SenseHat-Modul
#------------------------------------------------------------------------------

# Imports
from sense_hat import SenseHat


class SenseHatAdapter():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self.orientationPitch = 0.0
        self.orientationRoll = 0.0
        self.orientationYaw = 0.0
        self.displayBuffer = [[0, 0, 0]] * 64
        self.ForeColor = [255,255,255]          # White
        self.ForeColorIdle = [255, 127, 39]     # Orange
        self.ForeColorRunning = [0, 255, 0]     # Green
        self.ForeColorStop = [255, 0, 0]        # Red
        self.sense = None

        self.initSenseHat()


    # Funktions
    # --------------------------------------------------------------------------
    def initSenseHat(self):
        """
        Description: Initializes the sense-hat
        Returns:     Boolean
        """
        try:
            self.sense = SenseHat()
            self.sense.set_imu_config(False, True, False) # Gyroscope only
            return True
        except:
            return False


    def refreshOrientation(self):
        """
        Description: Reads the IMU-values (pitch/roll/yaw) of the Sense-Hat
        """
        try:
            currGyroData = self.sense.get_orientation()

            if currGyroData is not None:
                self.orientationPitch = currGyroData.get('pitch')
                self.orientationRoll = currGyroData.get('roll')
                self.orientationYaw = currGyroData.get('yaw')

            return True
        except:
            return False


    def getPitch(self):
        """
        Description: Gets the pitch-value from the last forced measurement
        Returns:     Float
        """
        return self.orientationPitch


    def getRoll(self):
        """
        Description: Gets the roll-value from the last forced measurement
        Returns:     Float
        """
        return self.orientationRoll


    def getYaw(self):
        """
        Description: Gets the yaw-value from the last forced measurement
        Returns:     Float
        """
        return self.orientationYaw


    def drawChar(self, newChar, newColor):
        """
        Description: Draws a character, mostly a number in the display-buffer
        Args:        1. Character as string
                     2. Color as simple list[] --> [R, G, B]
        Returns:     Float
        """
        charCode = self.getCharCode(newChar)

        for pixelPosition in charCode:
            self.displayBuffer[pixelPosition] = newColor

        return


    def clearDisplay(self):
        """
        Description: Clears the whole RGB-Display
        """
        self.sense.clear(0,0,0)

        return


    def refreshDisplay(self):
        """
        Description: Draws buffer into RGB-Display
        """
        self.sense.set_pixels(self.displayBuffer)

        return


    def setStatusLeds(self, listOfStates):
        """
        Description: Gets a whole list of states and calls setStatusLed for
                     every item.
        Args:        1. list with states
        """
        if(listOfStates is not None):
            count = len(listOfStates)

            for x in range(count):
                self.setStatusLed(x, listOfStates[x])
        return


    def setStatusLed(self, newNumber, newState):
        """
        Description: Sets the status for a given module/whatever and shows it
                     at the bottom of the RGB-Display.
                     Eight states from 0-7 are adjustable.
                     Possible states are:
                     "IDLE", "RUNNING", "STOPPED" -> Orange, Green, Red
        Args:        1. ID as integer (0-7)
                     2. Status as integer (0=IDLE, 1=RUNNING, 2=STOPPED)
        """
        if(0 <= newNumber and newNumber <= 7):
            pixelPosition = [56, 57, 58, 59, 60, 61, 62, 63]
            currentColor = self.ForeColorIdle

            if(newState == 1):
                currentColor = self.ForeColorRunning
            elif(newState == 2):
                currentColor = self.ForeColorStop

            self.displayBuffer[pixelPosition[newNumber]] = currentColor

        return


    def setRomanNumber(self, newNumber):
        """
        Description: Shows a roman number ont the RGB-Display.
                     Possible Numbers are: "I, II, III, IV, V".
                     Clears automatically the area for the number.
        Args:        1. Number as integer or string
        """
        self.drawChar("clear", [0, 0, 0])
        self.drawChar(str(newNumber), self.ForeColor)

        return


    def getCharCode(self, newChar):
        """
        Description: Draw-Matrix for the numbers
        Returns:     List[]
        """
        return {
            "0": [10, 11, 12, 13, 18, 21, 26, 29, 34, 37, 42, 43, 44, 45],
            "1": [13, 21, 29, 37, 45],
            "2": [10, 11, 12, 13, 21, 26, 27, 28, 29, 34, 42, 43, 44, 45],
            "3": [10, 11, 12, 13, 21, 27, 28, 29, 37, 42, 43, 44, 45],
            "4": [10, 13, 18, 21, 26, 27, 28, 29, 37, 45],
            "5": [10, 11, 12, 13, 18, 26, 27, 28, 29, 37, 42, 43, 44, 45],
            "clear": [10, 11, 12, 13, 18, 21, 26, 27, 28, 29, 34, 37, 42, 43, 44, 45]
        }.get(newChar, [0])  # 0 is default