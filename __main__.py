
import activity.init
from transitions import Machine
import random
import sys
from modul import display




class Haley(object):

    states = [
        'init',
        {'name': 'setup', 'on_enter': 'initSetup', 'on_exit': 'exitSetup'},
        {'name': 'ready', 'on_enter': 'initReady'},
        {'name': 'waitForGreen', 'on_enter': 'initWaitForGreen'},
        'blindDrive',
        'guidedDrive',
        'turning',
        'buttonDrive',
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
        print("init Setup")
        self.modulDisplay = display.display()


haley = Haley("Haley")
haley.startSetup()

while True:
    q = input("Please enter 'q' to stop:")
    if q.strip() == 'q':
        break