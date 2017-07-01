from threading import Thread
from time import sleep

import picamera
from picamera import array

import modul.kerasGreenLightDedection


class camera(Thread):
    def __init__(self):
        super().__init__()

        image_height = 128
        image_width = 128

        self._running = True
        self._dedectGreenLight = False
        self._dedectRomanNumber = False
        self._romanNumber = None
        self.isGreen = False
        self._greenLightDedection = modul.kerasGreenLightDedection.kerasGreenLightDedection(image_height, image_width)

        self._camera = picamera.PiCamera()
        self._camera.resolution = (image_height, image_width)
        self._camera.framerate = 10
        self._camera.exposure_mode = 'sports'

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

        with array.PiRGBArray(self._camera) as output:
            while (self._running):
                self._camera.capture(output, 'rgb')

                if self._dedectGreenLight:

                    self.isGreen = self._greenLightDedection.dedectAmpel(output)
                    if self.isGreen:
                        self.stopGreenlightDedection()

                if self._dedectRomanNumber:
                    print("looking for roman nummber")

                output.truncate(0)
                sleep(0.01)
