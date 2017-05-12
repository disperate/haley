from modul import i2cHandler
from modul import buttonpresser
from time import sleep
import config

controller = None
i2c = None

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
                if (abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()) < 5):
                    sleep(0.01)
                    buttonpresser.stop()
                    sleep(0.02)
                print("shift left")
            else:
                buttonpresser.right()
                if (abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()) < 5):
                    sleep(0.01)
                    buttonpresser.stop()
                    sleep(0.02)
                print("shift_right")
        else:
            buttonpresser.stop()
            sumDiff = 0
            print("Endckeck")
            for i in range(0, 5):
                sumDiff = abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront())
                print("LeftFront:  " + str(i2c.getDistanceLeftFront()))
                print("RightFront: " + str(i2c.getDistanceRightFront()))
                sleep(0.1)
            if sumDiff < 1:
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