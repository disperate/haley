from time import sleep

from modul import camera
from modul import i2cHandler
from modul import motor

try:
    i2c = i2cHandler.I2cHandler()
    i2c.start()

    camera = camera.camera(i2c)
    camera.start()

    controller = motor.motor()
    controller.start()

    while True:
        camera.startRomanNumberDedection()
        controller.setVelocityLeft(60.0)
        controller.setVelocityRight(60.0)

        sleep(6)

        controller.setVelocityLeft(0.0)
        controller.setVelocityRight(0.0)
        camera.stopRomanNumberDedection()

        input("Press Enter to continue...")

    controller.stop()


except KeyboardInterrupt:
    camera.terminate()
    print("Goodbye!")
except:
    camera.terminate()
    print("Aaaaaargh!")
    raise
