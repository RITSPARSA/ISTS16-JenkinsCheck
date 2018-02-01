# Iterate through all the hosts
from creds import creds
from config import Config
from hostManager import HostMan
import jenkins, json
import sys, logging, re

def iterateHosts(mask, count, action):
    '''
    Iterate through the number of hosts specified, Calculate the IP to use,
    and execute "action" on the given ip
    '''
    for i in range(1,count+1):
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
    # add the code to increase the ship for this team

def connect(ip):
    url = "http://{}:8080".format(ip)
    user = Config.USERNAME
    pw = Config.PASSWORDS.get(ip, 'Changeme-2018')
    try:
        logging.debug("{} - Attempting to login {}:{}".format(ip, user, pw))
        return jenkins.Jenkins(url, user, pw, timeout=Config.TIMEOUT)
    except Exception as e:
        logging.warn("Issue connecting to {}: {}").format(url, e)
        return False

''' Build if connection there '''
def build(ip):
    '''Trigger a build job on a remote server'''
    server = connect(ip)
    if submitJob(server, ip):
        try:
            # start the job (name of the job to build)
            server.build_job(creds.buildName)
            logging.info("{} - Triggering build on host".format(ip))
            HostMan.passHost(ip)
            return True
        except Exception as e:
            logging.error(e)
            HostMan.failHost(ip)
            return False
    return False


def check(ip):
    '''Stub Function'''
    # the desired build result
    success='SUCCESS'
    # connect to the server 
    server = connect(ip)
    try:
        # get the last build number (name of the build to get)
        build_num = server.get_job_info(creds.buildName)['lastBuild']['number']
        # retrieve the output of the build (name of build, number of that build)
        output = server.get_build_console_output(creds.buildName, build_num)
        # ensure output contains success and whiteteamKEY
        if (success in output) and (creds.whiteteamKEY in output):
            logging.info("{} - Build succeeded".format(ip))
        else:
            logging.info("{} - Build failed".format(ip))
        return True
    except Exception as e:
        logging.error("{} - Failure in check. {}".format(ip, e))
        return False

def submitJob(server, ip):
    try:
        if not server.job_exists(creds.buildName):
            # read xml file into variable
            if ip.split(".")[:2] = Config.EXTERNAL_IP.split(".")[:2]:
                # Read windows if looking at the external IP
                xmlFile = Config.WINDOWS_XML
                jobType = "Windows"
            else:
                # Read linux if looking at the internal IP
                xmlFile = Config.LINUX_XML
                jobType = "Linux"
            # open the xml
            xml=open(xmlFile, 'r').read()
            server.create_job(creds.buildName, xml)
            logging.info("{} - Submitted {} job to host".format(ip,
                jobType))
        return True
    except Exception as e:
        logging.warn("{} - {}".format(ip, e))
        return False


def main():
    logging.basicConfig(filename="jenkins-check.log", level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s')
    logging.info("====== Started Program ======")
    for i in range(2):
        # Load any changed password before each round
        Config.PASSWORDS = json.load(open('passwords.json'))
        logging.debug("Loading new passwords")
        # Reset the hosts to look at
        HostMan.nextRound()
        logging.debug("Resetting known hosts")
        logging.info("----- Starting Round {}-----".format(HostMan.ROUND_NUM))
        # Go through all the hosts and try to submit a job
        iterateHosts(Config.EXTERNAL_IP, Config.TEAM_COUNT, build)
        iterateHosts(Config.INTERNAL_IP, Config.TEAM_COUNT, build)
        # Loop through all the hosts that accepted a build
        # and check the build status
        for host in HostMan.WORKED:
            check(host)
        
if __name__ == '__main__':
    main()
