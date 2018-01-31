'''
Keep track of where builds are started so that we know
which hosts to check
'''

class HostManager(object):
    def __init__(self):
        # Start off with round 0
        self.ROUND_NUM = 0
        # All the hosts that we have failed on this round
        self.FAILED = {}
        # All the hosts that have triggered a build
        self.WORKED = []

    def nextRound(self):
        self.ROUND_NUM += 1
        self.WORKED = []

    def failHost(self, host):
        # Increment the number of times this host has failed
        self.FAILED[host] = self.FAILED.get(host, 0) + 1

    def passHost(self, host):
        # Clear all fails from the host
        self.FAILED.pop(host, None)
        # Add to the host list
        if host not in self.WORKED:
            self.WORKED += [host]

HostMan = HostManager()
