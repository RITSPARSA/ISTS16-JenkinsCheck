class Configuration(object):
    def __init__(self):
        # Number of rounds to check
        self.ROUNDS = 2
        # Number of teams
        self.TEAM_COUNT = 5
        # External IP mask
        self.EXTERNAL_IP = "10.80.100.x"
        # Internal IP mask
        self.INTERNAL_IP = "10.2.x.10"
        # The round check we are on
        self.BUILD_NUMBER = 0
        # Connection Timeout in seconds
        self.TIMEOUT = 5
        # Global Username
        self.USERNAME = "scoring"
        # The project name on jenkins
        self.BUILD_NAME = "ShipBuilder"
        # Passwords for the systems
        self.PASSWORDS = {}
        # Build config for windows
        self.WINDOWS_XML = "jobs/windows.xml"
        # Build config for linux
        self.LINUX_XML = "jobs/bsd.xml"

    def updateBuild(self):
        '''Increment the build number
        '''
        self.BUILD_NUMBER += 1

Config = Configuration()
