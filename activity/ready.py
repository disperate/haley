import time
import pigpio
import config
from haleyenum import direction


class readyActivity(object):
    def __init__(self, fsm):
        self._pi = pigpio.pi()
        buttonPressed = False

        print("waiting for button...")
        # Wait until button is pressed and direction is set
        while (not buttonPressed or fsm.direction == None):
            buttonPressed = not self._pi.read(config.BUTTON)
            if (self._pi.read(config.SWITCH1) == 0):
                fsm.direction = direction.direction.LEFT
            if (self._pi.read(config.SWITCH2) == 0):
                fsm.direction = direction.direction.RIGHT
            if (self._pi.read(config.SWITCH1) == self._pi.read(config.SWITCH2)):
                fsm.direction = None
            time.sleep(0.1)

        print("pressed, going :")
        print(fsm.direction)

        fsm.startPressed()
