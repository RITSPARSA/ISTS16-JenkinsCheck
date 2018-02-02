# Iterate through all the hosts
from config import Config
from hostManager import HostMan
import tok
import jenkins, json, logging, re, sys, time

def iterateHosts(mask, count, action):
    '''
    Iterate through the number of hosts specified, Calculate the IP to use,
    and execute "action" on the given ip
    '''
    # for i in range(1,count+1):
    for i in range(12,count+10):
        ip = mask.replace("x",str(i))
        action(ip)

def incrementShips(ip, flag):
    '''Determine the type of ship based on the IP
    Activate on a certain team based on the flag
    '''
    # Determine the team number based on the flag
    try:
        teamNum = re.findall('\d+', flag)[0]
    except:
        teamNum = ip.split(".")[3]
    # Check if we are building Bombers or Guardians
    if ip.split(".")[:2] == Config.TEAM_EXT_IP.split(".")[:2]:
        # Wolf makes bombers
        shipType = "bombers"
    else:
        # Vega makes guardians
        shipType = "guardian"

    data = { "value": 1 }
    url = Config.API_SHIP_URL
    endpoint = "teams/{}/{}".format(teamNum, shipType)

    try:
        tok.apiRequest(url, endpoint, data=data)
        logging.info("{} - {} built for team {}".format(ip, shipType,
            teamNum))
    except Exception as e:
        logging.error("{} - Error building ship: {}".format(
            ip, e))

def connect(ip):
    '''Make a connection to the jenkins server at IP
    '''
    url = "http://{}:8080".format(ip)
    user = Config.CHECK_USERNAME
    pw = Config.CHECK_PASSWORDS.get(ip, 'Changeme-2018')
    try:
        logging.debug("{} - Attempting to login {}:{}".format(ip, user, pw))
        return jenkins.Jenkins(url, user, pw, timeout=Config.CHECK_TIMEOUT)
    except Exception as e:
        logging.warn("Issue connecting to {}: {}").format(url, e)
        return False

def build(ip):
    '''Trigger a build job on a remote server
    If the job doesnt exist, submit the job
    '''
    server = connect(ip)
    if submitJob(server, ip):
        try:
            # start the job (name of the job to build)
            server.build_job(Config.CHECK_BUILD_NAME)
            logging.info("{} - Triggering build on host".format(ip))
            HostMan.passHost(ip)
            return True
        except Exception as e:
            logging.warn(e)
            HostMan.failHost(ip)
            return False
    return False


def check(ip):
    '''Check whether the build succeeded or failed
    '''
    # the desired build result
    success='SUCCESS'
    # connect to the server
    server = connect(ip)
    try:
        # get the last build number (name of the build to get)
        build_num = server.get_job_info(
            Config.CHECK_BUILD_NAME)['lastBuild']['number']
        # retrieve the output of the build (name of build, number of that build)
        output = server.get_build_console_output(Config.CHECK_BUILD_NAME,
            build_num)
        # ensure output contains success and whiteteamKEY
        if (success in output) and (Config.ROUNDFLAG in output):
            try:
                flag = re.findall('====.+====', output)[0]
            except:
                flag = 'fail'
            incrementShips(ip, flag)
            logging.info("{} - Build succeeded".format(ip))
        else:
            logging.info("{} - Build failed".format(ip))
        return True
    except Exception as e:
        logging.warn("{} - Failure in check. {}".format(ip, e))
        return False

def submitJob(server, ip):
    '''Submit a job to the server. If windows then submit windows job,
    if linux, submit linux job
    '''
    try:
        if not server.job_exists(Config.CHECK_BUILD_NAME):
            # read xml file into variable
            if ip.split(".")[:2] == Config.TEAM_EXT_IP.split(".")[:2]:
                # Read windows if looking at the external IP
                xmlFile = Config.CHECK_WINDOWS
                jobType = "Windows"
            else:
                # Read linux if looking at the internal IP
                xmlFile = Config.CHECK_LINUX
                jobType = "Linux"
            # open the xml
            xml=open(xmlFile, 'r').read()
            server.create_job(Config.CHECK_BUILD_NAME, xml)
            logging.info("{} - Submitted {} job to host".format(ip,
                jobType))
        return True
    except Exception as e:
        logging.warn("{} - {}".format(ip, e))
        return False


def main():

    logFormatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler("jenkins-check.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    
    logging.info("====== Started Program ======")
    
    # Get the API token or error
    tok.getToken()

    # Number of rounds
    for i in range(Config.ROUNDS):
        # Load any changed password before each round
        Config.CHECK_PASSWORDS = json.load(open('passwords.json'))
        logging.debug("Loading new passwords")
        # Reset the hosts to look at
        HostMan.nextRound()
        logging.debug("Resetting known hosts")
        logging.info("----- Starting Round {}-----".format(HostMan.ROUND_NUM))
        # Go through all the hosts and try to submit a job
        iterateHosts(Config.TEAM_EXT_IP, Config.TEAM_COUNT, build)
        iterateHosts(Config.TEAM_INT_IP, Config.TEAM_COUNT, build)
        # give the job time to run
        time.sleep(5)
        # Loop through all the hosts that accepted a build
        # and check the build status
        for host in HostMan.WORKED:
            check(host)

if __name__ == '__main__':
    main()
