from threading import Thread
from time import sleep
from common import drivingUtilities
from haleyenum import direction

THREAD_SLEEP_MS = 100

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
        print("Drive 1 sec")
        self._motor.setVelocityRight(80)
        self._motor.setVelocityLeft(80)
        sleep(0.4)

        # 2. Turn haley 90°
        print("Turn 90")
        if self._direction is direction.direction.LEFT:
            self._util.turn(90)
        if self._direction is direction.direction.RIGHT:
            self._util.turn(-90)

        # 3. Drive straight ahead until front sensor < 7cm
        print("Drive straight ahead until front sensor < 7cm")
        self._motor.setVelocityRight(80)
        self._motor.setVelocityLeft(80)

        while self._i2c.getDistanceFront() > 150:
            sleep(0.001)

        self._motor.setVelocityRight(30)
        self._motor.setVelocityLeft(30)

        while self._i2c.getDistanceFront() > 80:
            sleep(0.001)

        self._motor.setVelocityRight(0)
        self._motor.setVelocityLeft(0)


        # 4. Turn haley 90° again
        print("Turn 90")
        if self._direction is direction.direction.LEFT:
            self._util.turn(90)
        if self._direction is direction.direction.RIGHT:
            self._util.turn(-90)

        # 5. Check sensors if haley is parallel
        self._util.adjustToWall(self._direction)

        # 6. Drive straight ahead until sensors on both sides get ze right dimension

        self._motor.setVelocityRight(70)
        self._motor.setVelocityLeft(70)

        self._fsm.turned = True
        self._fsm.turnDone()
