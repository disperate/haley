from modul import motor
from modul import i2cHandler
from common import pid
import config

from time import sleep

controller = None

try:
    motor = motor.motor()
    motor.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    pid = pid.PID(0.01, 0, 0)
    pid.SetPoint = 0.0

    while (True):
        error = i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()
        print(error)
        if pid.update(error):
            motor.setVelocityLeft(config.guidedDriveVelocity * (1 + pid.output))
            motor.setVelocityRight(config.guidedDriveVelocity)

        sleep(0.0001)


except KeyboardInterrupt:
    motor.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    motor.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise
