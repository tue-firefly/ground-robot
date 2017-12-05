"""
Script to run a simple test sequence to verify correct behaviour of motors and arduino controller.
To be run on a Raspberry Pi connected via USB to an Arduino with the sketch in this repository.

Maintainer: Daan de Graaf
"""
from sys import stdin
from serial import Serial
import struct
from time import sleep

DEVICE = '/dev/ttyACM0'

ser = Serial(DEVICE, 115200)

def send_cmd(x, y, psi):
    data = struct.pack('=fff', x, y, psi)
    ser.write(data)
    ser.flush()

if __name__ == '__main__':
    print("Test sequence for ground robot")

    send_cmd(0, 0, 0)
    sleep(2)

    print("Moving in X direction")
    send_cmd(200, 0, 0)
    sleep(2)
    send_cmd(0, 0, 0)
    sleep(0.2)

    print("Moving in Y direction")
    send_cmd(0, 200, 0)
    sleep(2)
    send_cmd(0, 0, 0)
    sleep(0.2)

    print("Rotating one full circle")
    send_cmd(0, 0, 200)
    sleep(6.7)
    send_cmd(0, 0, 0)
