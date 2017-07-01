from time import sleep

from modul import motor

controller = None

try:
    controller = motor.motor()
    controller.start()
    controller.startLogging()

    print("1")
    controller.setVelocityLeft(100.0)
    controller.setVelocityRight(100.0)
    sleep(1)
    print("2")
    controller.setVelocityLeft(50.0)
    controller.setVelocityRight(-50.0)
    sleep(1)
    print("3")
    controller.setVelocityLeft(-50.0)
    controller.setVelocityRight(50.0)
    sleep(1)
    print("4")
    controller.setVelocityLeft(-100.0)
    controller.setVelocityRight(-100.0)
    sleep(1)

    print("Stop Logging")
    controller.stopLogging()
    controller.terminate()
except KeyboardInterrupt:
    controller.terminate()
    print("Goodbye!")
except:
    controller.terminate()
    print("Aaaaaargh!")
    raise
