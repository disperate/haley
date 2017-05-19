from common import velocityUtilities
from modul import i2cHandler
from time import sleep
from modul import motor

try:
    i2cHandler = i2cHandler.I2cHandler()
    i2cHandler.start()

    motor = motor.motor()
    motor.start()

    velocityUtilities = velocityUtilities.velocityUtilities(i2cHandler)

    while (True):
        velocity = velocityUtilities.getVelocity()
        print(velocity)
        motor.setVelocityLeft(velocity)
        motor.setVelocityRight(velocity)

        sleep(0.1)

    i2cHandler.terminate()

except KeyboardInterrupt:
    i2cHandler.terminate()
    motor.terminate()
    print("Goodbye!")
except:
    i2cHandler.terminate()
    motor.terminate()
    print("Aaaaaargh!")
    raise
