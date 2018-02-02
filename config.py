class Configuration(object):
    def __init__(self):
        ###########################
        ## Round/Team Information
        ###########################
        # Number of teams
        self.TEAM_COUNT = 5
        # External IP mask
        self.TEAM_EXT_IP = "10.3.x.20"

        ###########################
        ## Build/Check Information
        ###########################
        # Connection Timeout in seconds
        self.CHECK_TIMEOUT = 10
        # Username for the jenkins boxes
        self.CHECK_USERNAME = "scoring"
        # The project name on jenkins
        self.CHECK_BUILD_NAME = "ShipBuilder"
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
        
        # Hashes that identify the teams
        self.HASHES = ["c4ca4238a0b923820dcc509a6f75849b",
        "c81e728d9d4c2f636f067f89cc14862c",
        "eccbc87e4b5ce2fe28308fd9f2a7baf3",
        "a87ff679a2f3e71d9181a67b7542122c",
        "e4da3b7fbbce2345d7772b0674a318d5",
        "1679091c5a880faf6fb5e6087eb1b2dc",
        "8f14e45fceea167a5a36dedd4bea2543",
        "c9f0f895fb98ab9159f51fd0297e236d",
        "45c48cce2e2d7fbdea1afc51c7c6ad26",
        "d3d9446802a44259755d38e6d163e820",
        "6512bd43d9caa6e02c990b0a82652dca"]

Config = Configuration()
