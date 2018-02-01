class Configuration(object):
    def __init__(self):
        # Number of teams
        self.TEAM_COUNT = 5
        # External IP mask
        self.EXTERNAL_IP = "10.3.x.20"
        # Internal IP mask
        # self.INTERNAL_IP = "10.2.x.10"
        self.INTERNAL_IP = "10.80.100.x"
        # The round check we are on
        self.BUILD_NUMBER = 0
        # Connection Timeout in seconds
        self.TIMEOUT = 10
        # Global Username
        self.USERNAME = "scoring"
        # Passwords for the systems
        self.PASSWORDS = {}
        # Build config for windows
        self.WINDOWS_XML = "jobs/windows.xml"
        # Build config for linux
        self.LINUX_XML = "jobs/bsd.xml"
        # whiteteam defined key to look for in output
        self.ROUNDFLAG='452345234523452345'
        # name of the build to run
        self.buildName='VegaBuild'

    def updateBuild(self):
        '''Increment the build number
        '''
        self.BUILD_NUMBER += 1

Config = Configuration()
