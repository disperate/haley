from modul import motor
from modul import i2cHandler
from common import drivingUtilities

import config

from time import sleep

motorDriver = None
handler = None
testPattern = 2

try:
    handler = i2cHandler.I2cHandler()
    handler.start()

    motorDriver = motor.motor()
    motorDriver.start()
    #motorDriver.startLogging()

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)

    # Simple drive forward, turn, forward, turn
    if(testPattern == 1):
        for x in range(0,1):
            sleep(0.5)
            utilities.accelerate(60)
            sleep(1)
            utilities.accelerate(100)
            utilities.stop()
            utilities.turn(180)
            utilities.accelerate(100)
            sleep(1)
            utilities.accelerate(60)
            sleep(0.5)
            utilities.stop()
            utilities.turn(180)

    # Approach wall test
    if(testPattern == 2):
        sleep(0.5)
        utilities.driveByTime(2000, -80)
        utilities.accelerate(100)
        utilities.approachWallAndStop(10)


    utilities.stop()
    #motorDriver.stopLogging()
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
