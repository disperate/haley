import time

import config
from haleyenum import direction


class loseWallsActivity(object):
    def __init__(self, fsm, i2c, currentDirection):

        if currentDirection is direction.direction.LEFT:
            while i2c.getDistanceLeftBack() < config.loseWallsDistanceThreshold:
                time.sleep(0.01)
        if currentDirection is direction.direction.RIGHT:
            while i2c.getDistanceRightBack() < config.loseWallsDistanceThreshold:
                time.sleep(0.01)

        print("walls lost")
        fsm.wallsLost()
