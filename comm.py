"""
Basic communication library for pi to to Arduino

Maintainer: Daan de Graaf
"""
import serial
import struct
import time

DEVICE = '/dev/ttyACM0'
BAUD = 115200

# Opens a serial connection to the Arduino
def open_serial():
    ser = serial.Serial(DEVICE, BAUD)
    time.sleep(1)
    send_cmd(ser, 0, 0, 0)
    return ser

def send_cmd(ser, x, y, psi):
    data = struct.pack('=fff', x, y, psi)
    ser.write(data)
    ser.flush()
