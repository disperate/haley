import cv2
import numpy as np

redValue = 175
greenValue = 60
sensitivity = 15
font = cv2.FONT_HERSHEY_SIMPLEX

lower_green = np.array([greenValue - sensitivity, 100, 50])
upper_green = np.array([greenValue + sensitivity, 255, 255])

class greenLightDedection:

    def _green(self, img):
        mask = cv2.inRange(img, lower_green, upper_green)
        onlygreenframe = cv2.bitwise_and(img, img, mask=mask)
        return self._dedectCircles(onlygreenframe)


    def _dedectCircles(self, img):
        res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(res, cv2.HOUGH_GRADIENT, 1, 20, param1=10, param2=10, minRadius=3, maxRadius=20)
        if circles is not None:
            return True
        return False


    def dedectAmpel(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        if self._green(hsv):
            print("Let's go. It's Green. GREEN!")
            return True
        else:
            print("Not green...")
            return False

