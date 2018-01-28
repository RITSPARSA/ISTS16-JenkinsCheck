#/usr/bin/python3

from creds import user, pw, address, buildName
import jenkins

server = jenkins.Jenkins(address, username=user, password=pw)
server.build_job(buildName)
