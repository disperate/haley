from modul import i2cHandler
from time import sleep
from modul import fork
import config

controller = None
i2c = None

try:
    forkHandler = fork.fork()

    i2c = i2cHandler.I2cHandler()
    i2c.start()

    moveButtonSlider = True
    # print("Start init Buttonslider")
    while moveButtonSlider:
        # print("LeftFront:  " + str(i2c.getDistanceLeftFront()))
        # print("RightFront: " + str(i2c.getDistanceRightFront()))
        if (i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()):
            if (i2c.getDistanceLeftFront() > i2c.getDistanceRightFront()):
                forkHandler.moveLeft()
                if (abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()) < 5):
                    sleep(0.01)
                    forkHandler.stopMovement()
                    sleep(0.02)
                print("shift left")
            else:
                forkHandler.moveRight()
                if (abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront()) < 5):
                    sleep(0.01)
                    forkHandler.stopMovement()
                    sleep(0.02)
                print("shift_right")
        else:
            forkHandler.stopMovement()
            sumDiff = 0
            # print("Endckeck")
            for i in range(0, 5):
                sumDiff += abs(i2c.getDistanceLeftFront() - i2c.getDistanceRightFront())
                print("LeftFront:  " + str(i2c.getDistanceLeftFront()))
                print("RightFront: " + str(i2c.getDistanceRightFront()))
                sleep(0.1)
            if sumDiff < 3:
                #print("stop")
                moveButtonSlider = False
        sleep(0.01)


except KeyboardInterrupt:
    i2c.terminate()
    print("Goodbye!")
except:
    i2c.terminate()
    print("Aaaaaargh!")
    raise