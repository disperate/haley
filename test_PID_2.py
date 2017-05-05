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

    pid_dist = pid.PID(0.01, 0, 0)
    pid_dist.setWindup(0.5)
    pid_dist.sample_time = 0.01
    soll_angle = 0

    pid_angle = pid.PID(0.03, 0, 0)
    pid_angle.setWindup(0.3)
    pid_angle.sample_time = 0.01

    print("Test: 1.0 ")
    print("Time; SollD; IstD; ErrD; OutD; ; SollW; IstW; ErrW; OutW;")

    while (True):
        ist_dist = i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()
        ist_angle = atan((i2c.getDistanceLeftFront() - (i2c.getDistanceLeftBack()-0.5)) / 180)
        pid_dist.SetPoint = 0.0
        if pid_dist.update(ist_dist):
            soll_angle = pid_dist.output
            pid_angle.SetPoint = soll_angle
            regD_out_str = str(round(pid_dist.current_time,0)) +"; "+ str(round(ist_dist, 3)) +"; "+\
                           str(round(ist_dist, 3)) +"; "+ str(round(soll_angle, 1)) +"; "

            if pid_angle.update(ist_angle):
                DeltaVelocityLeft_proz = pid_angle.output
                VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
                motor.setVelocityLeft(config.guidedDriveVelocity * VelocityLeft_proz)
                motor.setVelocityRight(config.guidedDriveVelocity)
    #            motor.setVelocityLeft(100 * DeltaVelocityLeft_proz)
    #            motor.setVelocityRight(100 * -DeltaVelocityLeft_proz)
                regW_out_str = str(round(soll_angle, 3)) +" ; "+ str(round(ist_angle, 3)) +" ; "+\
                               str(round(soll_angle-ist_angle, 3)) +" ; "+\
                               str(round(DeltaVelocityLeft_proz,3))

            #print("\033c")
            print(regD_out_str + regW_out_str)
            regD_out_str = ""
            regW_out_str = ""

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