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

        #self.pid_dist = pid.PID(0.002, 0, 0)
        #self.pid_dist.setWindup(0.5)
        #self.pid_dist.sample_time = 0.1
        #self.soll_angle = 0

        #self.pid_angle = pid.PID(1.5, 0, 0)
        #self.pid_angle.setWindup(0.5)
        #self.pid_angle.sample_time = 0.1

    def terminate(self):
        self._running = False

    def run(self):
        while(self._running):
            self._regler.update()

            #if ((self._i2c.getDistanceLeftBack() > config.loseWallsDistanceThreshold) or
            #    (self._i2c.getDistanceLeftFront() > config.loseWallsDistanceThreshold) or
            #    (self._i2c.getDistanceRightBack() > config.loseWallsDistanceThreshold) or
            #    (self._i2c.getDistanceRightFront() > config.loseWallsDistanceThreshold)    ):
            #    self._motorController.setVelocityLeft(config.guidedDriveVelocity)
            #    self._motorController.setVelocityRight(config.guidedDriveVelocity)
            #else:
            #    ist_dist = self._i2c.getDistanceLeftBack() - self._i2c.getDistanceRightBack()
            #    ist_angle = atan((self._i2c.getDistanceLeftFront() - (self._i2c.getDistanceLeftBack() - 0.5)) / 180)
            #    self.pid_dist.SetPoint = 0.0
            #    if self.pid_dist.update(ist_dist):
            #        self.soll_angle = self.pid_dist.output
            #        self.pid_angle.SetPoint = self.soll_angle

            #    if self.pid_angle.update(ist_angle):
            #        DeltaVelocityLeft_proz = self.pid_angle.output
            #        VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
            #        self._motorController.setVelocityLeft(config.guidedDriveVelocity)
            #        self._motorController.setVelocityRight(config.guidedDriveVelocity * VelocityLeft_proz)
            sleep(0.02)
