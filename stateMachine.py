from transitions import Machine
from threading import Thread

from modul import display
from modul import camera
from activity import init
from activity import ready
from activity import waitForGreen
from activity import blindDrive
from activity import dedectWalls

class Haley(object):

    states = [
        'init',
        {'name': 'setup', 'on_enter': 'initSetup'},
        {'name': 'ready', 'on_enter': 'initReady'},
        {'name': 'waitForGreen', 'on_enter': 'initWaitForGreen', 'on_exit' : 'exitWaitForGreen'},
        {'name': 'blindDrive','on_enter': 'initBlindDrive', 'on_exit' : 'exitBlindDrive'},
        {'name': 'guidedDrive', 'on_enter': 'initGuidedDrive'},
        {'name': 'turning', 'on_enter': 'initTurning'},
        {'name': 'buttonDrive','on_enter': 'initButtonDrive'},
        'end']

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
            trigger='turnDone', source='turning', dest='blindDrive')

        self.machine.add_transition(
            trigger='wallsLost', source='guidedDrive', dest='buttonDrive', conditions='hasTurned')

        self.machine.add_transition(
            trigger='buttonPressed', source='buttonDrive', dest='end')


    def initSetup(self):

        ##init all modules
        self.modulDisplay = display.display()

        self.cameraModul = camera.camera()
        self.cameraModul.start()

        i = init.initActivity(self)

    def initReady(self):
        t = Thread(target=ready.readyActivity, args = (self,))
        t.start()

    def initWaitForGreen(self):
        t = Thread(target=waitForGreen.waitForGreenActivity, args=(self, self.cameraModul))
        t.start()

    def exitWaitForGreen(self):
        self.cameraModul.stopGreenlightDedection()


    def initBlindDrive(self):
        self.blindDriver = blindDrive.blindDriveActivity(self)

        blindDriverThread = Thread(target=self.blindDriver.run, args=())
        blindDriverThread.start()

        t2 = Thread(target=dedectWalls.dedectWallsActivity, args=(self,))
        t2.start()

    def exitBlindDrive(self):
        self.blindDriver.terminate()