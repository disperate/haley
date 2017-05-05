from threading import Thread
import time
import pigpio
import config

class buttonpresser(Thread):

    _goLeft = False
    _goRight = False

    def __init__(self):
        super().__init__()

        self._pi = pigpio.pi()
        self._running = True

    def left(self):
        self._goLeft = True
        self._goRight = False

    def right(self):
        self._goRight = True
        self._goLeft = False

    def stop(self):
        self._goRight = False
        self._goLeft = False

    def terminate(self):
        self._running = False

    def run(self):

        while self._running:
            self._pi.write(config.DCMOT_IN1, self._goLeft)
            self._pi.write(config.DCMOT_IN2, self._goRight)
            time.sleep(0.01)