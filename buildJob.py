#/usr/bin/python3

from creds import user, pw, address, buildName
from checkJob import check
import jenkins
import time

def build():
    for ip in address:
        server = jenkins.Jenkins(ip, username=user, password=pw, timeout=30)
        server.build_job(buildName)
    time.sleep(10)
    for ip in address:
        server = jenkins.Jenkins(ip, username=user, password=pw, timeout=30)
        if buildName not in server.get_running_builds():
            check(ip)

def main():
    build()

if __name__ == '__main__':
    main()
