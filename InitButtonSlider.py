from modul import i2cHandler
from modul import buttonpresser
from time import sleep
import config

controller = None

try:
    buttonpresser = buttonpresser.buttonpresser()
    buttonpresser.start()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    moveButtonSlider = True
    print("Start init Buttonslider")
    while moveButtonSlider:
        deltaLeft = i2c.getDistanceLeftBack() - i2c.getDistanceLeftFront()
        deltaRight = i2c.getDistanceRightBack() - i2c.getDistanceRightFront()
        if (i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()):
            if (i2c.getDistanceLeftFront() > i2c.getDistanceRightFront()):
                buttonpresser.left()
                print("shift left")
            else:
                buttonpresser.right()
                print("shift_right")
        else:
            buttonpresser.stop()
            print("stop")
            moveButtonSlider = False
        sleep(0.01)


except KeyboardInterrupt:
    buttonpresser.terminate()
    i2c.terminate()
    print("Goodbye!")
except:
    buttonpresser.terminate()
    i2c.terminate()
    print("Aaaaaargh!")
    raise