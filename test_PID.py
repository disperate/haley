from math import atan

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
        error_angle = atan((i2c.getDistanceLeftFront()-i2c.getDistanceLeftBack()) / 180)
        print("\033c")
        print("DIST: "+ str(error_dist))
        print("ANGL: " + str(error_angle))
        if pid_dist.update(error_dist):
            print("pid_dist: " + str(pid_dist.output))
            pid_angle.SetPoint = pid_dist.output
        if pid_angle.update(error_angle):
            #motor.setVelocityLeft(config.guidedDriveVelocity * (1 + pid_angle.output))
            #motor.setVelocityRight(config.guidedDriveVelocity)
            print("pid_angle: " + str(pid_angle.output))
            motor.setVelocityLeft(100*(pid_angle.output))
            motor.setVelocityRight(-100*(pid_angle.output))

        sleep(0.1)


except KeyboardInterrupt:
    motor.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    motor.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise
