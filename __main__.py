import sys
import time
import stateMachine

class PrenTeam6():
    haley = stateMachine.Haley("Haley")
    haley.startSetup()
    while True:
        time.sleep(1)
        print('Current state: ' + haley.state)
        if haley.state == 'end':
            exit()

if __name__ == "__main__":
    app = PrenTeam6()

    ##app.run()


