from common import drivingUtilities
from haleyenum import direction
from modul import i2cHandler
from modul import motor

motorDriver = None
handler = None

try:
    motorDriver = motor.motor()
    motorDriver.start()

    handler = i2cHandler.I2cHandler()
    handler.start()

    utilities = drivingUtilities.DrivingUtilities(handler, motorDriver)
    utilities.adjustToWall(direction.direction.LEFT)

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
