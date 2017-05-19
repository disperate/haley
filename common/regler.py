#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Autor:        Urs Stoeckli
#-------------------------------------------------------------------------------
# Class:        Regler
# Description:  Regler um Haley in der Mitte der Spur zu halten
#
#               Der erste Regler versucht den Distanzfehler auf 0 zu regeln und
#               gibt dazu den benötigten Korrekturwinkel (Proportional zur Abweichung)
#               an den zweiten Regler weiter.
#               Der zweite Regler regelt den Winkel zur Bande auf dem vom ersten
#               Regler vorgegebenen Winkel.
#
# mode:        TO_MIDDLE:
#               - Regler versucht die Differenz zwischen linkem und rechtem
#                 Distanzsensor auf 0 zu regeln.
#               - Der Winkel wird zur linken Bande gemessen
#               TO_LEFT:
#               - Regler versucht die Distanz zur linken Bande auf 85mm zu regeln.
#               - Der Winkel wird zur linken Bande gemessen
#               TO_RIGHT:
#               - Regler versucht die Distanz zur rechten Bande auf 85mm zu regeln.
#               - Der Winkel wird zur rechten Bande gemessen
#
# _motorController:  Referenz zum Motoeren-Modul
#
# _i2c:         Referenz zu den I2C-Distanzsensoren
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#
#
#------------------------------------------------------------------------------


from math import atan
from time import sleep
import config
from common import pid
from haleyenum.reglerMode import reglerMode


class PID:
    # *** Konstruktor ***
    def __init__(self, motor, i2c, mode):
        super().__init__()
        self._motorController = motor
        self._i2c = i2c

        self.pid_dist = pid.PID(0.002, 0, 0)
        self.pid_dist.setWindup(0.5)
        self.pid_dist.sample_time = 0.1
        self.soll_angle = 0

        self.pid_angle = pid.PID(1.5, 0, 0)
        self.pid_angle.setWindup(0.5)
        self.pid_angle.sample_time = 0.1

        self.mode = mode

    # *** Funktionen ***

    # Setzen des Mode:
    # - TO_MIDDLE:  Differenz der linken und rechten Distanz auf 0 regeln
    # - TO_LEFT:    Distanz zur linken Bande auf 85mm regeln
    # - TO_RIGHT:   Distanz zur rechten Bande auf 85mm regeln
    def setMode(self, mode):
        self.mode = mode

    # Distanzfehler berechnen (je nach gewähltem Mode)
    def calcDist(self):
        if self.mode is reglerMode.TO_RIGHT:
            return 85 - self._i2c.getDistanceRightBack()
        elif self.mode is reglerMode.TO_LEFT:
            return self._i2c.getDistanceLeftBack() - 85
        else:
            return self._i2c.getDistanceLeftBack() - self._i2c.getDistanceRightBack()

    # Ist-Winkel berechnen (je nach gewähltem Mode zur linken oder rechten Bande)
    def calcAngle(self):
        if self.mode is reglerMode.TO_RIGHT:
            -atan((self._i2c.getDistanceRightFront() - (self._i2c.getDistanceRightBack() - 0.5)) / 180)
        else:
            atan((self._i2c.getDistanceLeftFront() - (self._i2c.getDistanceLeftBack() - 0.5)) / 180)

    # Prüft ob ein Wert der verwendeten Sensoren zu hoch ist (abhängig vom Mode)
    def checkDistValues(self):
        if self.mode is reglerMode.TO_RIGHT:
            if ((self._i2c.getDistanceRightBack() > config.loseWallsDistanceThreshold) or
                (self._i2c.getDistanceRightFront() > config.loseWallsDistanceThreshold)):
                return False
        elif self.mode is reglerMode.TO_LEFT:
            if ((self._i2c.getDistanceLeftBack() > config.loseWallsDistanceThreshold) or
                (self._i2c.getDistanceLeftFront() > config.loseWallsDistanceThreshold)):
                return False
        else:
            if ((self._i2c.getDistanceLeftBack() > config.loseWallsDistanceThreshold) or
                (self._i2c.getDistanceLeftFront() > config.loseWallsDistanceThreshold) or
                (self._i2c.getDistanceRightBack() > config.loseWallsDistanceThreshold) or
                (self._i2c.getDistanceRightFront() > config.loseWallsDistanceThreshold)):
                return False
        return True

    # Regler ausführen
    def update(self):
        if checkDistValues():
            ist_dist = calcDist()
            ist_angle = calcAngle()
            self.pid_dist.SetPoint = 0.0
            if self.pid_dist.update(ist_dist):
                self.soll_angle = self.pid_dist.output
                self.pid_angle.SetPoint = self.soll_angle

            if self.pid_angle.update(ist_angle):
                DeltaVelocityLeft_proz = self.pid_angle.output
                VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
                self._motorController.setVelocityLeft(config.guidedDriveVelocity)
                self._motorController.setVelocityRight(config.guidedDriveVelocity * VelocityLeft_proz)
        else:
            self._motorController.setVelocityLeft(config.guidedDriveVelocity)
            self._motorController.setVelocityRight(config.guidedDriveVelocity)
