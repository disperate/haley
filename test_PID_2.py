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

    pid_dist = pid.PID(0.002, 0, 0)
    pid_dist.setWindup(0.5)
    pid_dist.sample_time = 0.1
    soll_angle = 0

    pid_angle = pid.PID(1.5, 0, 0)
    pid_angle.setWindup(0.5)
    pid_angle.sample_time = 0.1

    print("Test: 1.0 ")
    print("Time; SollD; IstD; ErrD; OutD; ; SollW; IstW; ErrW; OutW;")

    regD_out_str = ""
    regW_out_str = ""

    cnt = 1
    while(True):
        print("\033c")
        print("Wait for Distance-Data (Try " + str(cnt) + "): " + \
             str(i2c.getDistanceLeftFront()) +", "+ str(i2c.getDistanceRightFront()) +", "+\
             str(i2c.getDistanceLeftBack()) +", "+ str(i2c.getDistanceLeftBack()))
        if (i2c.getDistanceLeftFront() > 0):
            if (i2c.getDistanceLeftBack() > 0):
                if (i2c.getDistanceRightFront() > 0):
                    if (i2c.getDistanceRightBack() > 0):
                        break;
        cnt = cnt + 1
        sleep(0.1)

    while (True):
        ist_dist = i2c.getDistanceLeftBack() - i2c.getDistanceRightBack()
        ist_angle = atan((i2c.getDistanceLeftFront() - (i2c.getDistanceLeftBack()-0.5)) / 180)
        pid_dist.SetPoint = 0.0
        if pid_dist.update(ist_dist):
            soll_angle = pid_dist.output
            pid_angle.SetPoint = soll_angle
            regD_out_str = str(round(pid_dist.SetPoint, 3)) +"; " + str(round(ist_dist, 3)) + "; " +\
                           str(round(pid_dist.SetPoint-ist_dist, 3)) +"; "+ str(round(soll_angle, 1)) +"; ;"

        if pid_angle.update(ist_angle):
            DeltaVelocityLeft_proz = pid_angle.output
            VelocityLeft_proz = 1 + DeltaVelocityLeft_proz
            motor.setVelocityLeft(config.guidedDriveVelocity)
            motor.setVelocityRight(config.guidedDriveVelocity * VelocityLeft_proz)
            #motor.setVelocityLeft(config.guidedDriveVelocity * -DeltaVelocityLeft_proz)
            #motor.setVelocityRight(config.guidedDriveVelocity * DeltaVelocityLeft_proz)
            regW_out_str = str(round(soll_angle, 3)) +" ; "+ str(round(ist_angle, 3)) +" ; "+\
                           str(round(soll_angle-ist_angle, 3)) +" ; "+\
                           str(round(DeltaVelocityLeft_proz,5))

            #print("\033c")
            print(str(round(pid_dist.current_time,3)) +"; "+ regD_out_str + regW_out_str)
            regD_out_str = ""
            regW_out_str = ""

        sleep(0.02)


except KeyboardInterrupt:
    motor.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    motor.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise