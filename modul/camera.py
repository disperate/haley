import time
from threading import Thread

import numpy as np
import picamera

import modul.greenLightDedection


class camera(Thread):
    def __init__(self):
        super().__init__()
        self._running = True
        self._dedectGreenLight = False
        self._dedectRomanNumber = False
        self._romanNumber = None
        self.isGreen = False
        self._camera = picamera.PiCamera()
        self._camera.resolution = (640, 480)
        self._camera.framerate = 24
        self._greenLightDedection = modul.greenLightDedection.greenLightDedection()

    def startGreenlightDedection(self):
        self._dedectGreenLight = True

    def stopGreenlightDedection(self):
        self._dedectGreenLight = False

    def startRomanNumberDedection(self):
        self._dedectRomanNumber = True

    def stopRomanNumberDedection(self):
        self._dedectRomanNumber = False

    def getRomanNumber(self):
        """
        Description: Returns the found Roman Number or None if its not found yet.
        Start looking for the roman number by calling startRomanNumberDedection()
        Returns:     int (1-5)
        """
        return self._romanNumber

    def terminate(self):
        self._running = False

    def run(self):
        while (self._running):
            image = np.empty((480 * 640 * 3,), dtype=np.uint8)
            self._camera.capture(image, 'bgr')
            image = image.reshape((480, 640, 3))

            if self._dedectGreenLight:
                self.isGreen = self._greenLightDedection.dedectAmpel(image)
                if self.isGreen:
                    self.stopGreenlightDedection()

            if self._dedectRomanNumber:
                print("looking for roman nummber")
            time.sleep(0.01)
