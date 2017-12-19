"""
Very basic controller that communicates with topcam-tracker 
and remote_control.py to have the ground robot hold 
the position given by REF. If you run the topcam-tracker on
the same laptop, start it with 'tracker 1 127.0.0.1 6000'

Adjust ROBOT_IP as needed.

Maintainer: Daan de Graaf
"""
import socket
import struct
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 6000

ROBOT_IP = "192.168.0.100"
ROBOT_PORT = 12000

REF = (0.5, 3, 0)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

send_sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def send_cmd(sock, v_x, v_y, v_psi):
    data = struct.pack('=Bddd', 2, v_x, v_y, v_psi)
    sock.sendto(data, (ROBOT_IP, ROBOT_PORT))

while True:
    data, addr = sock.recvfrom(4 + 3*8)
    (i, x, y, psi) = struct.unpack('=Iddd', data)
    
    ref_psi = 1000 * (REF[2] - psi)
    ref_psi = min(200, ref_psi)
    ref_psi = max(-200, ref_psi)

    ref_x = 1000 * (REF[0] - x)
    ref_x = min(200, max(-200, ref_x))
    ref_y = 1000 * (REF[1] - y)
    ref_y = min(200, max(-200, ref_y))
    if abs(ref_psi) > 100:
        print("Angle unstable: {}".format(psi))
        ref_x = 0
        ref_y = 0
    else:
        print("ref_x: {}, ref_y: {}".format(ref_x, ref_y))
    send_cmd(send_sock, ref_x, ref_y, ref_psi)
