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
from threading import Thread
from time import sleep

# Constants
MAX_TIME = 5.0
MIN_TIME = 4.0

#
class initActivity(Object):
    # *** Konstruktor ***
    def __init__(self, fsm, i2c, buttonpresser):
        super().__init__()
        self._i2c = i2c
        self._buttonpresser = buttonpresser

        if self.waitForButton() > 4.0:  # Schalter auf Konfig und Taste zwischen >4s betätigt
            initFork()                  # ja, Tastendrücker initialisieren
            getDistOffset()             # Offsets der Sensoren ermitteln

        fsm.setupComplete()             # Setup beenden

    # Wartet solange Kippschalter auf Konfig (Mittelstellung) bis die Taste zwischen MIN_TIME und MAX_TIME betätigt wird.
    # Vorgang wird beendet wenn der Kippschalter aus der Mittelstellung geht, die Taste zwischen MIN_TIME und MAX_TIME
    # losgelassen wird oder die Taste länger als MAX_TIME gehalten wird.
    #
    # Rückgabe: 0 falls Kippschalter nicht auf Mittelstellung
    #           Betätigungsdauer (MIN_TIME...MAX_TIME) falls Kippschalter auf Mittelstellung
    def waitForButton(self):
        pressedTime = 0
        buttonLast = False;
        while self._pi.read(config.SWITCH1) and self._pi.read(config.SWITCH2) and (pressedTime < MIN_TIME):
            buttonNew = not self._pi.read(config.BUTTON)
            if buttonNew and not buttonLast:
                startTime = time.time()
            if not buttonNew and buttonLast:
                pressedTime = time.time() - startTime;
            sleep(0.05)
            if (time.time() - startTime) > MAX_TIME:
                pressedTime = time.time() - startTime
        if self._pi.read(config.SWITCH1) == self._pi.read(config.SWITCH2):
            return 0
        return pressedTime

    # Fährt den Tastendrücker auf die Mittelstellung (Differenz zwischen linker und rechter Distanz = 0)
    # fährt die letzen 5mm nur schrittweise, um nicht zu weit zu fahren
    # Am Schluss wird 6x gemessen und geprüft ob die mittlere Abweichung < 0.5mm ist
    def initFork(self):
        moveButtonSlider = True
        while moveButtonSlider:
            if (_i2c.getDistanceLeftFront() - _i2c.getDistanceRightFront()):
                if (_i2c.getDistanceLeftFront() > _i2c.getDistanceRightFront()):
                    _buttonpresser.left()
                    if (abs(_i2c.getDistanceLeftFront() - _i2c.getDistanceRightFront()) < 5):
                        sleep(0.01)
                        _buttonpresser.stop()
                        sleep(0.02)
                else:
                    _buttonpresser.right()
                    if (abs(_i2c.getDistanceLeftFront() - _i2c.getDistanceRightFront()) < 5):
                        sleep(0.01)
                        _buttonpresser.stop()
                        sleep(0.02)
            else:
                _buttonpresser.stop()
                sumDiff = 0
                for i in range(0, 5):
                    sumDiff += abs(_i2c.getDistanceLeftFront() - _i2c.getDistanceRightFront())
                    sleep(0.1)
                if sumDiff < 3:
                    moveButtonSlider = False
            sleep(0.01)


    def getDistOffset(self):
        sumLeftBack = 0
        sumLeftFront = 0
        sumRightBack = 0
        sumLeftBack = 0
        for i in range(0, 7):
            sumLeftBack   += _i2c.getDistanceLeftBack()
            sumLeftFront  += _i2c.getDistanceLeftFront()
            sumRightBack  += _i2c.getDistanceRightBack()
            sumRightFront += _i2c.getDistanceRightFront()
            sleep(0.1)
        OffsetLeftFront  = SumLeftFront/8  - 40
        OffsetLeftBack   = SumLeftBack/8   - 40
        OffsetRightFront = SumRightFront/8 - 40
        OffsetRightBack  = SumRightBack/8  - 40