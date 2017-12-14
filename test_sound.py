import socket
import struct
import time
import sys

if len(sys.argv) < 2:
    print("ERR: Pass target ip as input")
    sys.exit(1)
UDP_IP = sys.argv[1]
UDP_PORT = 12000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def send(x, y, psi):
    sock.sendto(struct.pack("=ddd", x, y, psi), (UDP_IP, UDP_PORT))

for _ in range(0, 5):
    send(10, 0, 0)
    time.sleep(0.3)
    send(-10, 0, 0)
    time.sleep(0.3)
