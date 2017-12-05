"""
Script to manually control the ground robot.
To be used on a Raspberry Pi connected to the Arduino over USB,
and the sketch in this repository

Maintainer: Daan de Graaf
"""
from sys import stdin
from serial import Serial
import struct
from getch import get_char

DEVICE='/dev/ttyACM0'

ser = Serial(DEVICE, 115200)

def send_cmd(x, y, psi):
    data = struct.pack('=fff', x, y, psi)
    ser.write(data)
    ser.flush()

if __name__ == '__main__':
    print("Manual control for Ground robot.")
    print("Use w-a-s-d to move around, e-r to turn. Any other button to stop moving")
    print("Press q to quit")
    while True:
        char = get_char()
        if char == 'w':
            send_cmd(0, 200, 0)
        elif char == 'W':
            send_cmd(0, 500, 0)
        elif char == 'a':
            send_cmd(-200, 0, 0)
        elif char == 's':
            send_cmd(0, -200, 0)
        elif char == 'd':
            send_cmd(200, 0, 0)
        elif char == 'e':
            send_cmd(0, 0, -200)
        elif char == 'r':
            send_cmd(0, 0, 200)
        elif char == 'q':
            send_cmd(0, 0, 0)
            break
        else:
            send_cmd(0, 0, 0)
