"""
Script to manually control the ground robot.
To be used on a Raspberry Pi connected to the Arduino over USB,
and the sketch in this repository

Maintainer: Daan de Graaf
"""
from sys import stdin, argv
from getch import get_char
import serial_comm
import udp_comm

if __name__ == '__main__':
    sock = None
    ser = None
    if len(argv) > 1:
        device = argv[1]
        if len(device.split('.')) == 4:
            # This is probably an IP address
            sock = udp_comm.open_socket(device)
        else:
            ser = serial_comm.open_serial(device)
        print("Using device: {}".format(device))
    else:
        print("WARN: No device or IP address passed as argument, assuming default /dev/ttyUSB0")
        ser = serial_comm.open_serial()
    print("Manual control for Ground robot.")
    print("Use w-a-s-d to move around, e-r to turn. Any other button to stop moving")
    print("Press q to quit")

    def send_cmd(x, y, psi):
        if sock is not None:
            udp_comm.send_cmd(sock, 2, x, y, psi)
        else:
            serial_comm.send_cmd(ser, x, y, psi)
    
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
            send_cmd(0, 0, -400)
        elif char == 'r':
            send_cmd(0, 0, 400)
        elif char == 'q':
            send_cmd(0, 0, 0)
            break
        else:
            send_cmd(0, 0, 0)
