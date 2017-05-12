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

        pid_dist = pid.PID(0.002, 0, 0)
        pid_dist.setWindup(0.5)
        pid_dist.sample_time = 0.1
        soll_angle = 0

        pid_angle = pid.PID(1.5, 0, 0)
        pid_angle.setWindup(0.5)
        pid_angle.sample_time = 0.1

    def terminate(self):
        self._running = False

    def run(self):
        while(self._running):
            ist_dist = self._i2c.getDistanceLeftBack() - self._i2c.getDistanceRightBack()
            ist_angle = atan((self._i2c.getDistanceLeftFront() - (self._i2c.getDistanceLeftBack() - 0.5)) / 180)
            pid_dist.SetPoint = 0.0
            if pid_dist.update(ist_dist):
                soll_angle = pid_dist.output
                pid_angle.SetPoint = soll_angle

            if pid_angle.update(ist_angle):
                DeltaVelocityLeft_proz = pid_angle.output
                VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
                _motorController.setVelocityLeft(config.guidedDriveVelocity)

            sleep(0.02)
