#!/bin/env python3
import sys
from ip import get_ip
from discover import SSHDiscoverer
import argparse
from paramiko import SSHClient
from paramiko.ssh_exception import SSHException
from os import path
import sys

SSH_PORT = 22
PI_USER = 'pi'
PI_PASSWORD = 'raspberry'

DEPLOY_PATH = '/home/pi/remote_control/'
DEPLOY_FILES = [
    'remote_control.py',
    'comm.py',
    'remote_control.service',
    'post_deploy.sh'
]
POST_DEPLOY_COMMAND = 'cd {} && bash {}'.format(DEPLOY_PATH, DEPLOY_FILES[-1])
class DeployException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def deploy(ip, username, password):
    print("==== Deploying to {} ====".format(ip.ljust(15)))
    ssh = SSHClient()
    ssh.load_system_host_keys()
    try:
        ssh.connect(ip, SSH_PORT, username, password)
        # Create deploy path
        cmd = 'mkdir -p {}'.format(DEPLOY_PATH)
        (stdin, stdout, stderr) = ssh.exec_command(cmd)
        if stdout.channel.recv_exit_status() != 0:
            raise DeployException('Could not execute {}'.format(cmd))
        # Copy all files
        print("Copying files..")
        sftp = ssh.open_sftp()
        for filename in DEPLOY_FILES:
            local_path = path.join(path.dirname(sys.argv[0]), '..', filename)
            remote_path = DEPLOY_PATH + filename
            print('{} --> {}:{}'.format(local_path.ljust(30), ip, remote_path))
            sftp.put(local_path, remote_path, confirm=True)
        print("Running setup script..")
        # Run setup script, pipe output back?
        (stdin, stdout, stderr) = ssh.exec_command(POST_DEPLOY_COMMAND)
        for line in stdout.readlines():
            print('> ' + line, end='')

    except SSHException as e:
       raise DeployException(e.value)
    finally:
        ssh.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy code to ground robots on the LAN")
    parser.add_argument('ip', nargs='?', 
        help='an ip in the subnet to scan for robots', default=get_ip())
    parser.add_argument('-u', '--username', default=PI_USER,
        help='the username for SSH connections')
    parser.add_argument('-p', '--password', default=PI_PASSWORD,
        help='the password for SSH connections')
    parser.add_argument('--targets', default=None,
        help='comma-separated list of targets to deploy to. Skips scanning phase. example: 0.0.0.0,1.1.1.1')
    args = parser.parse_args()

    if not args.targets:
        disc = SSHDiscoverer(args.username, args.password, args.ip)
        print("Scanning {} for robots".format(disc.cidr))
        print("Live hosts: {}".format(", ".join(disc.live_hosts())))
        print("Robots found: {}".format(", ".join(disc.live_robots())))
        targets = disc.live_robots()
    else:
        targets = args.targets.split(',')
        if len(targets) == 0:
            print("Invalid list of targets. Make sure there a no spaces in between!")
            sys.exit(1)

    if not targets:
        print("No targets found. Deployment failed.")
        sys.exit(1)
    
    confirm = input('Deploy to {}? [Y/n] [ENTER] '.format(", ".join(targets)))
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        sys.exit(1)

    for ip in targets:
        try:
            deploy(ip, args.username, args.password)
        except DeployException as e:
            print("Failed to deploy to {}: {}".format(ip, e))
            confirm = input('Continue? [y/N] [ENTER] ')
            if confirm.lower() != 'y':
                print("Deployment halted.")
                sys.exit(1)
