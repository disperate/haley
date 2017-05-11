from threading import Thread
import time
import config
from common import pid


class guidedDriveActivity(Thread):

    def __init__(self, fsm, motor, i2c):
        super().__init__()
        self._running = True
        self._motorController = motor
        self._i2c = i2c
        self._pid = pid.PID(0.01, 0, 0)
        self._pid.SetPoint=0.0

    def terminate(self):
        self._running = False

    def run(self):
        while(self._running):
            self._motorController.setVelocityLeft(60.0)
            self._motorController.setVelocityRight(60.0)
            time.sleep(0.01)
