import time

class blindDriveActivity(object):
    def __init__(self, fsm):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        while(self._running):
            print("driving blind...")
            time.sleep(2)
