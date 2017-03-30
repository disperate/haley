import time
import stateMachine

haley = stateMachine.Haley("Haley")
haley.startSetup()

while True:
    time.sleep(2)
    print('Current state: ' + haley.state)
    if haley.state == 'end':
        break