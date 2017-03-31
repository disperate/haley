from threading import Thread
import time
import pigpio

class buttonpresser(Thread):


    def __init__(self):
        super().__init__()
        self._DCMOT_IN1 = 19
        self._DCMOT_IN2 = 18

        # Only for testing
        self._SWITCH1 = 5
        self._SWITCH2 = 6
        self._BUTTON = 4

        self._pi = pigpio.pi()
        self._running = True
        self._romanNumber = None

    def terminate(self):
        self._running = False

    def run(self):
        while (self._running):
            self._pi.write(18, self._pi.read(self._SWITCH1))
            self._pi.write(19, self._pi.read(self._SWITCH2))
            time.sleep(0.1)