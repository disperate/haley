import config


class velocityUtilities():
    def __init__(self, i2cHandler):
        self.i2cHandler = i2cHandler

    def getVelocity(self):
        return config.guidedDriveVelocity