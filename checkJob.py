#/usr/bin/python3

from creds import user, pw, address, buildName, whiteteamKEY
import jenkins

# the desired build result
success='SUCCESS'

# connect to jenkins
server = jenkins.Jenkins(address, username=user, password=pw)
# get the last build number
build_num = server.get_job_info(buildName)['lastBuild']['number']
# retrieve the output of the build
output = server.get_build_console_output(buildName, build_num)

# ensure output contains success and whiteteamKEY
if (success in output) and (whiteteamKEY in output):
    print("Build {0} succeeded".format(build_num))
else:
    print("Build {0} FAILED".format(build_num))
