import config


class velocityUtilities():
    def __init__(self, i2cHandler):
        self.i2cHandler = i2cHandler

    # Returns a velocity based on the current Roll level.
    # Roll +/- 10° => 80%
    # Roll +/- 15° => 70%
    # Roll +/- 20° => 60%

    def getVelocity(self):
        roll = int(self.i2cHandler.getCurrRoll())

        if (roll > 180):
            if (roll < 340):
                return config.guidedDriveVelocity * 0.6
            if (roll < 345):
                return config.guidedDriveVelocity * 0.7
            if (roll < 350):
                return config.guidedDriveVelocity * 0.8
        else:
            if (roll > 20):
                return config.guidedDriveVelocity * 0.6
            if (roll > 15):
                return config.guidedDriveVelocity * 0.7
            if (roll > 10):
                return config.guidedDriveVelocity * 0.8

        return config.guidedDriveVelocity
