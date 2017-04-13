import time

class turnActivity(object):
    def __init__(self, fsm, motor):
        motor.setVelocityLeft(60)
        motor.setVelocityRight(-60)
        time.sleep(2)

        motor.setVelocityLeft(60)
        motor.setVelocityRight(60)
        time.sleep(2)

        motor.setVelocityLeft(60)
        motor.setVelocityRight(-60)
        time.sleep(2)

