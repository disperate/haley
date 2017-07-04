from time import sleep

from modul import camera
from modul import i2cHandler

try:

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    camera = camera.camera(i2c)
    camera.start()
    sleep(2)

    camera.startGreenlightDedection()


except KeyboardInterrupt:
    camera.terminate()
    print("Goodbye!")
except:
    camera.terminate()
    print("Aaaaaargh!")
    raise
