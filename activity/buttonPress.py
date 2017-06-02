from threading import Thread
from time import sleep
from common import drivingUtilities
from modul import forkHandler

#------------------------------------------------------------------------------
# Attention! setPositionForNumber() is tested only for the left parcour!!!
# Handling for the right side is not tested but may work!
#------------------------------------------------------------------------------

class buttonPressActivity(Thread):
    def __init__(self, fsm, motorController, i2cHandler):
        super().__init__()
        self._fsm = fsm
        self._direction = fsm.direction
        self._motor = motorController
        self._i2c = i2cHandler
        self._util = drivingUtilities.DrivingUtilities(self._i2c, self._motor)
        self._fork = forkHandler.Fork(self._i2c)

    def run(self):
        # Drive straight ahead until a distance of 40mm in front of the buttons
        self._util.approachWallAndStop(50)

        # Positioning fork
        self._fork.setPositionForNumber(3, self._direction)

        # Smash that fuckin' button
        self._motor.setVelocityLeft(20)
        self._motor.setVelocityRight(20)
        sleep(0.7)
        # Step back
        self._util.driveByTime(1000, -40)
        # Reset position of fork
        self._fork.setPositionForNumber(0, self._direction)

        # Continue...
        self._fsm.buttonPressed()