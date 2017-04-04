#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
# Datum:        2017.04.04
# Version:      0.1
#------------------------------------------------------------------------------
# Class:        DistanceSensorAdapter
# Description:  This class provides:
#               - Initialization and access to the Distance-Sensors via I2C
#               - Distance-Sensors: VL53L0X Time-of-Flight (ToF) ranging sensor
#------------------------------------------------------------------------------

# Imports
import pigpio

# Class
class DistanceSensorAdapter():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self):
        self.pi = pigpio.pi()

    # Funktions
    # --------------------------------------------------------------------------
    def fuuBar(self):
        pass