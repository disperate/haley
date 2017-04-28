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

    pid_dist = pid.PID(0.6, 0, 0)
    pid_dist.SetPoint = 0.0

    pid_angle = pid.PID(0.2, 0, 0)
    pid_angle.SetPoint = 0.0

    while (True):
        error_dist = i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()
        error_angle = atan( (i2c.getDistanceLeftBack()-i2c.getDistanceLeftFront()) / 180 )
        print(error_dist)
        print(error_angle)
        if pid_dist.update(error_dist):
            pid_angle.SetPoint = pid_dist.output
        if pid_angle.update(error_angle):
            #motor.setVelocityLeft(config.guidedDriveVelocity * (1 + pid_angle.output))
            #motor.setVelocityRight(config.guidedDriveVelocity)
            motor.setVelocityLeft(0 * (1 + pid_angle.output))
            motor.setVelocityRight(0)

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
