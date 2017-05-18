
from modul import camera
from time import sleep

try:
    camera = camera.camera()
    camera.start()

    camera.startGreenlightDedection()


except KeyboardInterrupt:
    camera.terminate()
    print("Goodbye!")
except:
    camera.terminate()
    print("Aaaaaargh!")
    raise