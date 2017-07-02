#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Autor:        Urs Stoeckli
# -------------------------------------------------------------------------------
# Class:        Init
# Description:  Initialisierung des Tastendrückers und Offset der Distanzsensoren
#
#               Solange der Kippschalter auf Konfig steht, wird auf einen
#               Tastendruck zwischen 4..5s gewartet.
#               Sobald dies erkannt wird, fährt der Tastendrücker auf die
#               Mittelstellung und ermittelt den Offset aller Distanzsensoren.
#
# -------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------
#
#
# ------------------------------------------------------------------------------

import time
from time import sleep

import pigpio

import config
from modul import fork
from modul.i2cModules import distanceSensorAdapter

# Constants
MAX_TIME = 4.0
MIN_TIME = 3.0


class initActivity(object):
    # *** Konstruktor ***
    def __init__(self, fsm, i2c):
        super().__init__()
        self._i2c = i2c
        self._fork = fork.fork(self._i2c)
        self._pi = pigpio.pi()

        if self.waitForButton() > MIN_TIME:  # Schalter auf Konfig und Taste zwischen >4s betätigt
            print("Calibrating...")
            self.initFork()  # ja, Tastendrücker initialisieren
            self.getDistOffset()  # Offsets der Sensoren ermitteln

        while (self._pi.read(config.BUTTON)):
            print("LB: {:4d}, LF: {:4d}, F: {:4d}, RF: {:4d}, RB: {:4d}".format(
                self._i2c.getDistanceLeftBack(),
                self._i2c.getDistanceLeftFront(),
                self._i2c.getDistanceFront(),
                self._i2c.getDistanceRightFront(),
                self._i2c.getDistanceRightBack()))
            sleep(0.11)

        fsm.setupComplete()  # Setup beenden

    # Wartet solange Kippschalter auf Konfig (Mittelstellung) bis die Taste zwischen MIN_TIME und MAX_TIME betätigt wird.
    # Vorgang wird beendet wenn der Kippschalter aus der Mittelstellung geht, die Taste zwischen MIN_TIME und MAX_TIME
    # losgelassen wird oder die Taste länger als MAX_TIME gehalten wird.
    #
    # Rückgabe: 0 falls Kippschalter nicht auf Mittelstellung
    #           Betätigungsdauer (MIN_TIME...MAX_TIME) falls Kippschalter auf Mittelstellung
    def waitForButton(self):
        pressedTime = 0
        buttonLast = False
        startTime = time.time()
        while self._pi.read(config.SWITCH1) and self._pi.read(config.SWITCH2) and (pressedTime < MIN_TIME):
            buttonNew = not self._pi.read(config.BUTTON)
            if not buttonNew:
                startTime = time.time()
            if not buttonNew and buttonLast:
                pressedTime = time.time() - startTime
            sleep(0.05)
            if (time.time() - startTime) > MAX_TIME:
                pressedTime = time.time() - startTime
        if self._pi.read(config.SWITCH1) != self._pi.read(config.SWITCH2):
            return 0
        return pressedTime

    # Fährt den Tastendrücker auf die Mittelstellung (Differenz zwischen linker und rechter Distanz = 0)
    # fährt die letzen 5mm nur schrittweise, um nicht zu weit zu fahren
    # Am Schluss wird 6x gemessen und geprüft ob die mittlere Abweichung < 0.5mm ist
    def initFork(self):
        moveButtonSlider = True
        while moveButtonSlider:

            left = self._i2c.getDistanceLeftFront()
            right = self._i2c.getDistanceRightFront()
            if abs(left - right) < 5:
                self._fork.stopMovement()
                result = self.getMeanDist(4)
                left = result[distanceSensorAdapter.SENSOR_LEFT_FRONT]
                right = result[distanceSensorAdapter.SENSOR_RIGHT_FRONT]
            if abs(left - right):
                if (left > right):
                    self._fork.moveLeft()
                    if (abs(left - right) < 5):
                        sleep(abs(left - right) * 0.1)
                        self._fork.stopMovement()
                else:
                    self._fork.moveRight()
                    if (abs(left - right) < 5):
                        sleep(abs(left - right) * 0.1)
                        self._fork.stopMovement()
            else:
                self._fork.stopMovement()
                result = self.getMeanDist(8)
                if abs(result[distanceSensorAdapter.SENSOR_LEFT_FRONT] - result[
                    distanceSensorAdapter.SENSOR_RIGHT_FRONT]) < 4:
                    print("LB: {:4d}, LF: {:4d}, F: {:4d}, RF: {:4d}, RB: {:4d}".format(
                        self._i2c.getDistanceLeftBack(),
                        self._i2c.getDistanceLeftFront(),
                        self._i2c.getDistanceFront(),
                        self._i2c.getDistanceRightFront(),
                        self._i2c.getDistanceRightBack()))
                    moveButtonSlider = False
            sleep(0.01)

    def getMeanDist(self, anzMess=8):
        sumRightFront = 0
        sumLeftFront = 0
        sumFront = 0
        sumRightBack = 0
        sumLeftBack = 0
        for i in range(0, anzMess):
            sumLeftBack += self._i2c.getDistanceLeftBack()
            sumLeftFront += self._i2c.getDistanceLeftFront()
            sumFront += self._i2c.getDistanceFront()
            sumRightBack += self._i2c.getDistanceRightBack()
            sumRightFront += self._i2c.getDistanceRightFront()
            sleep(0.11)

        return [sumLeftBack / anzMess, sumLeftFront / anzMess, sumFront / anzMess, sumRightFront / anzMess,
                sumRightBack / anzMess]

    def getDistOffset(self):
        result = self.getMeanDist(8)

        # TODO save offsets to i2c Modul
        offsetLeftFront = result[distanceSensorAdapter.SENSOR_LEFT_BACK] - 91
        offsetLeftBack = result[distanceSensorAdapter.SENSOR_LEFT_FRONT] - 90
        offsetRightFront = result[distanceSensorAdapter.SENSOR_RIGHT_FRONT] - 91
        offsetRightBack = result[distanceSensorAdapter.SENSOR_RIGHT_BACK] - 90

        print("OffsetLeftFront:  " + str(offsetLeftFront))
        print("OffsetLeftBack:   " + str(offsetLeftBack))
        print("OffsetRightFront: " + str(offsetRightFront))
        print("OffsetRightBack:  " + str(offsetRightBack))
