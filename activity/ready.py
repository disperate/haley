import time

class readyActivity(object):
    def __init__(self, fsm):
        print("waiting for button...")
        time.sleep(2)
        print("pressed")
        fsm.startPressed()

