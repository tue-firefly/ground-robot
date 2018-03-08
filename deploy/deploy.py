"""
Deploys remote_control.py to all Pi's on the local network.

Author: Daan de Graaf
"""

#!/usr/bin/env python3
import sys
import argparse
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy
from paramiko.ssh_exception import SSHException
from os import path
from string import Template
import os
import sys
import pnock

SSH_PORT = 22
PI_USER = 'pi'
PI_PASSWORD = 'raspberry'

def rel_path(*args):
    return path.join(path.dirname(sys.argv[0]), *args)

DEPLOY_PATH = '/home/pi/remote_control/'
DEPLOY_FILES = [
    rel_path('..', 'remote_control.py'),
    rel_path('..', 'serial_comm.py'),
]

POST_DEPLOY_COMMAND = 'cd {} && bash {}'.format(DEPLOY_PATH, 'post_deploy.sh')

SCRIPT_DIR = path.dirname(sys.argv[0])

ARDUINO_SKETCH_DEFAULT_PATH = path.join(SCRIPT_DIR, '..', '..', 
    'omnibot-controller', 'controller', 'controller.ino')

class DeployException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def deploy(ip, username, password, arduino_sketch_file=None):
    print("==== Deploying to {} ====".format(ip.ljust(15)))
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
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

        def copy_file(local_path, remote_path):
            print('{} --> {}:{}'.format(local_path.ljust(30), ip, remote_path))
            sftp.put(local_path, remote_path, confirm=True)

        deploy_files = DEPLOY_FILES
        for f in os.listdir(rel_path('files')):
            deploy_files.append(rel_path('files', f))


        for local_path in deploy_files:
            filename = path.basename(local_path)
            remote_path = DEPLOY_PATH + filename
            copy_file(local_path, remote_path)

        if arduino_sketch_file is not None:
            copy_file(path.join(path.dirname(arduino_sketch_file), 'Makefile'), DEPLOY_PATH + 'Makefile')
            copy_file(arduino_sketch_file, DEPLOY_PATH + 'sketch.ino')

        print("Running setup script..")
        # Run setup script, pipe output back?
        channel = ssh.get_transport().open_session()
        channel.exec_command(POST_DEPLOY_COMMAND)
        while not channel.exit_status_ready():
            if channel.recv_stderr_ready():
                os.write(sys.stderr.fileno(), channel.recv_stderr(4096))
            if channel.recv_ready():
                os.write(sys.stdout.fileno(), channel.recv(4096))


    except SSHException as e:
       raise DeployException(e.value)
    finally:
        ssh.close()

def find_arduino_sketch():
    if path.isfile(ARDUINO_SKETCH_DEFAULT_PATH):
        return ARDUINO_SKETCH_DEFAULT_PATH
    return None

def is_robot(ip, user, passwd):
    
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    try:
        client.connect(ip, SSH_PORT, user, passwd)
        client.close()
        return True
    except:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy code to ground robots on the LAN")
    parser.add_argument('ip', nargs='?', 
        help='an ip in the subnet to scan for robots', default=pnock.local_ip())
    parser.add_argument('-u', '--username', default=PI_USER,
        help='the username for SSH connections')
    parser.add_argument('-p', '--password', default=PI_PASSWORD,
        help='the password for SSH connections')
    parser.add_argument('--targets', default=None,
        help='comma-separated list of targets to deploy to. Skips scanning phase. example: 0.0.0.0,1.1.1.1')
    parser.add_argument('--wpa', default=None,
        help='credentials to login to the tue-wpa2 network. example: s123456:password123')
    args = parser.parse_args()

    if not args.targets:
        live_hosts = pnock.sweep_lan(SSH_PORT, iface_ip=args.ip)
        print("Live hosts: {}".format(", ".join(live_hosts)))
        targets = list(filter(lambda ip: is_robot(ip, args.username, args.password), live_hosts))
        print("Live robots: {}".format(", ".join(targets)))
    else:
        targets = args.targets.split(',')
        if len(targets) == 0:
            print("Invalid list of targets. Make sure there a no spaces in between!")
            sys.exit(1)

    if not targets:
        print("No targets found. Deployment failed.")
        sys.exit(1)

    arduino_sketch_file = find_arduino_sketch()
    if arduino_sketch_file is None:
        print("Arduino sketch not found, skipping...")

    if args.wpa is not None:
        parts = args.wpa.split(':')
        if len(parts) != 2:
            print('Invalid credentials specified: {}'.format(args.wpa))
            sys.exit(1)
        creds = {
            'username': parts[0],
            'password': parts[1]
        }
        with open(rel_path('wpa_supplicant.conf.tue-wpa2.template'), 'r') as template:
            template = Template(template.read())
            rendered = template.substitute(creds)
            outfile = open(rel_path('files', 'wpa_supplicant.conf.tue-wpa2'), 'w')
            outfile.write(rendered)
            outfile.close()
            print('tue-wpa2 credentials ready for uploading')
    else:
        try:
            # Cleanup old wpa_supplicant files (they contain passwords so we should be careful
            os.remove(rel_path('files', 'wpa_supplicant.conf.tue-wpa2'))
        except:
            pass
    
    confirm = input('Deploy to {}? [Y/n] [ENTER] '.format(", ".join(targets)))
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        sys.exit(1)

    for ip in targets:
        try:
            deploy(ip, args.username, args.password, arduino_sketch_file)
        except DeployException as e:
            print("Failed to deploy to {}: {}".format(ip, e))
            confirm = input('Continue? [y/N] [ENTER] ')
            if confirm.lower() != 'y':
                print("Deployment halted.")
                sys.exit(1)
