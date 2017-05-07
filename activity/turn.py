from threading import Thread
from time import sleep
from common import drivingUtilities

THREAD_SLEEP_MS = 100

class turnActivity(Thread):
    def __init__(self, fsm, motorController, i2cHandler):
        super().__init__()
        self._direction = fsm.direction
        self._motor = motorController
        self._i2c = i2cHandler
        self._util = drivingUtilities.DrivingUtilities(self._i2c, self._motor)

    def run(self):
        # 1. Drive straight ahead for a specific time
        print("Drive 1 sec")
        self._motor.setVelocityRight(60)
        self._motor.setVelocityLeft(60)
        sleep(0.5)

        # 2. Turn haley 90°
        print("Turn 90")
        self._util.turn(-90)

        # 3. Drive straight ahead until front sensor < 7cm
        print("Drive straight ahead until front sensor < 7cm")
        self._motor.setVelocityRight(40)
        self._motor.setVelocityLeft(40)

        while self._i2c.getDistanceFront() > 100:
            print("Wall is ahead: " + str(self._i2c.getDistanceFront()))
            sleep(0.001)

        self._motor.setVelocityRight(0)
        self._motor.setVelocityLeft(0)


        # 4. Turn haley 90° again
        self._util.turn(-90)

        # 5. Check sensors if haley is parallel


        # 6. Drive straight ahead until sensors on both sides get ze right dimension

        self._motor.setVelocityRight(60)
        self._motor.setVelocityLeft(60)
        # sleep((1 / 1000) * THREAD_SLEEP_MS)


    def _driveStraightAhead(self, velocity, timeInMs):
        self._motorController(velocity)
        self._motorController(velocity)
        sleep(timeInMs)