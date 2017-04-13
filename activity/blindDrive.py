from threading import Thread
import time
import config


class blindDriveActivity(Thread):

    def __init__(self, fsm, motor):
        super().__init__()
        self._running = True
        self._motorController = motor

    def terminate(self):
        self._motorController.setVelocityLeft(0.0)
        self._motorController.setVelocityRight(0.0)
        self._running = False

    def run(self):
        while(self._running):
            self._motorController.setVelocityLeft(config.blindDriveVelocity)
            self._motorController.setVelocityRight(config.blindDriveVelocity)
            time.sleep(0.1)
