import time

class loseWallsActivity(object):
    def __init__(self, fsm):
        print("waiting for walls lost...")
        time.sleep(12)
        print("walls lost")
        fsm.wallsLost()