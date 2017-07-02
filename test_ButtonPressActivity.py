from time import sleep

from common import drivingUtilities
from haleyenum.direction import direction
from modul import fork
from modul import i2cHandler
from modul import motor

motorDriver = None
i2c = None
fork = None
testPattern = 1

try:
    motorDriver = motor.motor()
    motorDriver.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    utilities = drivingUtilities.DrivingUtilities(i2c, motorDriver)
    fork = fork.fork(i2c)

    # Set manually fork position
    if (testPattern == 1):
        fork.setForkPositionByManual()

    # Set fork position test
    if (testPattern == 2):
        fork.setPositionForNumber(5, direction.RIGHT)
        sleep(3)

    # Test all numbers
    if (testPattern == 3):
        fork.setPositionForNumber(1, direction.LEFT)
        sleep(1)
        fork.setPositionForNumber(2, direction.LEFT)
        sleep(1)
        fork.setPositionForNumber(3, direction.LEFT)
        sleep(1)
        fork.setPositionForNumber(4, direction.LEFT)
        sleep(1)
        fork.setPositionForNumber(5, direction.LEFT)
        sleep(1)
        fork.setPositionForNumber(0, direction.LEFT)
        sleep(1)

    # Test button press routine
    if (testPattern == 4):
        sleep(1)
        utilities.driveByTime(1500, -50)
        # Startgeschwindigkeit
        utilities.accelerate(100)
        # Fahre bis 30mm an die Wand
        utilities.approachWallAndStop(50)

        # Positioniere Gabel
        fork.setPositionForNumber(3, direction.RIGHT)

        # Tippe Button
        motorDriver.setVelocityLeft(20)
        motorDriver.setVelocityRight(20)
        sleep(0.2)
        # Kurzes Rücksetzen
        utilities.driveByTime(1000, -40)
        fork.setPositionForNumber(0, direction.RIGHT)

    motorDriver.terminate()
    i2c.terminate()

except KeyboardInterrupt:
    fork.stopMovement()
    motorDriver.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    fork.stopMovement()
    motorDriver.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise
