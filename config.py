class Configuration(object):
    def __init__(self):
        ###########################
        ## Round/Team Information
        ###########################
        # Number of rounds to check
        self.ROUNDS = 2
        # Number of teams
        self.TEAM_COUNT = 5
        # External IP mask
        self.TEAM_EXT_IP = "10.3.x.20"
        # Internal IP mask
        # self.INTERNAL_IP = "10.2.x.10"
        self.TEAM_INT_IP = "10.80.100.x"



        ###########################
        ## Build/Check Information
        ###########################
        # Connection Timeout in seconds
        self.CHECK_TIMEOUT = 10
        # Username for the jenkins boxes
        self.CHECK_USERNAME = "scoring"
        # The project name on jenkins
        self.CHECK_BUILD_NAME = "ShipBuilder"
        # Passwords for the systems
        self.CHECK_PASSWORDS = {}
        # Build config for windows
        self.CHECK_WINDOWS = "jobs/windows.xml"
        # Build config for linux
        self.CHECK_LINUX = "jobs/bsd.xml"
        # whiteteam defined key to look for in output
        self.CHECK_FLAG = 'testing'

        ###########################
        ## API Information
        ###########################
        self.API_TOK = ""
        self.API_USERNAME = "theblindmice"
        self.API_PASSWORD = "basedgodboyuan1016"
        self.API_SHIP_URL = "http://lilbite.org:6000"
        self.API_AUTH_URL = "http://lilbite.org:9000"


    def updateBuild(self):
        '''Increment the build number
        '''
        self.BUILD_NUMBER += 1

Config = Configuration()
