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

# Imports
import time
from time import sleep
from modul import forkHandler

import pigpio

import config

# Constants
MAX_TIME = 4.0
MIN_TIME = 3.0


#
class initActivity(object):
    # *** Konstruktor ***
    def __init__(self, fsm, i2c):
        super().__init__()
        self._i2c = i2c
        self._fork = forkHandler.Fork(self._i2c)
        self._pi = pigpio.pi()

        if self.waitForButton() > MIN_TIME:  # Schalter auf Konfig und Taste zwischen >4s betätigt
            print("Calibrating...")
            self.initFork()  # ja, Tastendrücker initialisieren
            self.getDistOffset()  # Offsets der Sensoren ermitteln

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

            if (self._i2c.getDistanceLeftFront() - self._i2c.getDistanceRightFront()):
                if (self._i2c.getDistanceLeftFront() > self._i2c.getDistanceRightFront()):
                    self._fork.moveLeft()
                    if (abs(self._i2c.getDistanceLeftFront() - self._i2c.getDistanceRightFront()) < 5):
                        sleep(0.01)
                        self._fork.stopMovement()
                        sleep(0.02)
                else:
                    self._fork.moveRight()
                    if (abs(self._i2c.getDistanceLeftFront() - self._i2c.getDistanceRightFront()) < 5):
                        sleep(0.01)
                        self._fork.stopMovement()
                        sleep(0.02)
            else:
                self._fork.stopMovement()
                sumDiff = 0
                for i in range(0, 5):
                    sumDiff += abs(self._i2c.getDistanceLeftFront() - self._i2c.getDistanceRightFront())
                    sleep(0.1)
                if sumDiff < 6:
                    print("LEFTFRONT: " + str(self._i2c.getDistanceLeftFront()))
                    print("RIGHTFRONT: " + str(self._i2c.getDistanceRightFront()))
                    moveButtonSlider = False
            sleep(0.01)

    def getDistOffset(self):
        sumRightFront = 0
        sumLeftFront = 0
        sumRightBack = 0
        sumLeftBack = 0
        for i in range(0, 7):
            sumLeftBack += self._i2c.getDistanceLeftBack()
            sumLeftFront += self._i2c.getDistanceLeftFront()
            sumRightBack += self._i2c.getDistanceRightBack()
            sumRightFront += self._i2c.getDistanceRightFront()
            sleep(0.1)

        #TODO replace 40 with messured offset
        #TODO save offsets to i2c Modul
        offsetLeftFront = sumLeftFront / 8 - 93
        offsetLeftBack = sumLeftBack / 8 - 94
        offsetRightFront = sumRightFront / 8 - 93
        offsetRightBack = sumRightBack / 8 - 94
        print("OffsetLeftFront:  " + str(offsetLeftFront))
        print("OffsetLeftBack:   " + str(offsetLeftBack))
        print("OffsetRightFront: " + str(offsetRightFront))
        print("OffsetRightBack:  " + str(offsetRightBack))

