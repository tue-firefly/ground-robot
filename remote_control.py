"""
Script to receive commands from the base station (over UDP) and relay them to the arduino.
TODO: Also allows for Hardware-In-the-Loop simulation by returning the integrated velocities.

Maintainer: Daan de Graaf
"""
import serial 
import socket
import struct
from comm import open_serial, send_cmd

# UDP socket parameters
UDP_IP = '0.0.0.0'
UDP_PORT = 12000

# A command consists of 3 doubles, which are 8 bytes long each
COMMAND_SIZE = 3*8

# Mass of the robot for calculating velocity from force
MASS = 1

def udp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    # Reduce the socket timeout
    sec	= 1
    usec = 500000
    timeval	= struct.pack('ll', sec, usec)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
    return sock

if __name__ == '__main__':
    sock = udp_socket()
    ser = open_serial()

    v_x = 0
    v_y = 0
    while True:
        try:
            # Read and parse command
            data, addr = sock.recvfrom(COMMAND_SIZE)
            (f_x, f_y, psi) = struct.unpack('=ddd', data)

            # Forward euler's method
            # TODO That's for later

            v_x += f_x * MASS
            v_y += f_y * MASS
            print("Sending: {}".format((v_x, v_y, psi)))
            send_cmd(ser, v_x, v_y, psi)
        except BlockingIOError:
            # Nothing received, no problem
            pass
        except KeyboardInterrupt:
            print()
            send_cmd(ser, 0, 0, 0)
            break
