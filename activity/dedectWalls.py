import time

class dedectWallsActivity(object):
    def __init__(self, fsm):
        print("waiting for walls...")
        time.sleep(12)
        print("walls dedected")
        fsm.wallsDedected()
