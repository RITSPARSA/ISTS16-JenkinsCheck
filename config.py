class Configuration(object):
    def __init__(self):
        # Number of teams
        self.TEAM_COUNT = 5
        # External IP mask
        self.EXTERNAL_IP = "10.80.100.x"
        # Internal IP mask
        self.INTERNAL_IP = "10.2.x.10"
        # The round check we are on
        self.BUILD_NUMBER = 0

    def updateBuild(self):
        '''Increment the build number
        '''
        self.BUILD_NUMBER += 1

Config = Configuration()
