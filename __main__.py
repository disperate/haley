import time

from transitions import Machine

from modul import display
from activity import init
from activity import ready
from activity import waitForGreen
from activity import blindDrive


class Haley(object):

    states = [
        'init',
        {'name': 'setup', 'on_enter': 'initSetup'},
        {'name': 'ready', 'on_enter': 'initReady'},
        {'name': 'waitForGreen', 'on_enter': 'initWaitForGreen'},
        {'name': 'blindDrive','on_enter': 'initBlindDrive'},
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

        i = init.initActivity(self)

    def initReady(self):
        i = ready.readyActivity(self)

    def initWaitForGreen(self):
        i = waitForGreen.waitForGreenActivity(self)

    def initBlindDrive(self):
        i = blindDrive.blindDriveActivity(self)




haley = Haley("Haley")
haley.startSetup()

while True:
    time.sleep(2)
    print('Current state: ' + haley.state)
    if haley.state == 'end':
        break