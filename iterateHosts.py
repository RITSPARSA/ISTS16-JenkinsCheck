# Iterate through all the hosts
from creds import creds
from config import Config
import jenkins, json
import sys

def iterateHosts(mask, count, action):
    '''
    Iterate through the number of hosts specified, Calculate the IP to use,
    and execute "action" on the given ip
    '''
    for i in range(1,count+1):
        ip = mask.replace("x",str(i))
        action(ip, i)

def connect(url, user, pw):
    try:
        return jenkins.Jenkins(url, user, pw, timeout=10)
    except Exception:
        print("Issue connecting to {}").format(url)
        return False

''' Build if connection there '''
def build(ip, teamNum):
    '''Stub Function'''
    print("Building on "+ ip)
    if submitJob(ip, teamNum):
        pws=json.load(open('passwords.json'))
        # connect to the server (server address, username, password, timeout)
        print('http://{}:8080'.format(ip))
        server = connect('http://{}:8080'.format(ip), creds.user,
            pws.get(teamNum, 'Changeme-2018'))
        try:
            # start the job (name of the job to build)
            server.build_job(creds.buildName)
            return True
        except Exception:
            print("Couldn't connect to "+ ip)
            return False
    return

def check(ip, teamNum):
    '''Stub Function'''
    print("Checking build on "+ ip)

    # the desired build result
    success='SUCCESS'

    pws=json.load(open('passwords.json'))
    # connect to the server (server address, username, password, timeout)
    server = connect('http://{}:8080'.format(ip), creds.user,
        pws.get(teamNum, 'Changeme-2018'))
    try:
        # get the last build number (name of the build to get)
        build_num = server.get_job_info(creds.buildName)['lastBuild']['number']
        # retrieve the output of the build (name of build, number of that build)
        output = server.get_build_console_output(creds.buildName, build_num)
        # ensure output contains success and whiteteamKEY
        if (success in output) and (creds.whiteteamKEY in output):
            print("Build {0} for {1} succeeded".format(build_num, ip))
        else:
            print("Build {0} for {1} FAILED".format(build_num, ip))
        return True
    except Exception:
        print("Couldn't connect to "+ ip)
        return False
    return

def submitJob(ip, teamNum):
    pws=json.load(open('passwords.json'))
    # connect to the server (server address, username, password, timeout)
    server = connect('http://{}:8080'.format(ip), creds.user,
        pws.get(teamNum, 'Changeme-2018'))
    try:
        if not server.job_exists(creds.buildName):
            # read xml file into variable
            xml=open(creds.xmlFile, 'r').read()
            server.create_job(creds.buildName, xml)
        return True
    except Exception:
        print("Couldn't connect to "+ ip)
        return False
    return


def main():
    iterateHosts(Config.EXTERNAL_IP, Config.TEAM_COUNT, build)
    iterateHosts(Config.INTERNAL_IP, Config.TEAM_COUNT, build)
    iterateHosts(Config.EXTERNAL_IP, Config.TEAM_COUNT, check)
    iterateHosts(Config.INTERNAL_IP, Config.TEAM_COUNT, check)

if __name__ == '__main__':
    main()
