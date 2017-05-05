from threading import Thread
from time import sleep

THREAD_SLEEP_MS = 100

class turnActivity(Thread):
    def __init__(self, fsm, motorController, i2cHandler):
        super().__init__()
        self._direction = fsm.direction
        self._motorController = motorController
        self._i2cHandler = i2cHandler

    def run(self):
        # 1. Drive straight ahead for a specific time
        self._driveStraightAhead(60, 1000)

        # 2. Turn haley 90°
        self._turn(90)

        # 3. Drive straight ahead until front sensor < 7cm


        # 4. Turn haley 90° again


        # 5. Check sensors if haley is parallel


        # 6. Drive straight ahead until sensors on both sides get ze right dimension


        # sleep((1 / 1000) * THREAD_SLEEP_MS)


    def _driveStraightAhead(self, velocity, timeInMs):
        self._motorController(velocity)
        self._motorController(velocity)
        sleep(timeInMs)


    def _turn(self, angle):
        self._i2cHandler.resetRelativeYaw()

        if(angle < 0):
            # Turn left
            while(True):
                currDelta = (abs(angle) - abs(self._i2cHandler.currRelativeYaw)) > 10
                if(currDelta > 10):
                    self._motorController.setVelocityLeft(-50)
                    self._motorController.setVelocityRight(50)
                else:
                    self._motorController.setVelocityLeft(-20)
                    self._motorController.setVelocityRight(20)

                if(angle - (self._i2cHandler.currRelativeYaw) > 0):
                    break
        else:
            # Turn right
            while(True):
                pass




        while(True):
            if(angle < )

            if (endAngleUnder - currentAngle < 20):
                motor.setVelocityLeft(20)
                motor.setVelocityRight(-20)








        # 1. Drive straight ahead for a specific time
        motor.setVelocityLeft(60)
        motor.setVelocityRight(60)

        # 2. Turn haley 90°
        fsm.direction

        # 3. Drive straight ahead until front sensor < 7cm


        # 4. Turn haley 90° again


        # 5. Check sensors if haley is parallel


        # 6. Drive straight ahead until sensors on both sides get ze right dimension
        motor.setVelocityLeft(60)
        motor.setVelocityRight(60)
