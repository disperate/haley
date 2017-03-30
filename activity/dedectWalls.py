import time

class dedectWallsActivity(object):
    def __init__(self, fsm):
        print("waiting for walls...")
        time.sleep(7)
        print("walls dedected")
        fsm.wallsDedected()
