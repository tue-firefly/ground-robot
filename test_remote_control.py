"""
Basic test script for remote_contro.py. Sends a command to move in X direction over UDP.

Maintainer: Daan de Graaf
"""
import socket
import struct
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 12000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def send(x, y, psi):
    sock.sendto(struct.pack("=ddd", x, y, psi), (UDP_IP, UDP_PORT))


send(200, 0, 0)
time.sleep(2)
send(-200, 0, 0)
