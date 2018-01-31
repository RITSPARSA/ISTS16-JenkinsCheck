# Iterate through all the hosts
from config import Config


def iterateHosts(mask, count, action):
    '''
    Iterate through the number of hosts specified, Calculate the IP to use,
    and execute "action" on the given ip
    '''
    for i in range(1,count+1):
        ip = mask.replace("x",str(i))
        action(ip)


def build(ip):
    '''Stub Function'''
    print("Building on "+ ip)

def check(ip):
    '''Stub Function'''
    print("Checking build on "+ ip)


def main():
    iterateHosts(Config.EXTERNAL_IP, Config.TEAM_COUNT, build)
    iterateHosts(Config.INTERNAL_IP, Config.TEAM_COUNT, build)
    iterateHosts(Config.EXTERNAL_IP, Config.TEAM_COUNT, check)
    iterateHosts(Config.INTERNAL_IP, Config.TEAM_COUNT, check)

if __name__ == '__main__':
    main()
