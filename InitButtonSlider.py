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

    moveButtonSlider = True
    print("Start init Buttonslider")
    while moveButtonSlider:
        print("LeftFront:  " + str(i2c.getDistanceLeftFront()))
        print("RightFront: " + str(i2c.getDistanceRightFront()))
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