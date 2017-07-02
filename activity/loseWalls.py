import time

import config


class loseWallsActivity(object):
    def __init__(self, fsm, i2c):
        while i2c.getDistanceLeftBack() < config.loseWallsDistanceThreshold or i2c.getDistanceRightBack() < config.loseWallsDistanceThreshold:
            print("i see walls...")
            time.sleep(0.01)

        print("walls lost")
        fsm.wallsLost()
