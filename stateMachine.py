from threading import Thread

from transitions import Machine

from activity import blindDrive
from activity import buttonPress
from activity import dedectWalls
from activity import guidedDrive
from activity import init
from activity import loseWalls
from activity import loseWallsOneSide
from activity import ready
from activity import turn
from activity import waitForGreen
from modul import camera
from modul import display
from modul import i2cHandler
from modul import motor


class Haley(object):
    states = [
        'init',
        {'name': 'setup', 'on_enter': 'initSetup'},
        {'name': 'ready', 'on_enter': 'initReady'},
        {'name': 'waitForGreen', 'on_enter': 'initWaitForGreen', 'on_exit': 'exitWaitForGreen'},
        {'name': 'blindDrive', 'on_enter': 'initBlindDrive', 'on_exit': 'exitBlindDrive'},
        {'name': 'guidedDrive', 'on_enter': 'initGuidedDrive', 'on_exit': 'exitGuidedDrive'},
        {'name': 'turning', 'on_enter': 'initTurning', 'on_exit': 'exitTurning'},
        {'name': 'buttonDrive', 'on_enter': 'initButtonDrive'},
        'end']

    direction = None

    turned = False

    def __init__(self, name):

        self.name = name
        self.machine = Machine(
            model=self, states=Haley.states, initial='init', auto_transitions=False)

        self.machine.add_transition(
            trigger='startSetup', source='init', dest='setup')

        self.machine.add_transition(
            trigger='setupComplete', source='setup', dest='ready')

        self.machine.add_transition(
            trigger='startPressed', source='ready', dest='waitForGreen')

        self.machine.add_transition(
            trigger='greenlight', source='waitForGreen', dest='blindDrive')

        self.machine.add_transition(
            trigger='wallsDedected', source='blindDrive', dest='guidedDrive')

        self.machine.add_transition(
            trigger='wallsLost', source='guidedDrive', dest='turning', unless='hasTurned')

        self.machine.add_transition(
            trigger='wallsLost', source='guidedDrive', dest='buttonDrive', conditions='hasTurned')

        self.machine.add_transition(
            trigger='turnDone', source='turning', dest='blindDrive')

        self.machine.add_transition(
            trigger='buttonPressed', source='buttonDrive', dest='end')

    def initSetup(self):

        ##init all modules
        self.displayModul = display.display()

        self.cameraModul = camera.camera()
        self.cameraModul.start()

        self.motorModul = motor.motor()
        self.motorModul.start()

        self.i2c = i2cHandler.I2cHandler()
        self.i2c.start()

        i = init.initActivity(self, self.i2c)

    def initReady(self):
        t = Thread(target=ready.readyActivity, args=(self,))
        t.start()

    def initWaitForGreen(self):
        t = Thread(target=waitForGreen.waitForGreenActivity, args=(self, self.cameraModul))
        t.start()

    def exitWaitForGreen(self):
        self.cameraModul.stopGreenlightDedection()
        self.cameraModul.startRomanNumberDedection()

    def initBlindDrive(self):

        self.blindDriveActivity = blindDrive.blindDriveActivity(self, self.motorModul)
        self.blindDriveActivity.start()

        dedectWallsThread = Thread(target=dedectWalls.dedectWallsActivity, args=(self, self.i2c))
        dedectWallsThread.start()

    def exitBlindDrive(self):
        self.blindDriveActivity.terminate()

    def initGuidedDrive(self):
        self.guidedDriveActivity = guidedDrive.guidedDriveActivity(self, self.motorModul, self.i2c)
        self.guidedDriveActivity.start()
        if self.hasTurned():
            wallsLostThread = Thread(target=loseWallsOneSide.loseWallsActivity, args=(self, self.i2c, self.direction))
            wallsLostThread.start()
        else:
            wallsLostThread = Thread(target=loseWalls.loseWallsActivity, args=(self, self.i2c))
            wallsLostThread.start()

    def exitGuidedDrive(self):
        self.guidedDriveActivity.terminate()

    def initTurning(self):
        self.cameraModul.stopRomanNumberDedection()
        turnThread = turn.turnActivity(self, self.motorModul, self.i2c)
        turnThread.start()

    def exitTurning(self):
        self.cameraModul.startRomanNumberDedection()

    def initButtonDrive(self):
        buttonPresser = buttonPress.buttonPressActivity(self, self.motorModul, self.i2c)
        buttonPresser.start()

    def hasTurned(self):
        return self.turned
