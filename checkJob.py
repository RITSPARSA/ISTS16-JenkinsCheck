#/usr/bin/python3

from creds import user, pw, address, buildName, whiteteamKEY
import jenkins

def check(addr):
    # the desired build result
    success='SUCCESS'

    # connect to jenkins
    server = jenkins.Jenkins(addr, username=user, password=pw, timeout=30)
    # get the last build number
    build_num = server.get_job_info(buildName)['lastBuild']['number']
    # retrieve the output of the build
    output = server.get_build_console_output(buildName, build_num)

    # ensure output contains success and whiteteamKEY
    if (success in output) and (whiteteamKEY in output):
        print("Build {0} for {1} succeeded".format(build_num, addr))
    else:
        print("Build {0} for {1} FAILED".format(build_num, addr))

    return

def main():
    for addr in address:
        check(addr)

if __name__ == '__main__':
    main()
