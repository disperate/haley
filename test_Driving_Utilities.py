from modul import motor
from modul import i2cHandler
from common import drivingUtilities

import config

from time import sleep

motorDriver = None
handler = None

try:
    handler = i2cHandler.I2cHandler()
    handler.start()

    motorDriver = motor.motor()
    motorDriver.start()
    motorDriver.startLogging()

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)
    sleep(0.5)
    utilities.accelerate(30)
    sleep(0.5)
    utilities.accelerate(80)
    sleep(0.5)
    utilities.accelerate(-80)
    sleep(0.5)
    utilities.accelerate(-30)
    sleep(0.5)
    utilities.stop()
    sleep(0.5)


    #utilities.turn(90.0)

    """utilities.driveDistanceByTime(1700, 80.0)
utilities.driveDistanceByTime(1700, -80.0)
utilities.driveDistanceByTime(1700, 80.0)
utilities.driveDistanceByTime(1700, -80.0)"""
    #utilities.turn(-90.0)
    #utilities.driveDistanceByTime(1300, 80.0)
    #utilities.turn(-90.0)

    """utilities.driveDistanceByTime(1500, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(3000, 80.0)
    utilities.turn(90.0)
    utilities.driveDistanceByTime(1500, 80.0)"""

    motorDriver.stopLogging()
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
