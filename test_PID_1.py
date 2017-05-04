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
    pid.setWindup(0.5)

    while (True):
        ist_dist = i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()
        pid.SetPoint = 0.0
        if pid.update(ist_dist):
            DeltaVelocityLeft_proz = pid.output
            VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
            motor.setVelocityLeft(config.guidedDriveVelocity * VelocityLeft_proz)
            motor.setVelocityRight(config.guidedDriveVelocity)

            print("Reg. Distanz: Soll: 0.000mm, Ist: " + str(round(ist_dist,3)) + "mm, Fehler: " +
                  str(round(ist_dist,3)) + "mm, Out: " + str(round(100 * DeltaVelocityLeft_proz,3)) + "%")


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
