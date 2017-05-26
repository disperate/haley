from threading import Thread
from time import sleep
from common import regler
from haleyenum.reglerMode import ReglerMode


class guidedDriveActivity(Thread):
    def __init__(self, fsm, motor, i2c):
        super().__init__()
        self._running = True
        self._motorController = motor
        self._i2c = i2c
        self._regler = regler.PID(self._motorController, self._i2c, ReglerMode.TO_MIDDLE)

    def terminate(self):
        self._running = False

    def run(self):
        while (self._running):
            self._regler.update()
            sleep(0.02)
