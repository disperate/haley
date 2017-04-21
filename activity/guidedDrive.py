from threading import Thread
import time
import config
from common import PID


class guidedDriveActivity(Thread):

    def __init__(self, fsm, motor, i2c):
        super().__init__()
        self._running = True
        self._motorController = motor
        self._i2c = i2c
        self._pid = PID.PID(0.001, 0, 0)
        self._pid.SetPoint=0.0

    def terminate(self):
        self._motorController.setVelocityLeft(0.0)
        self._motorController.setVelocityRight(0.0)
        self._running = False

    def run(self):
        while(self._running):
            error = self._i2c.getDistanceLeftBack() - self._i2c.getDistanceRightBack()
            print(error)
            if self._pid.update(error):
                self._motorController.setVelocityLeft(config.guidedDriveVelocity * (1 + self._pid.output))
                self._motorController.setVelocityRight(config.guidedDriveVelocity)
