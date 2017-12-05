"""
Simple library to read raw character inputs from the terminal without any buffering.
Linux support only!

Author: Daan de Graaf
"""
import sys, tty, termios

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
