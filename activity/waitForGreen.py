import time

class waitForGreenActivity(object):
    def __init__(self, fsm, cameraModul):
        print("waiting for green...")
        cameraModul.startGreenlightDedection()
        time.sleep(3)
        print("green")
        fsm.greenlight()
