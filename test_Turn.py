from time import sleep

from modul import i2cHandler
from modul import motor

try:
    motor = motor.motor()
    motor.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    startAngle = i2c.currYaw

    endAngleUnder = startAngle + 89
    endAngleUpper = startAngle + 91

    if endAngleUnder > 360:
        endAngleUnder - 360

    if endAngleUpper > 360:
        endAngleUpper - 360

    motor.setVelocityLeft(60)
    motor.setVelocityRight(-60)
    while (True):
        currentAngle = i2c.currYaw

        if (endAngleUnder - currentAngle < 20):
            motor.setVelocityLeft(20)
            motor.setVelocityRight(-20)

        if currentAngle > endAngleUpper:
            motor.setVelocityLeft(-20)
            motor.setVelocityRight(20)

        print("\033c")
        print("Start Angle:" + str(startAngle))
        print("endAngleUnder" + str(endAngleUnder))
        print("endAngleUpper" + str(endAngleUpper))
        print("Current Angle:" + str(currentAngle))

        if (currentAngle > endAngleUnder and currentAngle < endAngleUpper):
            break

        sleep(0.1)

    motor.setVelocityLeft(0)
    motor.setVelocityRight(0)

except KeyboardInterrupt:
    motor.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    motor.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise
