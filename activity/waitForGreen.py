import time

class waitForGreenActivity(object):
    def __init__(self, fsm):
        print("waiting for green...")
        time.sleep(2)
        print("green")
        fsm.greenlight()
