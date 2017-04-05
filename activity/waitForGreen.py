import time
import config

class waitForGreenActivity(object):


    def __init__(self, fsm, cameraModul):
        self.startTime = time.time()
        print("waiting for green...")
        cameraModul.startGreenlightDedection()


        while(not cameraModul.isGreen() and not self.timeout()):
            time.sleep(0.1)

        print("green")
        fsm.greenlight()

    def timeout(self):
        secondsToTimeout = config.greenlightTimeoutInSeconds
        return time.time() - self.startTime > secondsToTimeout

