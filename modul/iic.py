#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.03.31
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        Iic
# Description:  This class provides:
#               - guarantees "synchronised" access to the I2C-bus.
#               - act as a container for gyro- and distance-data
#               - reads continuous via thread the current gyro- and
#                 distance-values and stores it
#------------------------------------------------------------------------------

# Imports
from modul.iic import senseHatAdapter
from modul.iic import distanceSensors

# Class
class Iic:
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self.currYaw = 0.0
        self.currPitch = 0.0
        self.currRoll = 0.0
        pass