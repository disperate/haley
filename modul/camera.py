import threading
from queue import Queue
from threading import Thread
from time import sleep

import picamera
from picamera import array

import modul.kerasGreenLightDedection
import modul.romanNumberDedection


class camera(Thread):

    imageQueue = Queue()

    def __init__(self, i2c):
        super().__init__()

        image_height = 128
        image_width = 128

        self._running = True
        self._dedectGreenLight = False
        self._dedectRomanNumber = False
        self.isGreen = False

        self._greenLightDedection = modul.kerasGreenLightDedection.kerasGreenLightDedection(image_height, image_width)
        self._romanNumberDedection = modul.romanNumberDedection.romanNumberDedection(image_height, image_width, i2c)

        self._camera = picamera.PiCamera()
        self._camera.resolution = (image_height, image_width)
        self._camera.framerate = 10
        self._camera.exposure_mode = 'sports'

        imageProcessingThread = threading.Thread(target=self.processImageQueue)
        imageProcessingThread.start()

    def processImageQueue(self):
        while True:
            self._romanNumberDedection.dedectNumber(self.imageQueue.get())
            sleep(0.01)

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
        print("returning roman number")

        resultList = list(self._romanNumberDedection.resultList)
        print(resultList)

        # if self._romanNumberDedection.romanNumber is not None:
        #    return self._romanNumberDedection.romanNumber

        print("In Bounds 3-5")
        for x in range(1, 6):
            if self.liesInBounds(3, 5, resultList, x):
                return x
        print("In Bounds 2-5")
        for x in range(1, 6):
            if self.liesInBounds(2, 5, resultList, x):
                return x
        print("In Bounds 1-6")
        for x in range(1, 6):
            if self.liesInBounds(1, 6, resultList, x):
                return x
        print("In Bounds 1-30")
        for x in range(1, 6):
            if self.liesInBounds(1, 30, resultList, x):
                return x

        print("Random die 2")
        return 2

    def liesInBounds(self, under, upper, listOfDedections, index):
        count = listOfDedections.count(index)
        if under <= count and count <= upper:
            return True

    def terminate(self):
        self._running = False

    def run(self):

        with array.PiRGBArray(self._camera) as output:
            while (self._running):
                self._camera.capture(output, 'rgb', use_video_port=True)

                if self._dedectGreenLight:

                    self.isGreen = self._greenLightDedection.greenLightDedected(output)
                    if self.isGreen:
                        self.stopGreenlightDedection()

                if self._dedectRomanNumber:
                    self.imageQueue.put(output)

                output.truncate(0)
                sleep(0.01)
