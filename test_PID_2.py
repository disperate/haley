from modul import motor
from modul import i2cHandler
from common import pid
import config
from math import atan

from time import sleep

controller = None

try:
    motor = motor.motor()
    motor.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    pid_dist = pid.PID(0.6, 0, 0)
    pid_dist.setWindup(0.5)
    soll_angle = 0

    pid_angle = pid.PID(0.2, 0, 0)
    pid_angle.setWindup(0.5)

    while (True):
        str_change = False
        ist_dist = i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()
        ist_angle = -atan((i2c.getDistanceLeftBack() - i2c.getDistanceLeftFront()) / 180)
        pid_dist.SetPoint = 0.0
#        if pid_dist.update(ist_dist):
#            soll_angle = pid_dist.output
#            pid_angle.SetPoint = soll_angle
#            str_change = True
#            reg1_out_str = "Reg. Distanz: Soll: 0.000mm , Ist: " + str(round(ist_dist, 3)) + "mm , Fehler: " +\
#                           str(round(ist_dist, 3)) + "mm , Out: " + str(round(soll_angle, 1)) + "rad"

        if pid_angle.update(ist_angle):
            DeltaVelocityLeft_proz = pid_angle.output
            VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
            # motor.setVelocityLeft(config.guidedDriveVelocity * VelocityLeft_proz)
            # motor.setVelocityRight(config.guidedDriveVelocity)
            motor.setVelocityLeft(100 * DeltaVelocityLeft_proz)
            motor.setVelocityRight(100 * -DeltaVelocityLeft_proz)
            str_change = True
            reg2_out_str = "Reg. Winkel:  Soll: " + str(round(soll_angle, 3)) + "rad, Ist: " + str(
                round(ist_angle, 3)) + "rad, Fehler: " + str(round(soll_angle - ist_angle, 3)) + "rad, Out: " + str(
                round(100 * DeltaVelocityLeft_proz, 3)) + "%"

        if str_change:
            print("\033c")
#            print(reg1_out_str)
            print(reg2_out_str)

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
