from modul import motor
from modul import i2cHandler
from common import drivingUtilities

import config

from time import sleep

motorDriver = None
handler = None

try:
    motorDriver = motor.motor()
    motorDriver.start()

    handler = i2cHandler.I2cHandler()
    handler.start()

    sleep(2)

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)
    utilities.driveDistanceByTime(1500, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(1500, 80.0)

    motorDriver.terminate()
    handler.terminate()

except KeyboardInterrupt:
    motorDriver.terminate()
    handler.terminate()
    print("Goodbye!")
except:
    motorDriver.terminate()
    handler.terminate()
    print("Aaaaaargh!")
    raise
