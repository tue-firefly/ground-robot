"""
Discovers SSH servers on a LAN

Author: Daan de Graaf
"""
from ip import get_ip
from ping import ping_sweep
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy

# SSH servers run on port 22 by default
PORT = 22

class SSHDiscoverer:
    def __init__(self, username, password, iface_ip=get_ip()):
        # Cut off the last octet
        i = iface_ip.rfind('.')
        self.prefix = iface_ip[:i+1]
        self.username = username
        self.password = password
        
    @property
    def cidr(self):
        return "{}0/24".format(self.prefix) 

    def live_hosts(self):
        if not hasattr(self, '__live_hosts'):
            self._live_hosts = ping_sweep(self.prefix)
        return self._live_hosts

    def live_robots(self):
        if hasattr(self, '_live_robots'):
            return self._live_robots
        self._live_robots = []
        for ip in self.live_hosts():
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            try:
                client.connect(ip, PORT, 'pi', 'raspberry')
                client.close()
                self._live_robots.append(ip)
            except:
                pass
        return self._live_robots

# This is meant to be a library, but can also be used as a quick cli tool
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        iface_ip = sys.argv[1]
    else:
        iface_ip = get_ip()
    ssh = SSHDiscoverer('pi', 'raspberry', iface_ip)
    print("Searching robots on {}".format(ssh.cidr))
    for ip in ssh.live_robots():
        print("Robot found: {}".format(ip))
