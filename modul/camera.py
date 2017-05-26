from threading import Thread
import picamera
import numpy as np
import cv2
import time

redValue = 175
greenValue = 60
sensitivity = 15
font = cv2.FONT_HERSHEY_SIMPLEX


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
                print("looking for green light...")
                self._dedectAmpel(image)

            if self._dedectRomanNumber:
                print("looking for roman nummber")
            time.sleep(0.01)

    def _green(self, img):
        lower_red = np.array([greenValue - sensitivity, 100, 50])
        upper_red = np.array([greenValue + sensitivity, 255, 255])
        mask = cv2.inRange(img, lower_red, upper_red)
        onlygreenframe = cv2.bitwise_and(img, img, mask=mask)

        return self._dedectCircles(onlygreenframe)

    def _red(self, img):
        lower_red = np.array([redValue - sensitivity, 100, 100])
        upper_red = np.array([redValue + sensitivity, 255, 255])
        mask = cv2.inRange(img, lower_red, upper_red)
        onlyredframe = cv2.bitwise_and(img, img, mask=mask)

        kernel = np.ones((3, 3), np.uint8)

        img_erosion = cv2.erode(onlyredframe, kernel, iterations=1)

        return self._dedectCircles(img_erosion)

    def _toHSV(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def _dedectCircles(self, img):
        res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, 1, 20, param1=10, param2=10, minRadius=3, maxRadius=20)
        if circles is not None:
            return True
        return False

    def _dedectAmpel(self, img):
        hsv = self._toHSV(img)
        if self._red(hsv):
            print("red.")
        if self._green(hsv):
            self.isGreen = True
            print("Let's go. It's Green. GREEN!")
            self.stopGreenlightDedection()
