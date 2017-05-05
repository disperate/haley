#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Autor:        Adrian Kauz
#------------------------------------------------------------------------------
# Class:        Ringbuffer
# Description:  Buffer for float or integer values.
#
#------------------------------------------------------------------------------

class Ringbuffer():
    # Konstruktor
    # --------------------------------------------------------------------------
    def __init__(self, size = 5):
        self._printDebug("Init ringbuffer with {} elements...".format(size))
        self.size = size
        self.type = None
        self.buffer = [None] * size
        self.pointer = -1;
        self._printDebug("...done!")


    def add(self, value):
        if(self.pointer == -1):
            # Initial definition of type
            if(isinstance(value, float)):
                self.type = "Float"

            if(isinstance(value, int)):
                self.type = "Integer"

            self.resetBuffer()
        else:
            # Check type
            if(self.type == "Float"):
                if(isinstance(value, float) is False):
                    return False

            if (self.type == "Integer"):
                if (isinstance(value, int) is False):
                    return False

        # Set buffer position
        if(self.pointer < (self.size - 1)):
            self.pointer = self.pointer + 1
        else:
            self.pointer = 0

        # Write value into buffer position
        self.buffer[self.pointer] = value

        return True


    def resetBuffer(self):
        value = None

        if (self.type == "Integer"):
            value = 0

        if (self.type == "Float"):
            value = 0.0

        for x in range(0, self.size):
            self.buffer[x] = value


    def getCurrentValue(self):
        return self.buffer[self.pointer]


    def getPreviousValue(self):
        if(self.pointer > 0):
            return self.buffer[self.pointer - 1]
        else:
            return self.buffer[self.size - 1]


    def getArithmeticMean(self):
        if(self.isFull()):
            result = 0.0

            for bufferItem in self.buffer:
                result = result + float(bufferItem)

            if (self.type == "Integer"):
                return int(round(result / self.size))
            else:
                return result / self.size

        else:
            return None


    def isFull(self):
        for bufferItem in self.buffer:
            if((isinstance(bufferItem, int) is False) and (isinstance(bufferItem, float) is False)):
                return False

        return True


    def _printDebug(self, message):
        if (__debug__):
            print("    {}: {}".format(self.__class__.__name__, message))