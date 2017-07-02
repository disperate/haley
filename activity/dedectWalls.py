import time

import config


class dedectWallsActivity(object):
    def __init__(self, fsm, i2c):
        while i2c.getDistanceLeftBack() + i2c.getDistanceRightBack() > config.dedectWallsDistanceThreshold:
            print("waiting for walls...")
            time.sleep(0.1)

        print("walls dedected")
        fsm.wallsDedected()
