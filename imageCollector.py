import os
from time import sleep

from picamera import PiCamera

from modul import motor

controller = None

try:

    controller = motor.motor()
    controller.start()

    camera = PiCamera()
    camera.framerate = 10
    camera.resolution = (256, 256)
    camera.exposure_mode = 'sports'
    camera.start_preview()

    # Camera warm-up time
    sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g

    baseNumber = int(input('Base number: '))
    print('ready...')
    while (True):
        directory = input('Choose number (1-5): ')

        if not os.path.exists(directory):
            os.makedirs(directory)

        controller.setVelocityLeft(70.0)
        controller.setVelocityRight(70.0)

        camera.capture_sequence([directory + '/image%00002d.jpg' % i for i in range(baseNumber, baseNumber + 6, 1)])
        baseNumber = baseNumber + 6
        print('Current Number: ' + str(baseNumber))

        controller.setVelocityLeft(0.0)
        controller.setVelocityRight(0.0)
        controller.stop()

except KeyboardInterrupt:
    controller.terminate()
    print("Goodbye!")
except:
    controller.terminate()
    print("Aaaaaargh!")
    raise
