from modul import motor
from modul import i2cHandler
import config

from time import sleep

try:
    motor = motor.motor()
    motor.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()
    sleep(2)

    angle = -45.0
    velocity_max = 50.0
    currVelocity = 0.5
    startVelocityCounter = 0

    i2c.resetRelativeYaw()

    if(angle < 0):
        # Turn left
        print("Start: CurrentRelative -> {}, Gyro --> {}".format(i2c.currRelativeYaw, i2c.getCurrYaw()))
        #currVelocity = velocity_max
        while(True):
            currDelta = abs(angle) - abs(i2c.currRelativeYaw)
            # Anfahren
            if(currDelta > (abs(angle) - 15)):
                if(currVelocity < velocity_max):
                    currVelocity = currVelocity + 0.025
                    motor.setVelocityLeft(-currVelocity)
                    motor.setVelocityRight(currVelocity)
                    continue

            # Stoppen
            if (currDelta < 2):
                motor.setVelocityLeft(0.0)
                motor.setVelocityRight(0.0)
                break

            # Bremsen
            if (currDelta <= 15):
                currVelocity = (velocity_max / 15.0) * currDelta
                motor.setVelocityLeft(-currVelocity)
                motor.setVelocityRight(currVelocity)
                continue

            sleep(0.1)
        print("Stop: CurrentRelative -> {}, Gyro --> {}".format(i2c.currRelativeYaw, i2c.getCurrYaw()))
    else:
        # Turn right
        while(True):
            pass

    motor.terminate()
    i2c.terminate()



except KeyboardInterrupt:
    motor.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    motor.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise
