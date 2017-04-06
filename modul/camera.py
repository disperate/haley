from threading import Thread
import time

class camera(Thread):

    def __init__(self):
        super().__init__()
        self._running = True
        self._dedectGreenLight = False
        self._dedectRomanNumber = False
        self._romanNumber = None
        self._isGreen = False

    def startGreenlightDedection(self):
        self._dedectGreenLight = True

    def stopGreenlightDedection(self):
        self._dedectGreenLight = False

    def startRomanNumberDedection(self):
        self._dedectRomanNumber = True

    def getRomanNumber(self):
        """
        Description: Returns the found Roman Number or None if its not found yet.
        Start looking for the roman number by calling startRomanNumberDedection()
        Returns:     int (1-5)
        """
        return self._romanNumber

    def isGreen(self):
        """
        Description: False until green light is dedected
        Start looking for green light by calling startGreenlightDedection
        Returns:     bool
        """
        return self._isGreen

    def terminate(self):
        self._running = False

    def run(self):
        while (self._running):
            if self._dedectGreenLight:
                print("looking for green light")

            if self._dedectRomanNumber:
                print("looking for roman nummber")
            time.sleep(0.1)
