from threading import Thread
from time import sleep
from common import drivingUtilities
from haleyenum import direction


class turnActivity(Thread):
    def __init__(self, fsm, motorController, i2cHandler):
        super().__init__()
        self._fsm = fsm
        self._direction = fsm.direction
        self._motor = motorController
        self._i2c = i2cHandler
        self._util = drivingUtilities.DrivingUtilities(self._i2c, self._motor)

    def run(self):

        # 1. Drive straight ahead for a specific time
        print("Drive 0.6 sec")
        self._util.driveByTime(700, 80)

        # 2. Turn haley 90°
        print("Turn 90")
        if self._direction is direction.direction.LEFT:
            self._util.turn(90)
        if self._direction is direction.direction.RIGHT:
            self._util.turn(-90)

        # 3. Drive straight ahead until fork has a distance of 10mm to the wall
        print("Drive straight ahead until fork as a distance of 10mm to the wall")
        self._util.accelerate(80)
        self._util.approachWallAndStop(10)

        # 4. Turn haley 90° again
        print("Turn 90")
        if self._direction is direction.direction.LEFT:
            self._util.turn(90)
        if self._direction is direction.direction.RIGHT:
            self._util.turn(-90)

        # 5. Check sensors if haley is parallel
        self._util.adjustToWall(self._direction)

        # 6. Drive straight ahead until sensors on both sides get ze right dimension
        self._util.accelerate(70)

        self._fsm.turned = True
        self._fsm.turnDone()
