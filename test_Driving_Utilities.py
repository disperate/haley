from time import sleep

from common import drivingUtilities
from modul import i2cHandler
from modul import motor

motorDriver = None
handler = None
testPattern = 1

try:
    handler = i2cHandler.I2cHandler()
    handler.start()

    motorDriver = motor.motor()
    motorDriver.start()
    motorDriver.startLogging()

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)

    # Simple drive forward, turn, forward, turn
    if (testPattern == 1):
        for x in range(0, 1):
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
    if (testPattern == 2):
        sleep(0.5)
        utilities.driveByTime(2000, -80)
        utilities.accelerate(100)
        utilities.approachWallAndStop(10)

    # Acceleration and stop test pattern
    if (testPattern == 3):
        sleep(0.2)
        utilities.accelerate(10)
        sleep(0.2)
        utilities.accelerate(40)
        sleep(0.2)
        utilities.accelerate(100)
        sleep(0.2)
        utilities.accelerate(-70)
        sleep(0.2)
        utilities.stop()
        sleep(0.2)
        utilities.accelerate(-70)
        sleep(0.2)
        utilities.stop()

    # DriveByTime Test
    if (testPattern == 4):
        sleep(0.2)
        utilities.driveByTime(150, 100)
        sleep(0.2)
        utilities.driveByTime(300, 100)
        sleep(0.2)
        utilities.driveByTime(600, 100)
        sleep(0.2)
        utilities.driveByTime(900, 100)
        sleep(0.2)
        utilities.driveByTime(1200, 100)
        sleep(0.2)

    utilities.stop()
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
