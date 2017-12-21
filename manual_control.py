"""
Script to manually control the ground robot.
To be used on a Raspberry Pi connected to the Arduino over USB,
and the sketch in this repository

Maintainer: Daan de Graaf
"""
from sys import stdin, argv
from getch import get_char
from comm import open_serial, send_cmd

if __name__ == '__main__':
    if len(argv) > 1:
        device = argv[1]
        ser = open_serial(device)
        print("Using device: {}".format(device))
    else:
        ser = open_serial()
    print("Manual control for Ground robot.")
    print("Use w-a-s-d to move around, e-r to turn. Any other button to stop moving")
    print("Press q to quit")
    while True:
        char = get_char()
        if char == 'w':
            send_cmd(ser, 0, 200, 0)
        elif char == 'W':
            send_cmd(ser, 0, 500, 0)
        elif char == 'a':
            send_cmd(ser, -200, 0, 0)
        elif char == 's':
            send_cmd(ser, 0, -200, 0)
        elif char == 'd':
            send_cmd(ser, 200, 0, 0)
        elif char == 'e':
            send_cmd(ser, 0, 0, -200)
        elif char == 'r':
            send_cmd(ser, 0, 0, 200)
        elif char == 'q':
            send_cmd(ser, 0, 0, 0)
            break
        else:
            send_cmd(ser, 0, 0, 0)
