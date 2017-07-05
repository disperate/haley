from threading import Thread
from time import sleep

from common import drivingUtilities
from modul import fork


# ------------------------------------------------------------------------------
# Attention! setPositionForNumber() is tested only for the left parcour!!!
# Handling for the right side is not tested but may work!
# ------------------------------------------------------------------------------

class buttonPressActivity(Thread):
    def __init__(self, fsm, motorController, i2cHandler, camera):
        super().__init__()
        self._fsm = fsm
        self._direction = fsm.direction
        self._motor = motorController
        self._camera = camera
        self._i2c = i2cHandler
        self._util = drivingUtilities.DrivingUtilities(self._i2c, self._motor)
        self._fork = fork.fork(self._i2c)

    def run(self):
        try:

            self._motor.setVelocityLeft(0)
            self._motor.setVelocityRight(0)

            while not self._camera.imageQueue.empty():
                print("waiting for queue")
                self._motor.setVelocityLeft(0)
                self._motor.setVelocityRight(0)
                sleep(0.1)

            print("Work in queue done")

            romanNumber = self._camera.getRomanNumber()
            self._i2c.setRomanNumber(romanNumber)

            self._motor.setVelocityLeft(40)
            self._motor.setVelocityRight(40)


            # Drive straight ahead until a distance of 50mm in front of the buttons
            self._util.approachWallAndStop(50)

            # Positioning fork
            self._fork.setPositionForNumber(romanNumber, self._direction)

            # Smash that fuckin' button
            self._motor.setVelocityLeft(20)
            self._motor.setVelocityRight(20)
            sleep(0.7)

            # Step back
            self._util.driveByTime(1000, -40)

            # Continue...
            self._fsm.buttonPressed()
        except:
            self._fork.stopMovement()
            self._motor.stop()
