from modul import motor
from modul import i2cHandler
from common import drivingUtilities
from modul import forkHandler
from haleyenum.direction import direction
import pigpio

import config

from time import sleep

motorDriver = None
handler = None
forkhandler = None


try:
    motorDriver = motor.motor()
    motorDriver.start()

    handler = i2cHandler.I2cHandler()
    handler.start()

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)

    forkHandler = forkHandler.Fork(handler)
    #forkHandler.setForkPositionByManual()

    """
    sleep(1)
    utilities.driveByTime(1500,-50)
    # Startgeschwindigkeit
    utilities.accelerate(70)
    # Fahre bis 30mm an die Wand
    utilities.approachWallAndStop(30)

    # Positioniere Gabel
    forkHandler.setPositionForNumber(5, direction.LEFT)

    # Tippe Button
    motorDriver.setVelocityLeft(20)
    motorDriver.setVelocityRight(20)
    sleep(0.3)
    # Kurzes Rücksetzen
    utilities.driveByTime(1000, -40)
    forkHandler.setPositionForNumber(0, direction.LEFT)
    utilities.turn(360)
"""
    # Fertig

    forkHandler.setForkPositionByManual()


    motorDriver.terminate()
    handler.terminate()

except KeyboardInterrupt:
    forkHandler.stopMovement()
    motorDriver.terminate()
    handler.terminate()
    print("Goodbye!")
except:
    forkHandler.stopMovement()
    motorDriver.terminate()
    handler.terminate()
    print("Aaaaaargh!")
    raise



"""
    while(True):
        print("Current distance: RF{}".format(handler.getDistanceRightFront()))
        sleep(2)

    sleep(1)
    utilities.driveByTime(1500,-50)
    # Startgeschwindigkeit
    utilities.accelerate(70)
    # Fahre bis 30mm an die Wand
    utilities.approachWallAndStop(30)

    # Positioniere Gabel


    # Tippe Button
    motorDriver.setVelocityLeft(20)
    motorDriver.setVelocityRight(20)
    sleep(0.3)
    # Kurzes Rücksetzen
    utilities.driveByTime(1000, -40)

    # Fertig
"""




