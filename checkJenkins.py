#!/usr/bin/python
from config import Config
import tok
import jenkins
import sys
import time


def connect(ip, passwd):
    '''Make a connection to the jenkins server at IP
    '''
    user = Config.CHECK_USERNAME
    url = "http://{}:8080/".format(ip)
    print("[*] Attempting to login via {}:{}".format(user, passwd))
    return jenkins.Jenkins(url, user, passwd, timeout=Config.CHECK_TIMEOUT)

def submitJob(ip, password):
    '''Submit a job to the server. If windows then submit windows job,
    if linux, submit linux job
    '''
    jobName = Config.CHECK_BUILD_NAME
    # Conenct to the server
    server = connect(ip, password)
    
    # Check if job exists. If so, delete it
    if server.job_exists(jobName):
        server.delete_job(jobName)
    # Get the right XML file
    if getHostname(ip) == "wolf":
        # Load windows config
        xmlFile = Config.CHECK_WINDOWS
        jobType = "Windows"
    else:
        # Read linux config
        xmlFile = Config.CHECK_LINUX
        jobType = "Linux"
    # Read the XML and submit it as a job
    xml=open(xmlFile, 'r').read()
    server.create_job(jobName, xml)
    # Build the job
    server.build_job(Config.CHECK_BUILD_NAME)
    print("[+] Submitted {} job to host".format(ip, jobType))

def checkJob(ip, password):
    '''wait for the build to finish then return status
    '''
    success='SUCCESS'
    jobName = Config.CHECK_BUILD_NAME
    # connect to the server
    server = connect(ip, password)
    # Wait for the job to finish
    count = 0
    while jobName in [d['name'] for d in server.get_running_builds()]:
        count += 1
        if count > 12:
            print("[-] waiting too long")
            exitFailed()
        time.sleep(10)
        print("[*] waiting on build...")
        
    # get the last build number (name of the build to get)
    build_num = server.get_job_info(
        Config.CHECK_BUILD_NAME)['lastBuild']['number']
    # retrieve the output of the build (name of build, number of that build)
    output = server.get_build_console_output(Config.CHECK_BUILD_NAME,
        build_num)
    # ensure output contains success and whiteteamKEY
    if (success not in output) or (Config.CHECK_FLAG not in output):
        print("[-] Build failed")
        return False
    # Find the flag in the output
    try:
        flag = re.findall('==== .+', output)[0]
    except:
        flag = "aaaaaaa"
    return incrementShips(ip, flag)


def incrementShips(ip, flag):
    '''Determine the type of ship based on the IP
    Activate on a certain team based on the flag
    '''
    # Determine the team number based on the flag
    try:
        teamNum = Config.HASHES.index(flag[4:].strip())
    except:
        teamNum = ip.split(".")[3]
    # Check if we are building Bombers or Guardians
    if getHostname(ip) == "wolf":
        # Wolf makes bombers
        shipType = "bomber"
    else:
        # Vega makes guardians
        shipType = "guardian"

    tok.getToken()
    data = { "value": 1 }
    url = Config.API_SHIP_URL
    endpoint = "teams/{}/{}".format(teamNum, shipType)

    try:
        tok.apiRequest(url, endpoint, data=data)
        print("[+] Build ships")
        return True
    except Exception as e:
        print("[!] Error building ships: {}".format(e))
        raise e

def getHostname(ip):
    '''Convert an IP address to a hostname
    '''
    if ip.split(".")[:2] == Config.TEAM_EXT_IP.split(".")[:2]:
        return "wolf"
    else:
        return "vega"


def main():
    try:
        if len(sys.argv) < 3:
            raise Exception("Please provide ip and username")
        ip = sys.argv[1]
        password = sys.argv[2]
        submitJob(ip, password)
        checkJob(ip, password)
        print("[+] SUCCESS")
        return True
    except Exception as e:
        print("[!] " +str(e))
        print("[-] FAILED")
        return False

if __name__ == '__main__':
    main()
