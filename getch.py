"""
Simple library to read raw character inputs from the terminal without any buffering.
Linux support only!

Author: Daan de Graaf
"""

def get_char():
    try:
        return get_char_unix()
    except ImportError:
        return get_char_windows()

def get_char_unix():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_char_windows():
    import msvcrt
    return msvcrt.getch()
